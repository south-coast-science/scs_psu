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

    __SOURCE = 'Mv1'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        standby = jdict.get('standby')
        v_in = jdict.get('pwr-in')

        return cls(standby, v_in)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, standby, v_in):
        """
        Constructor
        """
        self.__standby = standby                            # bool
        self.__v_in = Datum.float(v_in, 1)                  # PSU input voltage  float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['src'] = self.source

        jdict['standby'] = self.standby
        jdict['pwr-in'] = self.v_in

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def below_power_threshold(self, _charge_min):
        return False                                        # power threshold cannot be identified


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
        return None


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

    def __str__(self, *args, **kwargs):
        return "PSUStatus(mobile_v1):{standby:%s, v_in:%s}" % (self.standby, self.v_in)
