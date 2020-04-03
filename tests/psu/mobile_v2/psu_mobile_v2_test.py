#!/usr/bin/env python3

"""
Created on 1 Apr 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

See also: scs_dfe_end/tests/interface/components/rpz_header_test.py
"""

import time

from scs_core.data.json import JSONify

from scs_dfe.interface.pzhb.pzhb_mcu_t3_f1 import PZHBMCUt3f1

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.psu.mobile_v2.psu_mobile_v2 import PSUMobileV2


# --------------------------------------------------------------------------------------------------------------------

batt_pack = BattPackV1.construct()
print(batt_pack)

psu = PSUMobileV2(PZHBMCUt3f1(PZHBMCUt3f1.DEFAULT_ADDR), batt_pack)
print(psu)
print("-")

try:
    psu.open()

    while True:
        status = psu.status()

        print(status)
        print(JSONify.dumps(status))
        print("-")

        time.sleep(5.0)

finally:
    psu.close()
