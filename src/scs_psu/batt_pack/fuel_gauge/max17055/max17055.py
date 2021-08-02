"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Maxim Integrated 1-Cell Fuel Gauge with ModelGauge m5 EZ

4.5 Save learned parameters
It is recommended to save the learned capacity parameters every time bit 6 of the Cycles register toggles
(so that it is saved every 64% change in the battery) so that if power is lost the values can easily be restored.

https://www.maximintegrated.com/en/products/power/battery-management/MAX17055.html
https://www.maximintegrated.com/en/design/technical-documents/userguides-and-manuals/6/6365.html
https://github.com/electricimp/MAX17055
"""

import time

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Decode
from scs_core.data.timedelta import Timedelta

from scs_host.bus.i2c import I2C
from scs_host.lock.lock import Lock

from scs_psu.batt_pack.fuel_gauge.batt_status import BattStatus, ChargeLevel

from scs_psu.batt_pack.fuel_gauge.max17055.max17055_config import Max17055Config
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import Max17055Params


# --------------------------------------------------------------------------------------------------------------------

class Max17055(object):
    """
    classdocs
    """

    __PARAM_SAVE_INTERVAL =     5               # % change in charge after which params should be saved

    __ADDR =                    0x36

    __LOCK_TIMEOUT =            1.0             # seconds

    __REG_CHECK_NUM_RETRIES =   20              # tenths of a second

    __REG_STATUS =              0x00
    __REG_ALERT_VOLT =          0x01
    __REG_ALERT_TEMP =          0x02
    __REG_ALERT_CHARGE =        0x03
    __REG_REP_CAP =             0x05            # reported capacity
    __REG_REP_SOC =             0x06            # reported state of charge
    __REG_TEMP =                0x08
    __REG_V_CELL =              0x09            # Voltage
    __REG_CURRENT =             0x0a
    __REG_CURRENT_AVG =         0x0b
    __REG_MIX_SOC =             0x0d            # state of charge
    __REG_MIX_CAP =             0x0f

    __REG_FULL_CAP_REP =        0x10            # reported full capacity
    __REG_TTE =                 0x11            # time to empty
    __REG_TEMP_AVG =            0x16
    __REG_CYCLES =              0x17            # charging cycle count
    __REG_DESIGN_CAP =          0x18
    __REG_V_CELL_AVG =          0x19            # Voltage
    __REG_MAX_MIN_TEMP =        0x1a
    __REG_MAX_MIN_VOLT =        0x1b            # Voltage
    __REG_MAX_MIN_CURRENT =     0x1c
    __REG_I_CHRG_TERM =         0x1e
    __REG_CAP_AVG =             0x1f

    __REG_TTF =                 0x20            # time to full
    __REG_DEV_NAME =            0x21            # device name / version
    __REG_FULL_CAP_NOM =        0x23

    __REG_DIE_TEMP =            0x34
    __REG_R_COMP_0 =            0x38
    __REG_TEMP_CO =             0x39
    __REG_FSTAT =               0x3d
    __REG_V_EMPTY =             0x3a

    __REG_D_Q_ACC =             0x45
    __REG_D_P_ACC =             0x46

    __REG_HIB_MODE =            0x60            # hibernate mode

    __REG_POWER =               0xb1
    __REG_POWER_AVG =           0xb3
    __REG_ALERT_CURRENT =       0xb4
    __REG_HIB_CFG =             0xba            # hibernate configuration

    __REG_MODEL_CFG =           0xdb


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def param_save_interval(cls):
        return cls.__PARAM_SAVE_INTERVAL


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, conf: Max17055Config):
        """
        Constructor
        """
        self.__conf = conf


    # ----------------------------------------------------------------------------------------------------------------

    def initialise_as_github(self, force_config=False):
        # PoR?...
        if not self.read_power_on_reset() and not force_config:
            self.clear_power_on_reset()
            return False                                        # configuration is not updated

        try:
            self.obtain_lock()

            # wait for DNR to clear...
            self.__wait_for_reg_value(self.__REG_FSTAT, 0x0001, 0)

            # store hibernate configuration...
            hib_cfg = self.__read_reg(self.__REG_HIB_CFG)

            self.__write_reg(self.__REG_HIB_MODE, 0x90)
            self.__write_reg(self.__REG_HIB_CFG, 0x00)
            self.__write_reg(self.__REG_HIB_MODE, 0x00)

            # set battery config...
            des_cap = int(round(self.__conf.des_cap / self.__capacity_lsb()))
            self.__write_reg(self.__REG_DESIGN_CAP, des_cap)

            dq_acc = int(round(des_cap / 32))
            self.__write_reg(self.__REG_D_Q_ACC, dq_acc)

            # termination charge...
            chrg_therm = int(round(self.__conf.chrg_term / self.__current_lsb()))
            self.__write_reg(self.__REG_I_CHRG_TERM, chrg_therm)

            # Empty Voltage Target set in 10mV increments to bits 7-15,
            # Recovery Voltage set in 40mV increments to bits 0-6
            empty_v_target = int(self.__conf.empty_v_target * 100)
            recovery_v = int(self.__conf.recovery_v * 25)

            self.__write_reg(self.__REG_V_EMPTY, (empty_v_target << 7) | recovery_v)

            # refactored from: (des_Cap / 32) * (dPAccCoefficient / des_cap) = dPAccCoefficient / 32
            #             1600                                         1379
            dp_acc = int(51200 / 32) if self.__conf.chrg_v else int(44138 / 32)
            self.__write_reg(self.__REG_D_P_ACC, dp_acc)

            # model Refresh (bit 15), VChg (bit 10), ModelId (bits 4-7)
            model_cfg = (0x8000 | (self.__conf.chrg_v << 10) | (self.__conf.batt_type << 4))
            self.__write_reg(self.__REG_MODEL_CFG, model_cfg)

            # wait for reload...
            self.__wait_for_reg_value(self.__REG_MODEL_CFG, 0x8000, 0)

            # restore hibernate configuration...
            self.__write_reg(self.__REG_HIB_CFG, hib_cfg)

            # clear boot status...
            status = self.__read_reg(self.__REG_STATUS)
            self.__write_and_verify_reg(self.__REG_STATUS, status & 0x777f)

            # clear PoR bit...
            self.__write_and_verify_reg(self.__REG_STATUS, 0xfffd)

            return True                                             # configuration updated

        finally:
            self.release_lock()


    def initialise(self, force_config=False):
        # PoR?...
        if not self.read_power_on_reset() and not force_config:
            self.clear_power_on_reset()
            return False                                        # configuration is not updated

        try:
            self.obtain_lock()

            # wait for DNR to clear...
            self.__wait_for_reg_value(self.__REG_FSTAT, 0x0001, 0)

            # store hibernate configuration...
            hib_cfg = self.__read_reg(self.__REG_HIB_CFG)

            self.__write_reg(self.__REG_HIB_MODE, 0x90)
            self.__write_reg(self.__REG_HIB_CFG, 0x00)
            self.__write_reg(self.__REG_HIB_MODE, 0x00)

            conf = self.__conf

            # WriteRegister (0x18 , DesignCap) ; // Write DesignCap
            self.__write_reg(self.__REG_DESIGN_CAP, conf.des_cap)

            # WriteRegister (0x45 , DesignCap/32) ; //Write dQAcc
            dq_acc = int(conf.des_cap / 32)
            self.__write_reg(self.__REG_D_Q_ACC, dq_acc)

            # WriteRegister (0x1E , IchgTerm) ; // Write IchgTerm
            self.__write_reg(self.__REG_I_CHRG_TERM, conf.chrg_term)

            # WriteRegister (0x3A , VEmpty) ; // Write VEmpty       0xa561
            # mt = (settings.emptyVTarget * 100).tointeger();
            # recovery = (settings.recoveryV * 25).tointeger();
            v_empty = int(conf.empty_v_target * 100)
            v_recovery = int(conf.recovery_v * 25)

            # combined = (v_empty << 7) | v_recovery

            self.__write_reg(self.__REG_V_EMPTY, (v_empty << 7) | v_recovery)

            # WriteRegister (0x28 , LearnCFG) ;// (Optional in the INI) Write LearnCFG

            # WriteRegister (0x46 , dQAcc*44138/DesignCap); //Write dPAcc
            d_p_acc = int(dq_acc * 44138 / conf.des_cap)
            self.__write_reg(self.__REG_D_P_ACC, d_p_acc)      # 0x0ac7

            model_cfg = (0x8000 | (conf.chrg_v << 10) | (conf.batt_type << 4))
            self.__write_reg(self.__REG_MODEL_CFG, model_cfg)

            # wait for reload...
            self.__wait_for_reg_value(self.__REG_MODEL_CFG, model_cfg, 0)

            # restore hibernate configuration...
            self.__write_reg(self.__REG_HIB_CFG, hib_cfg)

            # clear boot status...
            status = self.__read_reg(self.__REG_STATUS)
            self.__write_and_verify_reg(self.__REG_STATUS, status & 0x777f)

            # clear PoR bit...
            self.__write_and_verify_reg(self.__REG_STATUS, 0xfffd)

            return True                                             # configuration updated

        finally:
            self.release_lock()


    def sample(self):
        try:
            self.obtain_lock()

            # input power...
            input_power_present = self.input_power_present()

            # charge...
            percent = self.read_charge_percent()
            mah = self.read_charge_mah()

            charge = ChargeLevel(percent, mah)

            # datum...
            tte = self.read_time_until_empty()
            ttf = self.read_time_until_full()

            v = self.read_voltage()
            current = self.read_current_avg()
            temperature = self.read_temperature()

            capacity = self.read_capacity_avg()
            cycles = self.read_cycles()

            return BattStatus(input_power_present, charge, tte, ttf, v, current, temperature, capacity, cycles)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def read_learned_params(self):
        try:
            self.obtain_lock()

            calibrated_on = LocalizedDatetime.now()

            r_comp_0 = self.__read_reg(self.__REG_R_COMP_0)
            temp_co = self.__read_reg(self.__REG_TEMP_CO)
            full_cap_rep = self.__read_reg(self.__REG_FULL_CAP_REP)
            full_cap_nom = self.__read_reg(self.__REG_FULL_CAP_NOM)

            cycles = self.__read_reg(self.__REG_CYCLES)

            return Max17055Params(calibrated_on, r_comp_0, temp_co, full_cap_rep, full_cap_nom, cycles)

        finally:
            self.release_lock()


    def write_params(self, params: Max17055Params):
        try:
            self.obtain_lock()

            # restore capacity...
            self.__write_and_verify_reg(self.__REG_R_COMP_0, params.r_comp_0)
            self.__write_and_verify_reg(self.__REG_TEMP_CO, params.temp_co)
            self.__write_and_verify_reg(self.__REG_FULL_CAP_NOM, params.full_cap_nom)

            time.sleep(0.350)

            # restore full cap...
            full_cap_nom = self.__read_reg(self.__REG_FULL_CAP_NOM)
            mix_soc = self.__read_reg(self.__REG_MIX_SOC)

            mix_cap = int(mix_soc * full_cap_nom / 256000)
            self.__write_and_verify_reg(self.__REG_MIX_CAP, mix_cap)

            self.__write_and_verify_reg(self.__REG_FULL_CAP_REP, params.full_cap_rep)

            # set dQacc to 200% of capacity...
            d_qacc = int(params.full_cap_nom / 16)
            self.__write_and_verify_reg(self.__REG_D_Q_ACC, d_qacc)

            # set dPacc to 200%
            self.__write_and_verify_reg(self.__REG_D_Q_ACC, 0x0c80)         # 3200

            time.sleep(0.350)

            # restore cycles...
            self.__write_and_verify_reg(self.__REG_CYCLES, params.cycles)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def read_power_on_reset(self):
        status = self.__read_reg(self.__REG_STATUS)
        por = status & 0x0002

        return bool(por)


    def clear_power_on_reset(self):
        try:
            self.obtain_lock()

            status = self.__read_reg(self.__REG_STATUS)
            self.__write_and_verify_reg(self.__REG_STATUS, status & 0xfffd)

        finally:
            self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def input_power_present(self):
        return self.read_current() >= 0.0


    # ----------------------------------------------------------------------------------------------------------------

    def read_charge_percent(self):
        raw_percent = self.__read_reg(self.__REG_REP_SOC)
        percent = raw_percent / 256.0

        return round(percent, 1)


    def read_charge_mah(self):
        raw_capacity = self.__read_reg(self.__REG_REP_CAP)
        milli_amp_hours = raw_capacity * self.__capacity_lsb()

        return int(round(milli_amp_hours))


    def read_time_until_empty(self):
        raw_tte = self.__read_reg(self.__REG_TTE, signed=True)

        if raw_tte < 1:
            return None

        tte = raw_tte * 5.625

        return Timedelta(seconds=round(tte))


    def read_time_until_full(self):
        raw_ttf = self.__read_reg(self.__REG_TTF, signed=True)

        if raw_ttf < 1:
            return None

        ttf = raw_ttf * 5.625

        return Timedelta(seconds=round(ttf))


    def read_capacity_avg(self):
        raw_capacity = self.__read_reg(self.__REG_CAP_AVG, signed=True)
        milli_amp_hours = raw_capacity * self.__capacity_lsb()

        return int(round(milli_amp_hours))


    def read_current(self):
        raw_current = self.__read_reg(self.__REG_CURRENT, signed=True)
        milli_amps = raw_current * self.__current_lsb()

        return int(round(milli_amps))


    def read_current_avg(self):
        raw_current = self.__read_reg(self.__REG_CURRENT_AVG, signed=True)
        milli_amps = raw_current * self.__current_lsb()

        return int(round(milli_amps))


    def read_voltage(self):
        raw_voltage = self.__read_reg(self.__REG_V_CELL)

        volts = (raw_voltage * 0.078125) / 1000.0

        return round(volts, 1)


    def read_temperature(self):
        raw_temp = self.__read_reg(self.__REG_TEMP, signed=True)
        centigrade = raw_temp / 256.0

        return round(centigrade, 1)


    def read_cycles(self):
        raw_cycles = self.__read_reg(self.__REG_CYCLES)
        cycles = raw_cycles / 100.0

        return round(cycles, 1)


    def read_device_rev(self):
        rev = self.__read_reg(self.__REG_DEV_NAME)

        return rev


    # ----------------------------------------------------------------------------------------------------------------

    def __capacity_lsb(self):
        res_milli_ohms = self.__conf.sense_res * 1000

        return 5.0 / res_milli_ohms          # mAh


    def __current_lsb(self):
        res_milli_ohms = self.__conf.sense_res * 1000

        return 1.5625 / res_milli_ohms       # mA


    # ----------------------------------------------------------------------------------------------------------------

    def __wait_for_reg_value(self, reg, mask, expected):
        read_value = None

        for _ in range(self.__REG_CHECK_NUM_RETRIES):
            read_value = self.__read_reg(reg)

            if read_value & mask == expected:
                return

            time.sleep(0.1)

        raise RuntimeError("reg:0x%02x mask:0x%04x expected:0x%04x got:0x%04x" % (reg, mask, expected, read_value))


    def __read_reg(self, reg, signed=False):
        try:
            I2C.Utilities.start_tx(self.__ADDR)

            read_bytes = I2C.Utilities.read_cmd(reg, 2)
            time.sleep(0.001)

            return Decode.int(read_bytes, '<') if signed else Decode.unsigned_int(read_bytes, '<')

        finally:
            I2C.Utilities.end_tx()


    def __write_reg(self, reg, value):
        try:
            I2C.Utilities.start_tx(self.__ADDR)

            I2C.Utilities.write_addr(reg, value & 0x00ff, value >> 8)
            time.sleep(0.001)

        finally:
            I2C.Utilities.end_tx()


    def __write_and_verify_reg(self, reg, value):
        read_value = None

        try:
            I2C.Utilities.start_tx(self.__ADDR)

            for _ in range(3):
                # write...
                I2C.Utilities.write_addr(reg, value & 0x00ff, value >> 8)
                time.sleep(0.001)

                # read...
                read_bytes = I2C.Utilities.read_cmd(reg, 2)
                time.sleep(0.001)

                read_value = Decode.unsigned_int(read_bytes, '<')

                if read_value == value:
                    return

            raise RuntimeError("reg:0x%02x value:0x%04x got:0x%04x" % (reg, value, read_value))

        finally:
            I2C.Utilities.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def obtain_lock(self):
        Lock.acquire(self.__lock_name, self.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return self.__class__.__name__


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{conf:%s}" %  self.__conf
