#!/usr/bin/env python3

"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/electricimp/MAX17055
"""

import json

from scs_core.data.json import JSONify

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_config import Max17055Config


# --------------------------------------------------------------------------------------------------------------------

conf = BattPackV1.gauge_conf()
print(conf)
print("-")

jstr = JSONify.dumps(conf)
print(jstr)
print("-")

jdict = json.loads(jstr)
conf = Max17055Config.construct_from_jdict(jdict)
print(conf)

