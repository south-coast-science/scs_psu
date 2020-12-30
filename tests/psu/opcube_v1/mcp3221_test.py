#!/usr/bin/env python3

"""
Created on 29 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C

from scs_psu.psu.opcube_v1.mcp3221 import MCP3221


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Utilities.open()

    adc = MCP3221(MCP3221.DEFAULT_ADDR)
    print(adc)
    print("=")

    while True:
        sample = adc.sample()
        print(sample)
        print("-")

        time.sleep(2.0)

except KeyboardInterrupt:
    print()

finally:
    I2C.Utilities.close()
