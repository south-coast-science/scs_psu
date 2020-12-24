#!/usr/bin/env python3

"""
Created on 3 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.batt_pack.fuel_gauge.max17055.max17055 import MAX17055

from scs_host.bus.i2c import UtilityI2C


# --------------------------------------------------------------------------------------------------------------------

try:
    UtilityI2C.open()

    conf = BattPackV1.gauge_conf()

    gauge = MAX17055(conf)
    print(gauge)
    print("-")

    print("read...")
    params = gauge.read_learned_params()
    print(params)
    print("-")

    # print("restore...")
    # gauge.restore_learned_params(params)
    # print("-")

    # print("read...")
    # params = gauge.read_learned_params()
    # print(params)

except KeyboardInterrupt:
    print()

finally:
    UtilityI2C.close()
