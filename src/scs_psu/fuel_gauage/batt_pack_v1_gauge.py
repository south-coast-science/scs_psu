"""
Created on 3 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Tuned for 2 x Nitecore IMR 18650 (3.7 V, 3100 mAh)
https://www.nitecore.co.uk/Shop/Products/Batteries/13663-Nitecore-IMR-18650-Battery-for-TM28-Torch.html#Features
"""

from scs_psu.fuel_gauage.max17055.max17055 import MAX17055
from scs_psu.fuel_gauage.max17055.max17055_config import MAX17055Config


# --------------------------------------------------------------------------------------------------------------------

class BattPackV1Gauge(MAX17055):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        des_cap = 6200              # mAh
        sense_res = 0.01            # Ω
        chrg_term = 10              # mA
        empty_v_target = 2.7        # V
        recovery_v = 3.0            # V

        chrg_v = MAX17055Config.CHRG_V_4_4_OR_4_35
        batt_type = MAX17055Config.BATT_TYPE_LiCoO2

        conf = MAX17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)

        super().__init__(conf)
