"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.datetime import Timedelta
from scs_core.data.json import JSONable

from scs_core.psu.psu_report import PSUReport

from scs_psu.batt_pack.fuel_gauge.fuel_status import FuelStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUStatus(PSUReport):
    """
    classdocs
    """

    POWER_IN_MINIMUM =        3.0           # Volts

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        standby = jdict.get('standby')
        power_in = jdict.get('pwr-in')
        batt_status = jdict.get('batt')

        return PSUStatus(standby, power_in, batt_status)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, standby, power_in, batt_status):
        """
        Constructor
        """
        self.__standby = standby                            # bool
        self.__power_in = Datum.float(power_in, 1)          # PSU input voltage  float
        self.__batt_status = batt_status                    # BattStatus


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['standby'] = self.standby
        jdict['pwr-in'] = self.power_in
        jdict['batt'] = self.batt_status

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def below_power_threshold(self):
        return self.power_in < self.POWER_IN_MINIMUM        # TODO: use percentage


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def standby(self):
        return self.__standby


    @property
    def power_in(self):
        return self.__power_in


    @property
    def batt_status(self):
        return self.__batt_status


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus:{standby:%s, power_in:%s, batt_status:%s}" % (self.standby, self.power_in, self.batt_status)


# --------------------------------------------------------------------------------------------------------------------

class BattStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        charge = jdict.get('chg')
        tte = Timedelta(seconds=jdict.get('tte'))
        ttf = Timedelta(seconds=jdict.get('ttf'))

        return cls(charge, tte, ttf)


    @classmethod
    def construct_from_fuel_status(cls, fuel_status: FuelStatus):
        charge = int(round(fuel_status.charge.percent))
        tte = fuel_status.tte
        ttf = fuel_status.ttf

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
        jdict['tte'] = None if self.tte is None else int(self.tte.total_seconds())
        jdict['ttf'] = None if self.ttf is None else int(self.ttf.total_seconds())

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
        return "FuelStatus:{charge:%s, tte:%s, ttf:%s}" %  (self.charge, self.tte, self.ttf)
