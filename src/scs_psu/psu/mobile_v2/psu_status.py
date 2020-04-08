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

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        standby = jdict.get('standby')
        power_in = jdict.get('pwr-in')
        charge_status = ChargeStatus.construct_from_jdict(jdict.get('batt'))

        return PSUStatus(standby, power_in, charge_status)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, standby, power_in, charge_status):
        """
        Constructor
        """
        self.__standby = standby                                # bool
        self.__power_in = Datum.float(power_in, 1)              # PSU input voltage  float
        self.__charge_status = charge_status                    # ChargeStatus


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['standby'] = self.standby
        jdict['pwr-in'] = self.power_in
        jdict['batt'] = self.charge_status

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def below_power_threshold(self, charge_min):
        if self.charge_status is None:
            return False                                    # power threshold cannot be identified

        if self.charge_status.tte is None:
            return False                                    # device is not running on battery or gauge disconnected

        return self.charge_status.charge < charge_min


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def standby(self):
        return self.__standby


    @property
    def batt_percent(self):
        return None if self.__charge_status is None else self.__charge_status.charge


    @property
    def power_in(self):
        return self.__power_in


    @property
    def charge_status(self):
        return self.__charge_status


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus:{standby:%s, power_in:%s, charge_status:%s}" % \
               (self.standby, self.power_in, self.charge_status)


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

    def as_json(self):
        jdict = OrderedDict()

        jdict['chg'] = self.charge
        jdict['tte'] = self.tte
        jdict['ttf'] = self.ttf

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
