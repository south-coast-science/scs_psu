"""
Created on 13 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
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

        return PSUStatus(standby, power_in)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, standby, power_in):
        """
        Constructor
        """
        self.__standby = standby                            # bool
        self.__power_in = Datum.float(power_in, 1)          # PSU input voltage  float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['standby'] = self.standby
        jdict['pwr-in'] = self.power_in

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def below_power_threshold(self, _charge_min):
        return False                                        # power threshold cannot be identified


    # ----------------------------------------------------------------------------------------------------------------
    # PSUReport properties...

    @property
    def standby(self):
        return self.__standby


    @property
    def batt_percent(self):
        return None


    @property
    def power_in(self):
        return self.__power_in


    @property
    def charge_status(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUStatus:{standby:%s, power_in:%s}" % (self.standby, self.power_in)
