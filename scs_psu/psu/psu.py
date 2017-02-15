"""
Created on 10 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_psu.psu.stm32 import STM32


# --------------------------------------------------------------------------------------------------------------------

class PSU(object):
    """
    STM32 32-Bit ARM Cortex-M Microcontroller
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__mcu = STM32()


    # ----------------------------------------------------------------------------------------------------------------

    def power_cycle(self, wait_secs, off_secs):
        self.__mcu.open()

        try:
            self.__mcu.write_reg(STM32.ADDR_POWER_WAIT_SECS, wait_secs)
            self.__mcu.write_reg(STM32.ADDR_POWER_OFF_SECS, off_secs)

            self.__mcu.cmd(STM32.CMD_POWER_CYCLE)

        finally:
            self.__mcu.close()


    def reset_watchdog(self):
        self.__mcu.open()

        try:
            self.__mcu.cmd(STM32.CMD_WATCHDOG_RESET)

        finally:
            self.__mcu.close()


    def set_rtc(self, datetime):
        self.__mcu.open()

        try:
            print(datetime)

            # TODO: load registers

            self.__mcu.cmd(STM32.CMD_RTC_SET)

        finally:
            self.__mcu.close()


    def run_rtc(self):
        self.__mcu.open()

        try:
            self.__mcu.cmd(STM32.CMD_RTC_RUN)

        finally:
            self.__mcu.close()


    def get_power(self):
        self.__mcu.open()

        try:
            self.__mcu.cmd(STM32.CMD_ADC_READ)

            socket_msb = self.__mcu.read_reg(STM32.ADDR_SOCKET_V_MSB)
            socket_lsb = self.__mcu.read_reg(STM32.ADDR_SOCKET_V_LSB)

            socket = socket_msb << 8 | socket_lsb

            battery_msb = self.__mcu.read_reg(STM32.ADDR_BATTERY_V_MSB)
            battery_lsb = self.__mcu.read_reg(STM32.ADDR_BATTERY_V_LSB)

            battery = battery_msb << 8 | battery_lsb

            return socket, battery

        finally:
            self.__mcu.close()


    def get_version(self):
        self.__mcu.open()

        try:
            version = self.__mcu.read_reg(STM32.ADDR_VERSION)

            software_version = version >> 4
            hardware_version = version & 0x0f

            return software_version, hardware_version

        finally:
            self.__mcu.close()


    def get_psu_status(self):
        pass


    def get_startup_status(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSU:{mcu:%s}" % self.__mcu
