"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lightweight system Raspberry Pi Zero header + mobile power pack + fuel gauge
"""

from scs_core.psu.psu import PSU

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.psu.mobile_v2.psu_status import PSUStatus, BattStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUMobileV2(PSU):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return 'MobileV2'


    @classmethod
    def requires_interface(cls):
        return True


    @classmethod
    def report_class(cls):
        return PSUStatus


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, header):
        """
        Constructor
        """
        self.__header = header
        self.__batt_pack = BattPackV1.construct()


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        I2C.open(Host.I2C_SENSORS)

        self.__header.button_enable()


    def close(self):
        I2C.close()


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        standby = self.__header.button_pressed()
        power_in = self.__header.read_batt_v()

        fuel_status = self.__batt_pack.sample_fuel_status()
        batt_status = BattStatus.construct_from_fuel_status(fuel_status)

        return PSUStatus(standby, power_in, batt_status)


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        return self.__header.version_ident()


    def uptime(self):
        return None


    def host_shutdown_initiated(self):
        return self.__header.host_shutdown_initiated()


    def watchdog_start(self, interval):
        return None


    def watchdog_stop(self):
        return None


    def watchdog_touch(self):
        return None


    def charge_pause(self, on):
        return None


    def charge_dead(self, on):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUMobileV2:{header:%s, batt_pack:%s}" % (self.__header, self.__batt_pack)
