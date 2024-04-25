"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
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

    __SOURCE = 'Mv2'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        standby = jdict.get('standby')
        input_power_present = jdict.get('in')
        v_in = jdict.get('pwr-in')
        charge_status = ChargeStatus.construct_from_jdict(jdict.get('batt'))

        return cls(standby, input_power_present, v_in, charge_status)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, standby, input_power_present, v_in, charge_status):
        """
        Constructor
        """
        self.__standby = standby                                    # bool
        self.__input_power_present = input_power_present            # bool
        self.__v_in = Datum.float(v_in, 1)                          # PSU input voltage  float
        self.__charge_status = charge_status                        # ChargeStatus


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['standby'] = self.standby
        jdict['in'] = self.input_power_present
        jdict['pwr-in'] = self.v_in
        jdict['batt'] = None if self.charge_status is None else self.charge_status.as_json()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def below_power_threshold(self, charge_min):
        if self.charge_status is None:
            return False                                    # power threshold cannot be identified

        if self.charge_status.tte is None:
            return False                                    # device is not running on battery or gauge disconnected

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
    def input_power_present(self):
        return self.__input_power_present


    @property
    def v_in(self):
        return self.__v_in


    @property
    def batt_percent(self):
        return None if self.__charge_status is None else self.__charge_status.charge


    @property
    def charge_status(self):
        return self.__charge_status


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus(mobile_v2):{standby:%s, input_power_present:%s, v_in:%s, charge_status:%s}" % \
               (self.standby, self.input_power_present, self.v_in, self.charge_status)


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
