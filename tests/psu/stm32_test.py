#!/usr/bin/env python3

"""
Created on 12 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_psu.psu.stm32 import STM32


# --------------------------------------------------------------------------------------------------------------------

mcu = STM32()
mcu.open()

print(mcu)


mcu.write_reg(STM32.ADDR_POWER_WAIT_SECS, 0x20)

value = mcu.read_reg(STM32.ADDR_POWER_WAIT_SECS)
print("wait: 0x%02x" % value)


mcu.write_reg(STM32.ADDR_POWER_OFF_SECS, 0x10)

value = mcu.read_reg(STM32.ADDR_POWER_OFF_SECS)
print("off: 0x%02x" % value)


mcu.cmd(STM32.CMD_POWER_CYCLE)


mcu.close()
