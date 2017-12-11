"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"rst": 10, "link-in": false, "chg": 1010, "batt-flt": false, "host-3v3": 3.4, "pwr-in": 12.3, "prot-batt": 9.9}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        reset = ResetStatus.construct_from_jdict(jdict.get('rst'))

        link_in = jdict.get('link-in')

        charger = ChargerStatus.construct_from_jdict(jdict.get('chg'))

        battery_fault = jdict.get('batt-flt')

        host_3v3 = jdict.get('host-3v3')
        power_in = jdict.get('pwr-in')
        prot_batt = jdict.get('prot-batt')

        return PSUStatus(reset, link_in, charger, battery_fault, host_3v3, power_in, prot_batt)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reset, link_in, charger, battery_fault, host_3v3, power_in, prot_batt):
        """
        Constructor
        """
        self.__reset = reset                                # ResetStatus

        self.__link_in = link_in                            # bool

        self.__charger = charger                            # ChargerStatus

        self.__battery_fault = battery_fault                # battery fault                             bool

        self.__host_3v3 = Datum.float(host_3v3, 1)          # host 3V3 voltage                          float
        self.__power_in = Datum.float(power_in, 1)          # PSU input voltage                         float
        self.__prot_batt = Datum.float(prot_batt, 1)        # battery voltage                           float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rst'] = self.reset

        jdict['link-in'] = self.link_in

        jdict['chg'] = self.charger

        jdict['batt-flt'] = self.battery_fault

        jdict['host-3v3'] = self.host_3v3
        jdict['pwr-in'] = self.power_in
        jdict['prot-batt'] = self.prot_batt

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def reset(self):
        return self.__reset


    @property
    def link_in(self):
        return self.__link_in


    @property
    def charger(self):
        return self.__charger


    @property
    def battery_fault(self):
        return self.__battery_fault


    @property
    def host_3v3(self):
        return self.__host_3v3


    @property
    def power_in(self):
        return self.__power_in


    @property
    def prot_batt(self):
        return self.__prot_batt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus:{reset:%s, link_in:%s, charger:%s, battery_fault:%s, " \
               "host_3v3:%s, power_in:%s, prot_batt:%s}" \
               % (self.reset, self.link_in, self.charger, self.battery_fault,
                  self.host_3v3, self.power_in, self.prot_batt)


# --------------------------------------------------------------------------------------------------------------------

class ResetStatus(JSONable):
    """
    classdocs
    """


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = list(str(jdict))

        power_reset = bool(int(items[0]))
        watchdog_reset = bool(int(items[1]))

        return ResetStatus(power_reset, watchdog_reset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, power_reset, watchdog_reset):
        """
        Constructor
        """
        self.__power_reset = power_reset                    # restart because host was powered down     bool
        self.__watchdog_reset = watchdog_reset              # restart because of watchdog timeout       bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        items = (self.power_reset, self.watchdog_reset)

        item_string = ''.join(['1' if item else '0' for item in items])

        return item_string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power_reset(self):
        return self.__power_reset


    @property
    def watchdog_reset(self):
        return self.__watchdog_reset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ResetStatus:{power_reset:%s, watchdog_reset:%s}" % (self.power_reset, self.watchdog_reset)


# --------------------------------------------------------------------------------------------------------------------

class ChargerStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = list(str(jdict))

        ready = bool(int(items[0]))
        fault = bool(int(items[1]))
        charging = bool(int(items[2]))
        top_off_charge = bool(int(items[3]))

        return ChargerStatus(ready, fault, charging, top_off_charge)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ready, fault, charging, top_off_charge):
        """
        Constructor
        """
        self.__ready = ready                                # bool
        self.__fault = fault                                # bool
        self.__charging = charging                          # bool
        self.__top_off_charge = top_off_charge              # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        items = (self.ready, self.fault, self.charging, self.top_off_charge)

        item_string = ''.join(['1' if item else '0' for item in items])

        return item_string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ready(self):
        return self.__ready


    @property
    def fault(self):
        return self.__fault


    @property
    def charging(self):
        return self.__charging


    @property
    def top_off_charge(self):
        return self.__top_off_charge


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChargerStatus:{ready:%s, fault:%s, charging:%s, top_off_charge:%s}" % \
               (self.ready, self.fault, self.charging, self.top_off_charge)
