"""
Created on 13 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract PSU
"""

import json

from abc import abstractmethod

from scs_core.psu.psu_uptime import PSUUptime
from scs_core.psu.psu_version import PSUVersion

from scs_host.sys.host_serial import HostSerial

from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

class SerialPSU(PSU):
    """
    South Coast Science PSU via UART
    """

    __EOL =                     "\n"

    __SERIAL_LOCK_TIMEOUT =     6.0         # seconds
    __SERIAL_COMMS_TIMEOUT =    4.0         # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uart):
        """
        Constructor
        """
        self._serial = HostSerial(uart, self.baud_rate(), False)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def baud_rate(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        self._serial.open(self.__SERIAL_LOCK_TIMEOUT, self.__SERIAL_COMMS_TIMEOUT)


    def close(self):
        self._serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        response = self.communicate("version")

        try:
            jdict = json.loads(response)
            return PSUVersion.construct_from_jdict(jdict)

        except ValueError:
            return None


    def uptime(self):
        response = self.communicate("uptime")

        try:
            jdict = json.loads(response)
            return PSUUptime.construct_from_jdict(jdict)

        except ValueError:
            return None


    def host_shutdown_initiated(self):
        response = self.communicate("dnr %d" % 1)

        return response


    def do_not_resuscitate(self, enable):
        param = 1 if bool(enable) else 0
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


    # ----------------------------------------------------------------------------------------------------------------

    def communicate(self, command):
        self._serial.write_line(command.strip(), self.__EOL)
        response = self._serial.read_line(self.__EOL, self.__SERIAL_COMMS_TIMEOUT)

        return response