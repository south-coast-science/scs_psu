"""
Created on 12 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable

from scs_psu.psu.stm32 import STM32


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, byte):
        charger_pause = bool(byte & STM32.STATUS_CHARGER_PAUSE)

        battery_dead = bool(byte & STM32.STATUS_BATTERY_DEAD)
        battery_fault = bool(byte & STM32.STATUS_BATTERY_FAULT)
        battery_on = bool(byte & STM32.STATUS_ON_BATTERY)

        socket_on = bool(byte & STM32.STATUS_ON_SOCKET)

        run = bool(byte & STM32.STATUS_RUN)

        return PSUStatus(charger_pause, battery_dead, battery_fault, battery_on, socket_on, run)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, charger_pause, battery_dead, battery_fault, battery_on, socket_on, run):
        """
        Constructor
        """
        self.__charger_pause = charger_pause

        self.__battery_dead = battery_dead
        self.__battery_fault = battery_fault
        self.__battery_on = battery_on

        self.__socket_on = socket_on

        self.__run = run


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['chg_pause'] = self.charger_pause

        jdict['bat_dead'] = self.battery_dead
        jdict['bat_fault'] = self.battery_fault
        jdict['bat_on'] = self.battery_on

        jdict['soc_on'] = self.socket_on

        jdict['run'] = self.run

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def charger_pause(self):
        return self.__charger_pause


    @property
    def battery_dead(self):
        return self.__battery_dead


    @property
    def battery_fault(self):
        return self.__battery_fault


    @property
    def battery_on(self):
        return self.__battery_on


    @property
    def socket_on(self):
        return self.__socket_on


    @property
    def run(self):
        return self.__run


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus:{charger_pause:%s, battery_dead:%s, battery_fault:%s, battery_on:%s, socket_on:%s, run:%s}" \
               % (self.charger_pause, self.battery_dead, self.battery_fault, self.battery_on, self.socket_on, self.run)
