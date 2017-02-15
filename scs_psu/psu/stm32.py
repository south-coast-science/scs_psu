"""
Created on 15 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://beaglebone.cameon.net/home/serial-ports-uart
"""

from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class STM32(object):
    """
    STM32 32-Bit ARM Cortex-M Microcontroller
    """

    MODE_READ =                 0x52
    MODE_WRITE =                0x57

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

    __UART =                    5
    __BAUD_RATE =               115200

    __SERIAL_TIMEOUT =          2.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__serial = HostSerial(self.__UART, self.__BAUD_RATE, False)


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        self.__serial.open(self.__SERIAL_TIMEOUT)


    def close(self):
        self.__serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def cmd(self, command):
        self.write_reg(self.ADDR_CMD_CTRL, self.CMD_CLEAR)
        self.write_reg(self.ADDR_CMD_CTRL, command)


    def read_reg(self, addr):
        self.__serial.write_chars(self.MODE_READ, addr)
        chars = self.__serial.read_chars(1)

        return int(chars[0])


    def write_reg(self, addr, char):
        self.__serial.write_chars(self.MODE_WRITE, addr, char)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "STM32:{serial:%s}" % self.__serial
