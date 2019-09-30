#!/usr/bin/env python3

"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.json import JSONify

from scs_psu.fuel_gauage.max17055 import MAX17055

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    gauge = MAX17055(5.0)
    print(gauge)
    print("-")

    while True:
        gauge.read_rep_cap()
        gauge.read_rep_soc_percent()
        gauge.read_tte()
        print("-")
        time.sleep(2.0)

finally:
    I2C.close()
