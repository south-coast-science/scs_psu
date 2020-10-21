#!/usr/bin/env python3

"""
Created on 21 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

See also: scs_dfe_eng/tests/interface/opcube/opcube_t1_test.py
"""

import time

from scs_core.data.json import JSONify

from scs_dfe.interface.opcube.opcube_mcu_t1 import OPCubeMCUt1

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.psu.opcube_v1.psu_opcube_v1 import PSUOPCubeV1


# --------------------------------------------------------------------------------------------------------------------

batt_pack = BattPackV1.construct()
print(batt_pack)

controller = OPCubeMCUt1(OPCubeMCUt1.DEFAULT_ADDR)
print(controller)

psu = PSUOPCubeV1(controller, batt_pack)
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
