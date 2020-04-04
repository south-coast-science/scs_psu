"""
Created on 3 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Tuned for 2 x Nitecore IMR 18650 (3.7 V, 3100 mAh)
https://www.nitecore.co.uk/Shop/Products/Batteries/13663-Nitecore-IMR-18650-Battery-for-TM28-Torch.html#Features
"""

import json

from scs_psu.batt_pack.fuel_gauge.max17055.max17055 import MAX17055
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_config import MAX17055Config
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import MAX17055Params


# --------------------------------------------------------------------------------------------------------------------

class BattPackV1(object):
    """
    classdocs
    """

    __CHARGE_MINIMUM =        5         # percent

    __DEFAULT_PARAMS =  '{"r-comp-0": 171, "temp-co": 8766, "full-cap-rep": 16712, "full-cap-nom": 41298, "cycles": 1}'

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def name():
        return 'PackV1'


    @staticmethod
    def gauge_conf():
        des_cap = 6200                  # mAh
        sense_res = 0.01                # Ω
        chrg_term = 40                  # mA
        empty_v_target = 3.3            # V
        recovery_v = 3.5                # V

        chrg_v = MAX17055Config.CHRG_V_4_2              # was CHRG_V_4_4_OR_4_35
        batt_type = MAX17055Config.BATT_TYPE_LiCoO2

        return MAX17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)


    @classmethod
    def charge_min(cls):
        return cls.__CHARGE_MINIMUM


    @classmethod
    def default_params(cls):
        return MAX17055Params.construct_from_jdict(json.loads(cls.__DEFAULT_PARAMS))


    @classmethod
    def construct(cls):
        conf = cls.gauge_conf()
        gauge = MAX17055(conf)

        return BattPackV1(gauge)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gauge):
        """
        Constructor
        """
        self.__gauge = gauge


    # ----------------------------------------------------------------------------------------------------------------

    def initialise(self, force_config=False):
        if not self.__gauge.read_power_on_reset() and not force_config:
            return False

        self.__gauge.initialise(force_config=force_config)
        self.write_params(self.default_params())

        return True


    def read_learned_params(self):
        return self.__gauge.read_learned_params()


    def write_params(self, params: MAX17055Params):
        self.__gauge.write_params(params)


    def sample_fuel_status(self):
        return self.__gauge.sample()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BattPackV1:{gauge:%s}" %  self.__gauge
