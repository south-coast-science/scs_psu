"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"src": "Cv1", "standby": false, "in": true, "pwr-in": 11.5, "chgr": "TFTF",
"batt": {"chg": 99, "tte": null, "ttf": null}, "prot-batt": 4.1}
"""

from collections import OrderedDict

from scs_core.data.datetime import Timedelta
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.psu.psu_report import PSUReport


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(PSUReport):
    """
    classdocs
    """

    POWER_IN_MINIMUM =        7.0           # Volts
    BATTERY_MINIMUM =         3.2           # Volts

    __SOURCE = 'Cv1'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        standby = jdict.get('standby')
        charger_status = ChargerStatus.construct_from_jdict(jdict.get('chgr'))
        v_in = jdict.get('pwr-in')

        charge_status = ChargeStatus.construct_from_jdict(jdict.get('batt'))
        prot_batt = jdict.get('prot-batt')

        return cls(standby, charger_status, v_in, charge_status, prot_batt)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, standby, charger_status, v_in, charge_status, prot_batt):
        """
        Constructor
        """
        self.__standby = standby                                # bool
        self.__charger_status = charger_status                  # ChargerStatus
        self.__v_in = Datum.float(v_in, 1)                      # PSU input voltage  float

        self.__charge_status = charge_status                    # ChargeStatus
        self.__prot_batt = Datum.float(prot_batt, 1)            # battery voltage  float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['standby'] = self.standby
        jdict['in'] = self.input_power_present
        jdict['pwr-in'] = self.v_in
        jdict['chgr'] = self.charger_status.as_json()

        jdict['batt'] = None if self.charge_status is None else self.charge_status.as_json()
        jdict['prot-batt'] = self.prot_batt

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def below_power_threshold(self, charge_min):
        if self.charge_status is None:
            return False                                    # power threshold cannot be identified

        if self.v_in > self.BATTERY_MINIMUM:                # DC input power is available or battery is charged
            return False

        return self.charge_status.charge < charge_min


    # ----------------------------------------------------------------------------------------------------------------
    # PSUReport properties...

    @property
    def source(self):
        return self.__SOURCE


    @property
    def standby(self):
        return self.__standby


    @property
    def charger_status(self):
        return self.__charger_status


    @property
    def input_power_present(self):
        return self.v_in is not None and self.v_in >= self.POWER_IN_MINIMUM


    @property
    def v_in(self):
        return self.__v_in


    @property
    def batt_percent(self):
        return None if self.__charge_status is None else self.__charge_status.charge


    @property
    def charge_status(self):
        return self.__charge_status


    @property
    def prot_batt(self):
        return self.__prot_batt


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus(opcube_v1):{standby:%s, charger_status:%s, v_in:%s, charge_status:%s, prot_batt:%s}" % \
               (self.standby, self.charger_status, self.v_in, self.charge_status, self.prot_batt)


# --------------------------------------------------------------------------------------------------------------------

class ChargeStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        charge = jdict.get('chg')
        tte = Timedelta.construct_from_jdict(jdict.get('tte'))
        ttf = Timedelta.construct_from_jdict(jdict.get('ttf'))

        return cls(charge, tte, ttf)


    @classmethod
    def construct_from_batt_status(cls, batt_status):
        if batt_status is None:
            return None

        charge = int(round(batt_status.charge.percent))
        tte = batt_status.tte
        ttf = batt_status.ttf

        return cls(charge, tte, ttf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, charge, tte, ttf):
        """
        Constructor
        """
        self.__charge = Datum.int(charge)                       # int           percentage
        self.__tte = tte                                        # TimeDelta     time to empty
        self.__ttf = ttf                                        # TimeDelta     time to full


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['chg'] = self.charge
        jdict['tte'] = None if self.tte is None else self.tte.as_json()
        jdict['ttf'] = None if self.ttf is None else self.ttf.as_json()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def charge(self):
        return self.__charge


    @property
    def tte(self):
        return self.__tte


    @property
    def ttf(self):
        return self.__ttf


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChargeStatus:{charge:%s, tte:%s, ttf:%s}" %  (self.charge, self.tte, self.ttf)


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

        ready = jdict[0] == 'T'
        fault = jdict[1] == 'T'
        charging = jdict[2] == 'T'
        power_fail = jdict[3] == 'T'

        return ChargerStatus(ready, fault, charging, power_fail)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ready, fault, charging, power_fail):
        """
        Constructor
        """
        self.__ready = ready                                # bool
        self.__fault = fault                                # bool
        self.__charging = charging                          # bool
        self.__power_fail = power_fail                      # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        items = (self.ready, self.fault, self.charging, self.power_fail)

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
    def power_fail(self):
        return self.__power_fail


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChargerStatus:{ready:%s, fault:%s, charging:%s, power_fail:%s}" % \
               (self.ready, self.fault, self.charging, self.power_fail)
