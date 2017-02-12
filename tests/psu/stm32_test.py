#!/usr/bin/env python3

"""
Created on 12 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_psu.psu.psu import PSU
from scs_psu.psu.stm32 import STM32


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    mcu = STM32(PSU.MCU_ADDR)
    print(mcu)

    check = mcu.read_reg(STM32.ADDR_PSU_STATUS)
    print("check:0x%02x" % check)

finally:
    I2C.close()
