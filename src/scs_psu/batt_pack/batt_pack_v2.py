"""
Created on 26 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Used by version 1 OPCubes.

Tuned for 1 x battery
"""

import json

from scs_psu.batt_pack.batt_pack import BattPack

from scs_psu.batt_pack.fuel_gauge.max17055.max17055_config import MAX17055Config
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import MAX17055Params


# --------------------------------------------------------------------------------------------------------------------

class BattPackV2(BattPack):
    """
    classdocs
    """

    __CHARGE_MINIMUM =        1         # percent

    __DEFAULT_PARAMS =  '{"calibrated-on": "2021-01-02T17:56:05Z", "r-comp-0": 156, "temp-co": 9278, ' \
                        '"full-cap-rep": 3471, "full-cap-nom": 1933, "cycles": 100}'


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def name():
        return 'PackV2'


    @staticmethod
    def gauge_conf():
        des_cap = 1200                  # mAh
        sense_res = 0.01                # Ω
        chrg_term = 10                  # mA
        empty_v_target = 3.3            # V
        recovery_v = 3.8                # V

        chrg_v = MAX17055Config.CHRG_V_4_2
        batt_type = MAX17055Config.BATT_TYPE_LiCoO2

        return MAX17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def charge_min(cls):
        return cls.__CHARGE_MINIMUM


    @classmethod
    def default_params(cls):
        return MAX17055Params.construct_from_jdict(json.loads(cls.__DEFAULT_PARAMS))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gauge):
        """
        Constructor
        """
        super().__init__(gauge)
