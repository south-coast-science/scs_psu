#!/usr/bin/env python3

"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_psu.psu.oslo_v1.psu_status import PSUStatus


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"rst": "FT", "standby": false, "chgr": "TFTF", "batt-flt": false, "host-3v3": 3.3, "pwr-in": 13.0, ' \
       '"prot-batt": 0.0}'
print(jstr)
print("-")

jdict = json.loads(jstr)
print(jdict)
print("-")

status = PSUStatus.construct_from_jdict(jdict)
print(status)
print("-")

jdict = status.as_json()
print(jdict)
print("-")

jstr = JSONify.dumps(jdict)
print(jstr)
print("-")
