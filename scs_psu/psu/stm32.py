"""
Created on 10 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class STM32(object):
    """
    STM32 32-Bit ARM Cortex-M Microcontroller
    """

    CMD_CLEAR =                 0x00        # 0000 0000
    CMD_POWER_CYCLE =           0x01        # 0000 0001
    CMD_WATCHDOG_RESET =        0x02        # 0000 0010
    CMD_RTC_SET =               0x04        # 0000 0100
    CMD_RTC_RUN =               0x80        # 0000 1000
    CMD_ADC_READ =              0x10        # 0001 0000

    STATUS_CHARGER_PAUSE =      0x01        # 0000 0001

    STATUS_BATTERY_DEAD =       0x04        # 0000 0100
    STATUS_BATTERY_FAULT =      0x08        # 0000 1000
    STATUS_ON_BATTERY =         0x10        # 0001 0000
    STATUS_ON_SOCKET =          0x20        # 0010 0000
    STATUS_RUN =                0x40        # 0100 0000

    STARTUP_POWER_CYCLE =       0x01        # 0000 0001
    STARTUP_WATCHDOG =          0x02        # 0000 0010

    ADDR_CHECK_VALUE =          0x00

    ADDR_POWER_WAIT_MINS =      0x01
    ADDR_POWER_WAIT_SECS =      0x02
    ADDR_POWER_OFF_MINS =       0x03
    ADDR_POWER_OFF_SECS =       0x04

    ADDR_BATTERY_CTRL =         0x05
    ADDR_PCB_CMD_CTRL =         0x06
    ADDR_CMD_CTRL =             0x07

    ADDR_BATTERY_V_MSB =        0x10
    ADDR_BATTERY_V_LSB =        0x11

    ADDR_SOCKET_V_MSB =         0x12
    ADDR_SOCKET_V_LSB =         0x13

    ADDR_RTC_0 =                0x15
    ADDR_RTC_1 =                0x16
    ADDR_RTC_2 =                0x17
    ADDR_RTC_3 =                0x18
    ADDR_RTC_4 =                0x19
    ADDR_RTC_5 =                0x1a
    ADDR_RTC_6 =                0x1b
    ADDR_RTC_7 =                0x1c
    ADDR_RTC_8 =                0x1d
    ADDR_RTC_9 =                0x1e

    ADDR_VERSION =              0x1f

    ADDR_CMD_STATUS =           0x20
    ADDR_PSU_STATUS =           0x21

    ADDR_STARTUP_STATUS =       0x3f

    __ADDR_MASK =               0x3f        # 0111 1111
    __DATA_MASK =               0xff        # 1111 1111


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr


    # ----------------------------------------------------------------------------------------------------------------

    def cmd(self, cmd):                   # TODO: needs timeout!
        self.issue_cmd(cmd)

        while True:
            time.sleep(0.001)       # TODO: for how long?

            busy = self.read_reg(STM32.ADDR_CMD_STATUS) & cmd

            if not busy:
                return


    def issue_cmd(self, cmd):
        addr = self.ADDR_CMD_CTRL & self.__ADDR_MASK

        try:
            I2C.start_tx(self.__addr)
            I2C.write(addr, self.CMD_CLEAR)
            I2C.write(addr, cmd)

        finally:
            I2C.end_tx()


    def read_reg(self, address):
        addr = address & self.__ADDR_MASK

        try:
            I2C.start_tx(self.__addr)
            # byte = I2C.read_cmd(addr, 1)

            I2C.write(addr, 0)
            byte = I2C.read(1)

            return byte
        finally:
            I2C.end_tx()


    def write_reg(self, address, byte):
        addr = address & self.__ADDR_MASK
        value = byte & self.__DATA_MASK

        try:
            I2C.start_tx(self.__addr)
            I2C.write(addr, value)
        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "STM32:{addr:0x%02x}" % self.__addr
