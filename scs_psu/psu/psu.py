"""
Created on 10 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.lock.lock import Lock
from scs_psu.psu.stm32 import STM32


# --------------------------------------------------------------------------------------------------------------------

class PSU(object):
    """
    STM32 32-Bit ARM Cortex-M Microcontroller
    """

    __LOCK =                    "CMD"
    __LOCK_TIMEOUT =            2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return cls.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__mcu = STM32()


    # ----------------------------------------------------------------------------------------------------------------

    def power_cycle(self, wait_secs, off_secs):
        Lock.acquire(PSU.__lock_name(PSU.__LOCK), PSU.__LOCK_TIMEOUT)

        try:
            self.__mcu.write_reg(STM32.ADDR_POWER_WAIT_SECS, wait_secs)
            self.__mcu.write_reg(STM32.ADDR_POWER_OFF_SECS, off_secs)

            self.__mcu.cmd(STM32.CMD_POWER_CYCLE)

        finally:
            Lock.release(PSU.__lock_name(PSU.__LOCK))


    def reset_watchdog(self):
        Lock.acquire(PSU.__lock_name(PSU.__LOCK), PSU.__LOCK_TIMEOUT)

        try:
            self.__mcu.issue_cmd(STM32.CMD_WATCHDOG_RESET)

        finally:
            Lock.release(PSU.__lock_name(PSU.__LOCK))


    def set_rtc(self, datetime):
        Lock.acquire(PSU.__lock_name(PSU.__LOCK), PSU.__LOCK_TIMEOUT)

        try:
            print(datetime)

            # TODO: load registers

            self.__mcu.issue_cmd(STM32.CMD_RTC_SET)

        finally:
            Lock.release(PSU.__lock_name(PSU.__LOCK))


    def run_rtc(self):
        Lock.acquire(PSU.__lock_name(PSU.__LOCK), PSU.__LOCK_TIMEOUT)

        try:
            self.__mcu.issue_cmd(STM32.CMD_RTC_RUN)

        finally:
            Lock.release(PSU.__lock_name(PSU.__LOCK))


    def get_power(self):
        Lock.acquire(PSU.__lock_name(PSU.__LOCK), PSU.__LOCK_TIMEOUT)

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
            Lock.release(PSU.__lock_name(PSU.__LOCK))


    def get_version(self):
        Lock.acquire(PSU.__lock_name(PSU.__LOCK), PSU.__LOCK_TIMEOUT)

        try:
            version = self.__mcu.read_reg(STM32.ADDR_VERSION)

            software_version = version >> 4
            hardware_version = version & 0x0f

            return software_version, hardware_version

        finally:
            Lock.release(PSU.__lock_name(PSU.__LOCK))


    def get_psu_status(self):
        pass


    def get_startup_status(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSU:{mcu:%s}" % self.__mcu
