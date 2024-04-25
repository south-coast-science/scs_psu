"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"src": "Ov1", "standby": false, "in": true, "pwr-in": 12.5, "rst": "FF", "chgr": "TFFF", "batt-flt": false,
"host-3v3": 3.3, "prot-batt": 8.9}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.psu.psu_report import PSUReport


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(PSUReport):
    """
    classdocs
    """

    POWER_IN_MINIMUM =        7.0           # Volts
    BATTERY_MINIMUM =         6.4           # Volts

    __SOURCE = 'Ov1'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        charger_jdict = jdict.get('chgr') if 'chgr' in jdict else jdict.get('chg')

        reset = ResetStatus.construct_from_jdict(jdict.get('rst'))
        standby = jdict.get('standby')
        charger = ChargerStatus.construct_from_jdict(charger_jdict)
        battery_fault = jdict.get('batt-flt')

        host_3v3 = jdict.get('host-3v3')
        v_in = jdict.get('pwr-in')
        prot_batt = jdict.get('prot-batt')

        return cls(reset, standby, charger, battery_fault, host_3v3, v_in, prot_batt)


    @classmethod
    def null_datum(cls):
        return cls(None, None, None, None, None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reset, standby, charger, battery_fault, host_3v3, v_in, prot_batt):
        """
        Constructor
        """
        self.__reset = reset                                # ResetStatus

        self.__standby = standby                            # bool

        self.__charger = charger                            # ChargerStatus

        self.__battery_fault = battery_fault                # battery fault                             bool

        self.__host_3v3 = Datum.float(host_3v3, 1)          # host 3V3 voltage                          float
        self.__v_in = Datum.float(v_in, 1)                  # PSU input voltage                         float
        self.__prot_batt = Datum.float(prot_batt, 1)        # battery voltage                           float


    # ----------------------------------------------------------------------------------------------------------------

    def is_null_datum(self):
        return self.__reset is None and self.__standby is None and self.__charger is None and \
               self.__battery_fault is None and self.__host_3v3 is None and self.__v_in is None and \
               self.__prot_batt is None


    def below_power_threshold(self, _charge_min):
        if self.input_power_present is None or self.prot_batt is None:
            return None

        if self.input_power_present:
            return False

        return self.prot_batt < self.BATTERY_MINIMUM


    # ----------------------------------------------------------------------------------------------------------------
    # PSUReport properties...

    @property
    def source(self):
        return self.__SOURCE


    @property
    def standby(self):
        return self.__standby


    @property
    def input_power_present(self):
        if self.v_in is None:
            return None

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

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['standby'] = self.standby
        jdict['in'] = self.input_power_present
        jdict['pwr-in'] = self.v_in

        jdict['rst'] = None if self.reset is None else self.reset.as_json()
        jdict['chgr'] = None if self.charger is None else self.charger.as_json()

        jdict['batt-flt'] = self.battery_fault

        jdict['host-3v3'] = self.host_3v3
        jdict['prot-batt'] = self.prot_batt

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def reset(self):
        return self.__reset


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
    def prot_batt(self):
        return self.__prot_batt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus(oslo_v1):{reset:%s, standby:%s, charger:%s, battery_fault:%s, " \
               "host_3v3:%s, v_in:%s, prot_batt:%s}" \
               % (self.reset, self.standby, self.charger, self.battery_fault,
                  self.host_3v3, self.v_in, self.prot_batt)


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

        power_reset = jdict[0] == 'T'
        watchdog_reset = jdict[1] == 'T'

        return ResetStatus(power_reset, watchdog_reset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, power_reset, watchdog_reset):
        """
        Constructor
        """
        self.__power_reset = power_reset                    # restart because host was powered down     bool
        self.__watchdog_reset = watchdog_reset              # restart because of watchdog timeout       bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        items = (self.power_reset, self.watchdog_reset)

        item_string = ''.join(['T' if item else 'F' for item in items])

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

        items = str(jdict)

        ready = items[0] in ('T', '1')
        fault = items[1] in ('T', '1')
        charging = items[2] in ('T', '1')
        top_off_charge = items[3] in ('T', '1')

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

    def as_json(self, **kwargs):
        items = (self.ready, self.fault, self.charging, self.top_off_charge)

        item_string = ''.join(['T' if item else 'F' for item in items])

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
