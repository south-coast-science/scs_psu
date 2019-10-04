#!/usr/bin/env python3

"""
Created on 3 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_psu.fuel_gauage.batt_pack_v1_gauge import BattPackV1Gauge

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    gauge = BattPackV1Gauge()
    print(gauge)
    print("-")

    print("read...")
    params = gauge.read_learned_params()
    print(params)
    print("-")

    print("restore...")
    gauge.restore_learned_params(params)
    print("-")

    print("read...")
    params = gauge.read_learned_params()
    print(params)

except KeyboardInterrupt:
    print()

finally:
    I2C.close()
