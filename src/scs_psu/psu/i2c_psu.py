"""
Created on 8 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract PSU that communicates over I2C
"""

from abc import ABC

from scs_core.data.json import JSONify
from scs_core.psu.psu import PSU

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class I2CPSU(PSU, ABC):
    """
    South Coast Science PSU via UART
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def requires_interface(cls):
        return True


    # ----------------------------------------------------------------------------------------------------------------

    def close(self):
        I2C.Utilities.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, controller):
        """
        Constructor
        """
        self.__controller = controller                          # MCU


    # ----------------------------------------------------------------------------------------------------------------

    def communicate(self, command):
        if command == 'name':
            return JSONify.dumps(self.name())

        if command == 'version':
            return JSONify.dumps(self.version())

        if command == 'state':
            return JSONify.dumps(self.status())

        if command == 'batt':
            sample = None if self.batt_pack is None else self.batt_pack.sample()
            return JSONify.dumps(sample)

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def power_peripherals(self, on):
        self.controller.power_all(on)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def controller(self):
        return self.__controller
