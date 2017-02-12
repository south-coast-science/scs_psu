#!/usr/bin/env python3

"""
Created on 12 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    psu = PSU()
    print(psu)

finally:
    I2C.close()
