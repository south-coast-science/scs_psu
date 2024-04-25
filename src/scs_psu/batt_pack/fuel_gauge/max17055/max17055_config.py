"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/electricimp/MAX17055
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Max17055Config(JSONable):
    """
    classdocs
    """
    CHRG_V_4_2 =            0x00
    CHRG_V_4_4_OR_4_35 =    0x01

    BATT_TYPE_LiCoO2 =      0
    BATT_TYPE_NCA_NCR =     2
    BATT_TYPE_LiFePO4 =     6


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        des_cap = jdict.get('des-cap')
        sense_res = jdict.get('sense-res')
        chrg_term = jdict.get('chrg-term')
        empty_v_target = jdict.get('empty-v-target')
        recovery_v = jdict.get('recovery-v')
        chrg_v = jdict.get('chrg-v')
        batt_type = jdict.get('batt-type')

        return Max17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type):
        """
        Constructor
        """
        self.__des_cap = Datum.int(des_cap)                         # designed capacity of the battery (mAh)
        self.__sense_res = Datum.float(sense_res, 3)                # size of the sense resistor (Ω)
        self.__chrg_term = Datum.int(chrg_term)                     # battery’s termination charge (mA)
        self.__empty_v_target = Datum.float(empty_v_target, 2)      # empty target voltage (V, resolution is 10mV)
        self.__recovery_v = Datum.float(recovery_v, 2)              # recovery voltage (V)
        self.__chrg_v = Datum.int(chrg_v)                           # charge voltage (see constants)
        self.__batt_type = Datum.int(batt_type)                     # type of battery (see constants)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['des-cap'] = self.des_cap
        jdict['sense-res'] = self.sense_res
        jdict['chrg-term'] = self.chrg_term
        jdict['empty-v-target'] = self.empty_v_target
        jdict['recovery-v'] = self.recovery_v
        jdict['chrg-v'] = self.chrg_v
        jdict['batt-type'] = self.batt_type

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def des_cap(self):
        return self.__des_cap


    @property
    def sense_res(self):
        return self.__sense_res


    @property
    def chrg_term(self):
        return self.__chrg_term


    @property
    def empty_v_target(self):
        return self.__empty_v_target


    @property
    def recovery_v(self):
        return self.__recovery_v


    @property
    def chrg_v(self):
        return self.__chrg_v


    @property
    def batt_type(self):
        return self.__batt_type


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Max17055Config:{des_cap:%s, sense_res:%s, chrg_term:%s, empty_v_target:%s, " \
               "recovery_v:%s, chrg_v:%s, batt_type:%s}" % \
               (self.des_cap, self.sense_res, self.chrg_term, self.empty_v_target,
                self.recovery_v, self.chrg_v, self.batt_type)
