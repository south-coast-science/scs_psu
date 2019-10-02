#!/usr/bin/env python3

"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/electricimp/MAX17055
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_psu.fuel_gauage.max17055_config import MAX17055Config


# --------------------------------------------------------------------------------------------------------------------

des_cap = 6200
sense_res = 0.01
chrg_term = 250                 # 20
empty_v_target = 2.7
recovery_v = 3.0
chrg_v = MAX17055Config.CHRG_V_4_4_OR_4_35
batt_type = MAX17055Config.BATT_TYPE_LiCoO2

conf = MAX17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)
print(conf)
print("-")

jstr = JSONify.dumps(conf)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
conf = MAX17055Config.construct_from_jdict(jdict)
print(conf)

