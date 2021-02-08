"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Cube board + OPCube PSU power pack + fuel gauge
"""

from scs_host.bus.i2c import I2C

from scs_psu.psu.i2c_psu import I2CPSU
from scs_psu.psu.opcube_v1.mcp3221 import MCP3221
from scs_psu.psu.opcube_v1.pca9534 import PCA9534

from scs_psu.psu.opcube_v1.psu_status import PSUStatus, ChargeStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUOPCubeV1(I2CPSU):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return 'OPCubeV1'


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

        self.__batt_pack = batt_pack                            # BattPackV2

        self.__charger = PCA9534(PCA9534.DEFAULT_ADDR)
        self.__v_in_monitor = MCP3221(MCP3221.DEFAULT_ADDR)


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        I2C.Utilities.open()
        self.charger.init()


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        standby = not self.controller.switch_state()

        try:
            batt_status = self.batt_pack.sample()

            charger_status = self.charger.sample()
            v_in = self.v_in_monitor.sample()
            charge_status = ChargeStatus.construct_from_batt_status(batt_status)
            prot_batt = None if batt_status is None else batt_status.v

        except AttributeError:
            charger_status = None
            v_in = None
            charge_status = None
            prot_batt = None

        return PSUStatus(standby, charger_status, v_in, charge_status, prot_batt)


    def charge_min(self):
        return None if self.batt_pack is None else self.__batt_pack.charge_min()


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        return self.controller.version_ident()


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


    @property
    def charger(self):
        return self.__charger


    @property
    def v_in_monitor(self):
        return self.__v_in_monitor


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUOPCubeV1:{controller:%s, charger:%s, batt_pack:%s, v_in_monitor:%s}" % \
               (self.controller, self.charger, self.batt_pack, self.v_in_monitor)
