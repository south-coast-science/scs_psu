"""
Created on 13 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lightweight system Raspberry Pi Zero header + mobile power pack
"""

from scs_core.psu.psu import PSU

from scs_host.bus.i2c import UtilityI2C

from scs_psu.psu.mobile_v1.psu_status import PSUStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUMobileV1(PSU):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return 'MobileV1'


    @classmethod
    def requires_interface(cls):
        return True


    @classmethod
    def uses_batt_pack(cls):
        return False


    @classmethod
    def report_class(cls):
        return PSUStatus


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, header):
        """
        Constructor
        """
        self.__header = header                                      # PZHB


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        UtilityI2C.open()

        self.__header.button_enable()


    def close(self):
        UtilityI2C.close()


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        standby = self.__header.button_pressed()
        power_in = self.__header.read_batt_v()

        return PSUStatus(standby, power_in)


    def charge_min(self):
        return None


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

    @property
    def batt_pack(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUMobileV1:{header:%s}" % self.__header
