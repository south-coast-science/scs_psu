"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"standby": "False", "in": "True", "pwr-in": 12.5, "rst": 0, "chg": 1000, "batt-flt": "False", "host-3v3": 3.3,
"prot-batt": 8.4}}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.psu.psu_report import PSUReport


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(PSUReport):
    """
    classdocs
    """

    POWER_IN_MINIMUM =        7.0           # Volts
    BATTERY_MINIMUM =         6.4           # Volts

    __SOURCE = 'Pv1'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        v_in = jdict.get('pwr-in')

        power_reset = jdict.get('p-rst')
        watchdog_reset = jdict.get('w-rst')

        battery_fault = jdict.get('batt-flt')

        host_3v3 = jdict.get('host-3v3')
        prot_batt = jdict.get('prot-batt')

        return cls(power_reset, watchdog_reset, battery_fault, host_3v3, v_in, prot_batt)


    @classmethod
    def null_datum(cls):
        return cls(None, None, None, None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, power_reset, watchdog_reset, battery_fault, host_3v3, v_in, prot_batt):
        """
        Constructor
        """
        self.__power_reset = power_reset                        # restart because host was powered down     bool
        self.__watchdog_reset = watchdog_reset                  # restart because of watchdog timeout       bool

        self.__battery_fault = battery_fault                    # battery fault                             bool

        self.__host_3v3 = Datum.float(host_3v3, 1)              # host 3V3 voltage                          float
        self.__v_in = Datum.float(v_in, 1)                      # PSU input voltage                         float
        self.__prot_batt = Datum.float(prot_batt, 1)            # battery voltage                           float


    # ----------------------------------------------------------------------------------------------------------------

    def is_null_datum(self):
        return self.__power_reset is None and self.__watchdog_reset is None and self.__battery_fault is None and \
               self.__host_3v3 is None and self.__v_in is None and self.__prot_batt is None


    def below_power_threshold(self, _charge_min):
        if self.input_power_present:
            return False

        return self.prot_batt < self.BATTERY_MINIMUM


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['in'] = self.input_power_present
        jdict['pwr-in'] = self.v_in

        jdict['p-rst'] = self.power_reset
        jdict['w-rst'] = self.watchdog_reset

        jdict['batt-flt'] = self.battery_fault

        jdict['host-3v3'] = self.host_3v3
        jdict['prot-batt'] = self.prot_batt

        return jdict


    # ----------------------------------------------------------------------------------------------------------------
    # PSUReport properties...

    @property
    def source(self):
        return self.__SOURCE


    @property
    def standby(self):
        return None


    @property
    def input_power_present(self):
        return self.v_in >= self.POWER_IN_MINIMUM


    @property
    def v_in(self):
        return self.__v_in


    @property
    def batt_percent(self):
        return None


    @property
    def charge_status(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power_reset(self):
        return self.__power_reset


    @property
    def watchdog_reset(self):
        return self.__watchdog_reset


    @property
    def battery_fault(self):
        return self.__battery_fault


    @property
    def host_3v3(self):
        return self.__host_3v3


    @property
    def prot_batt(self):
        return self.__prot_batt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus(prototype_v1):{power_reset:%s, watchdog_reset:%s, battery_fault:%s, " \
               "host_3v3:%s, v_in:%s, prot_batt:%s}" \
               % (self.power_reset, self.watchdog_reset, self.battery_fault,
                  self.host_3v3, self.v_in, self.prot_batt)
