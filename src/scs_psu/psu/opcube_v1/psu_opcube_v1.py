"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lightweight system Raspberry Pi Zero controller + mobile power pack + fuel gauge
"""

from scs_core.psu.psu import PSU

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_psu.psu.opcube_v1.psu_status import PSUStatus, ChargeStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUOPCubeV1(PSU):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return 'OPCubeV1'


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
        self.__controller = controller                          # OPCubeMCU
        self.__batt_pack = batt_pack                            # BattPackV1


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        I2C.open(Host.I2C_SENSORS)


    def close(self):
        I2C.close()


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        standby = not self.__controller.switch_state()

        try:
            batt_status = self.batt_pack.sample()

            input_power_present = None if batt_status is None else batt_status.input_power_present
            charge_status = ChargeStatus.construct_from_batt_status(batt_status)

        except (AttributeError, OSError):
            input_power_present = None
            charge_status = None

        return PSUStatus(standby, input_power_present, None, charge_status)


    def charge_min(self):
        return None if self.batt_pack is None else self.__batt_pack.charge_min()


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        return self.__controller.version_ident()


    def uptime(self):
        return None


    def host_shutdown_initiated(self):
        return self.__controller.host_shutdown_initiated()


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
        return "PSUOPCubeV1:{controller:%s, batt_pack:%s}" % (self.__controller, self.batt_pack)
