"""
Created on 3 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Used by version 1 Handhelds.

Tuned for 2 x Nitecore IMR 18650 (3.7 V, 3100 mAh)
https://www.nitecore.co.uk/Shop/Products/Batteries/13663-Nitecore-IMR-18650-Battery-for-TM28-Torch.html#Features
"""

import json

from scs_psu.batt_pack.batt_pack import BattPack

from scs_psu.batt_pack.fuel_gauge.max17055.max17055_config import Max17055Config
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import Max17055Params


# --------------------------------------------------------------------------------------------------------------------

class BattPackV1(BattPack):
    """
    classdocs
    """

    __CHARGE_MINIMUM =        1         # percent

    __DEFAULT_PARAMS =  '{"calibrated-on": "2021-04-19T13:29:46+01:00", "r-comp-0": 106, "temp-co": 8766, ' \
                        '"full-cap-rep": 10396, "full-cap-nom": 40738, "cycles": 245}'


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def name():
        return 'PackV1'


    @staticmethod
    def gauge_conf():
        des_cap = 6200                  # mAh
        sense_res = 0.01                # Ω
        chrg_term = 10                  # mA
        empty_v_target = 3.3            # V
        recovery_v = 3.8                # V

        chrg_v = Max17055Config.CHRG_V_4_2
        batt_type = Max17055Config.BATT_TYPE_LiCoO2

        return Max17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def charge_min(cls):
        return cls.__CHARGE_MINIMUM


    @classmethod
    def default_params(cls):
        return Max17055Params.construct_from_jdict(json.loads(cls.__DEFAULT_PARAMS))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gauge):
        """
        Constructor
        """
        super().__init__(gauge)
