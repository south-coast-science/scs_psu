"""
Created on 12 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable

from scs_psu.psu.stm32 import STM32


# --------------------------------------------------------------------------------------------------------------------

class StartupStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, byte):
        power_cycle = bool(byte & STM32.STARTUP_POWER_CYCLE)
        watchdog = bool(byte & STM32.STARTUP_WATCHDOG)

        return StartupStatus(power_cycle, watchdog)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, power_cycle, watchdog):
        """
        Constructor
        """
        self.__power_cycle = power_cycle
        self.__watchdog = watchdog


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pow_cycle'] = self.power_cycle
        jdict['watchdog'] = self.watchdog

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power_cycle(self):
        return self.__power_cycle


    @property
    def watchdog(self):
        return self.__watchdog


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StartupStatus:{power_cycle:%s, watchdog:%s}" % (self.power_cycle, self.watchdog)
