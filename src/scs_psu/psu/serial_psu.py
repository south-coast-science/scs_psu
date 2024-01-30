"""
Created on 13 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract PSU that communicates over a UART
"""

import json

from abc import abstractmethod

from scs_core.psu.psu import PSU
from scs_core.psu.psu_uptime import PSUUptime
from scs_core.psu.psu_version import PSUVersion

from scs_core.sys.logging import Logging

from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class SerialPSU(PSU):
    """
    South Coast Science PSU via UART
    """

    __EOL =                     "\n"

    __SERIAL_LOCK_TIMEOUT =     6.0         # seconds
    __SERIAL_COMMS_TIMEOUT =    2.0         # seconds


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def requires_interface(cls):
        return False


    @classmethod
    def uses_batt_pack(cls):
        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uart):
        """
        Constructor
        """
        self._serial = HostSerial(uart, self.baud_rate())
        self._logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def baud_rate(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        pass


    def close(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def communicate(self, command):
        try:
            self._serial.open(self.__SERIAL_LOCK_TIMEOUT, self.__SERIAL_COMMS_TIMEOUT)

            try:
                self._serial.write_line(command.strip(), self.__EOL)
            except AttributeError as ex:
                self._logger.error("write_line: %s" % repr(ex))
                return None

            try:
                return self._serial.read_line(eol=self.__EOL, timeout=self.__SERIAL_COMMS_TIMEOUT)
            except TimeoutError as ex:
                self._logger.error("read_line: %s" % repr(ex))
                return None

        finally:
            self._serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        response = self.communicate("version")

        try:
            jdict = json.loads(response)
            return PSUVersion.construct_from_jdict(jdict)

        except (TypeError, ValueError):
            return None


    def uptime(self):
        response = self.communicate("uptime")

        try:
            jdict = json.loads(response)
            return PSUUptime.construct_from_jdict(jdict)

        except (TypeError, ValueError):
            return None


    def host_shutdown_initiated(self):
        response = self.communicate("dnr %d" % 1)

        return response


    def do_not_resuscitate(self, on):
        param = 1 if bool(on) else 0
        response = self.communicate("dnr %d" % param)

        return response


    def watchdog_start(self, interval):
        response = self.communicate("w-start % d" % interval)

        return response


    def watchdog_stop(self):
        response = self.communicate("w-stop")

        return response


    def watchdog_touch(self):
        response = self.communicate("w-touch")

        return response


    def charge_pause(self, on):
        state = 1 if bool(on) else 0
        response = self.communicate("c-pause % d" % state)

        return response


    def charge_dead(self, on):
        state = 1 if bool(on) else 0
        response = self.communicate("c-dead % d" % state)

        return response


    def power_peripherals(self, on):
        pass
