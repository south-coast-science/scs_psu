"""
Created on 13 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lightweight system Raspberry Pi Zero header + mobile power pack
"""

from scs_dfe.board.rpz_header_t1_f1 import RPzHeaderT1F1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_psu.psu.mobile_v1.psu_status import PSUStatus
from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

class PSUMobileV1(PSU):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__header = RPzHeaderT1F1(RPzHeaderT1F1.DEFAULT_ADDR)


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        I2C.open(Host.I2C_SENSORS)


    def close(self):
        I2C.close()


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        standby = self.__header.button_pressed()
        power_in = self.__header.read_batt_v()

        return PSUStatus(standby, power_in)


    def construct_status_from_jdict(self, jdict):
        return PSUStatus.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        return self.__header.version_ident()


    def uptime(self):
        return None


    def do_not_resuscitate(self, enable):
        return None


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
        return "PSUMobileV1:{header:%s}" % self.__header
