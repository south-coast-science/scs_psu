"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Maxim Integrated 1-Cell Fuel Gauge with ModelGauge m5 EZ

https://www.maximintegrated.com/en/products/power/battery-management/MAX17055.html
https://pdfserv.maximintegrated.com/en/an/MAX17055-software-implementation-guide.pdf
"""

import time

from scs_core.climate.sht_datum import SHTDatum

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class MAX17055(object):
    """
    classdocs
    """

    CHARGE_VOLTAGE_BOUNDARY =   4.75            # Volts

    DESIGN_CAP =                0x1450
    I_CHG_TERM =                0x0333
    V_EMPTY =                   0xa561


    # ----------------------------------------------------------------------------------------------------------------

    __ADDR =                    0x36

    __LOCK_TIMEOUT =            1.0             # seconds

    __REG_STATUS =              0x00
    __REG_ALERT_VOLT =          0x01
    __REG_ALERT_TEMP =          0x02
    __REG_ALERT_CHARGE =        0x03
    __REG_REP_CAP =             0x05            # reported capacity
    __REG_REP_SOC =             0x06            # reported state of charge
    __REG_TEMP =                0x08
    __REG_VCELL =               0x09            # Voltage
    __REG_CURRENT =             0x0a
    __REG_CURRENT_AVG =         0x0b

    __REG_REP_FULL_CAP =        0x10            # reported full capacity
    __REG_TTE =                 0x11            # time to empty
    __REG_TEMP_AVG =            0x16
    __REG_CYCLES =              0x17            # charging cycle count
    __REG_DESIGN_CAP =          0x18
    __REG_VCELL_AVG =           0x19            # Voltage
    __REG_MAX_MIN_TEMP =        0x1a
    __REG_MAX_MIN_VOLT =        0x1b            # Voltage
    __REG_MAX_MIN_CURRENT =     0x1c
    __REG_I_CHG_TERM =          0x1e

    __REG_TTF =                 0x20            # time to full

    __REG_DIE_TEMP =            0x34
    __REG_FSTAT =               0x3d
    __REG_V_EMPTY =             0x3a

    __REG_DQ_ACC =              0x45
    __REG_DP_ACC =              0x46

    __REG_HIB_MODE =            0x60            # hibernate mode?

    __REG_POWER =               0xb1
    __REG_POWER_AVG =           0xb3
    __REG_ALERT_CURRENT =       0xb4
    __REG_HIB_CFG =             0xba            # hibernate configuration

    __REG_MODEL_CFG =           0xdb

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def null_datum(cls):
        return SHTDatum(None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, charge_voltage):
        """
        Constructor
        """
        self.__charge_voltage = charge_voltage


    # ----------------------------------------------------------------------------------------------------------------

    def initialise(self):
        try:
            self.obtain_lock()

            fstat = self.__read_register(self.__REG_FSTAT)
            print("initialise - fstat:0x%04x" % fstat)

            # clear battery removal...
            status = self.__read_register(self.__REG_STATUS)
            self.__write_register(self.__REG_STATUS, status & 0x7fff)

            status = self.__read_register(self.__REG_STATUS)
            print("initialise - status:0x%04x" % status)

            # step 1...
            if self.__get_status_por():
                # step 2...
                self.__wait_for_fstat_dnr()
                # step 3...
                self.__initialise_conf()

            # step 4...
            self.__set_initialisation_complete()

            # step 4.2...
            por = self.__get_status_por()
            print("initialise - por:%s" % por)

        finally:
            self.release_lock()


    def sample(self):
        try:
            self.obtain_lock()

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def read_rep_cap(self):
        rep_cap = self.__read_register(self.__REG_REP_CAP)
        print("read_rep_cap:%s" % rep_cap)

        return rep_cap


    def read_rep_soc_percent(self):
        rep_soc = self.__read_register(self.__REG_REP_SOC)
        rep_soc_percent = rep_soc >> 8
        print("read_rep_soc:%s" % rep_soc_percent)

        return rep_soc_percent


    def read_tte(self):
        tte = self.__read_register(self.__REG_TTE)
        print("read_tte:%s" % tte)

        return tte


    # ----------------------------------------------------------------------------------------------------------------

    # step 1...
    def __get_status_por(self):
        status = self.__read_register(self.__REG_STATUS)
        print("get_status_por - status:0x%04x" % status)

        return bool(status & 0x0002)


    # step 2...
    def __wait_for_fstat_dnr(self):
        while True:
            fstat = self.__read_register(self.__REG_FSTAT)
            print("delay_on_fstat_dnr - fstat:0x%04x" % fstat)

            if not fstat & 0x0001:
                return

            time.sleep(0.010)


    # step 3...
    def __initialise_conf(self):
        hib_cfg = self.__read_register(self.__REG_HIB_CFG)
        print("initialise_conf - hib_cfg:0x%04x" % hib_cfg)

        self.__exit_hibernate()

        # EZ config...
        dq_acc = int(self.DESIGN_CAP / 32)
        print("initialise_conf - dq_acc:0x%04x" % dq_acc)

        self.__write_register(self.__REG_DESIGN_CAP, self.DESIGN_CAP)
        self.__write_register(self.__REG_DQ_ACC, dq_acc)
        self.__write_register(self.__REG_I_CHG_TERM, self.I_CHG_TERM)
        self.__write_register(self.__REG_V_EMPTY, self.V_EMPTY)

        if self.charge_voltage > self.CHARGE_VOLTAGE_BOUNDARY:
            dp_acc = int(dq_acc * 51200 / self.DESIGN_CAP)
            model_cfg = 0x8400
        else:
            dp_acc = int(dq_acc * 44138 / self.DESIGN_CAP)
            model_cfg = 0x8000

        self.__write_register(self.__REG_DP_ACC, dp_acc)
        self.__write_register(self.__REG_MODEL_CFG, model_cfg)

        # self.__wait_for_model_cfg_refresh()

        dp_acc = self.__read_register(self.__REG_DP_ACC)
        print("initialise_conf - dp_acc:0x%04x" % dp_acc)

        model_cfg = self.__read_register(self.__REG_MODEL_CFG)
        print("initialise_conf - model_cfg:0x%04x" % model_cfg)

        self.__write_register(self.__REG_HIB_CFG, hib_cfg)


    def __exit_hibernate(self):
        self.__write_register(self.__REG_HIB_MODE, 0x90)
        self.__write_register(self.__REG_HIB_CFG, 0x00)
        self.__write_register(self.__REG_HIB_MODE, 0x00)


    def __wait_for_model_cfg_refresh(self):
        while True:
            model_cfg = self.__read_register(self.__REG_MODEL_CFG)
            print("wait_for_model_cfg_refresh - model_cfg:0x%04x" % model_cfg)

            if not (model_cfg & 0x8000):
                return

            time.sleep(1)


    # step 4...
    def __set_initialisation_complete(self):
        status = self.__read_register(self.__REG_STATUS)
        print("set_initialisation_complete - status 1:0x%04x" % status)

        self.__write_and_verify_register(self.__REG_STATUS, status & 0xfffd)

        status = self.__read_register(self.__REG_STATUS)
        print("set_initialisation_complete - status 2:0x%04x" % status)




    # ----------------------------------------------------------------------------------------------------------------

    def __write_register(self, reg, value):
        try:
            I2C.start_tx(self.__ADDR)

            I2C.write_addr(reg, value >> 8, value & 0xff)
            time.sleep(0.001)

        finally:
            I2C.end_tx()


    def __read_register(self, reg):
        try:
            I2C.start_tx(self.__ADDR)

            read_bytes = I2C.read_cmd(reg, 2)
            time.sleep(0.001)

            value = read_bytes[0] << 8 | read_bytes[1]

            return int(value)

        finally:
            I2C.end_tx()


    def __write_and_verify_register(self, reg, value):
        try:
            I2C.start_tx(self.__ADDR)

            for _ in range(3):
                # write...
                I2C.write_addr(reg, value >> 8, value & 0xff)
                time.sleep(0.001)

                # read...
                read_bytes = I2C.read_cmd(reg, 2)
                time.sleep(0.001)

                read_value = read_bytes[0] << 8 | read_bytes[1]

                if read_value == value:
                    return

            raise RuntimeError("reg:%0x02x value:%0x04x got:%0x04x")

        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return self.__class__.__name__


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def charge_voltage(self):
        return self.__charge_voltage


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MAX17055:{charge_voltage:%s}" % self.charge_voltage
