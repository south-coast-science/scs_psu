"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lightweight system Raspberry Pi Zero header + mobile power pack + fuel gauge
"""

from scs_core.psu.psu_version import PSUVersion

from scs_host.bus.i2c import I2C

from scs_psu.psu.i2c_psu import I2CPSU
from scs_psu.psu.mobile_v2.psu_status import PSUStatus, ChargeStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUMobileV2(I2CPSU):
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
    def uses_batt_pack(cls):
        return True


    @classmethod
    def report_class(cls):
        return PSUStatus


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, controller, batt_pack):
        """
        Constructor
        """
        super().__init__(controller)

        self.__batt_pack = batt_pack                                # BattPackV1


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        I2C.Utilities.open()
        self.controller.button_enable()


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        standby = self.controller.button_pressed()
        power_in = self.controller.read_batt_v()

        try:
            batt_status = self.batt_pack.sample()
            input_power_present = None if batt_status is None else batt_status.input_power_present
            charge_status = ChargeStatus.construct_from_batt_status(batt_status)        # TODO: untangle this!

        except (AttributeError, OSError):
            input_power_present = None
            charge_status = None

        return PSUStatus(standby, input_power_present, power_in, charge_status)


    def charge_min(self):
        return None if self.batt_pack is None else self.__batt_pack.charge_min()


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        id = self.controller.version_ident()
        tag = self.controller.version_tag()

        return PSUVersion.construct(id, tag)


    def uptime(self):
        return None


    def host_shutdown_initiated(self):
        return self.controller.host_shutdown_initiated()


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
        return self.__batt_pack


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUMobileV2:{header:%s, batt_pack:%s}" % (self.controller, self.batt_pack)
