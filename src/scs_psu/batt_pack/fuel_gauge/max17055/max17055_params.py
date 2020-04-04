"""
Created on 3 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Values stored here shall be in their raw (16-bit unsigned int) form.

https://www.maximintegrated.com/en/design/technical-documents/userguides-and-manuals/6/6365.html

Document example:
{"r-comp-0": 171, "temp-co": 8766, "full-cap-rep": 16712, "full-cap-nom": 41298, "cycles": 966}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MAX17055Params(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        r_comp_0 = jdict.get('r-comp-0')
        temp_co = jdict.get('temp-co')
        full_cap_rep = jdict.get('full-cap-rep')
        full_cap_nom = jdict.get('full-cap-nom')

        cycles = jdict.get('cycles')

        return MAX17055Params(r_comp_0, temp_co, full_cap_rep, full_cap_nom, cycles)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, r_comp_0, temp_co, full_cap_rep, full_cap_nom, cycles):
        """
        Constructor
        """
        self.__r_comp_0 = r_comp_0                      # unsigned int
        self.__temp_co = temp_co                        # unsigned int
        self.__full_cap_rep = full_cap_rep              # unsigned int
        self.__full_cap_nom = full_cap_nom              # unsigned int

        self.__cycles = Datum.int(cycles)               # unsigned int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['r-comp-0'] = self.r_comp_0
        jdict['temp-co'] = self.temp_co
        jdict['full-cap-rep'] = self.full_cap_rep
        jdict['full-cap-nom'] = self.full_cap_nom

        jdict['cycles'] = self.cycles

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def r_comp_0(self):
        return self.__r_comp_0


    @property
    def temp_co(self):
        return self.__temp_co


    @property
    def full_cap_rep(self):
        return self.__full_cap_rep


    @property
    def full_cap_nom(self):
        return self.__full_cap_nom


    @property
    def cycles(self):
        return self.__cycles


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MAX17055Params:{r_comp_0:%s, temp_co:%s, full_cap_rep:%s, full_cap_nom:%s, cycles:%s}" % \
               (self.r_comp_0, self.temp_co, self.full_cap_rep, self.full_cap_nom, self.cycles)
