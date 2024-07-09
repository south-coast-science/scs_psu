#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta

from scs_psu.batt_pack.fuel_gauge.batt_status import BattStatus, ChargeLevel


# --------------------------------------------------------------------------------------------------------------------

charge = ChargeLevel(23.2, 2057)
print(charge)
print("-")

tte = Timedelta(hours=1, minutes=2, seconds=3)
ttf = Timedelta(hours=11, minutes=21, seconds=31)


datum = BattStatus(True, charge, tte, ttf, 3.3, 1024, 31.2, 4096, 66.5)
print(datum)
print("-")

jstr = JSONify.dumps(datum)
print(jstr)
print("-")

jdict = json.loads(jstr)

datum = BattStatus.construct_from_jdict(jdict)
print(datum)
print("-")

percent = datum.charge.percent
print("percent:%s%%" % percent)
