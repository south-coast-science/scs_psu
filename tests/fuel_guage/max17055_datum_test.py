#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify
from scs_core.data.timedelta import Timedelta

from scs_psu.fuel_gauage.max17055_datum import MAX17055Charge, MAX17055Datum


# --------------------------------------------------------------------------------------------------------------------

charge = MAX17055Charge(23.2, 2057)
print(charge)
print("-")

tte = Timedelta(hours=1, minutes=2, seconds=3)
ttf = Timedelta(hours=11, minutes=21, seconds=31)

datum = MAX17055Datum(charge, tte, ttf, 1024, 31.2)
print(datum)
print("-")

jstr = JSONify.dumps(datum)
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

datum = MAX17055Datum.construct_from_jdict(jdict)
print(datum)
print("-")

percent = datum.charge.percent
print("percent:%s%%" % percent)
