"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import sys

from abc import abstractmethod
from collections import OrderedDict

from scs_host.sys.host_serial import HostSerial

from scs_core.psu.psu_uptime import PSUUptime
from scs_core.psu.psu_version import PSUVersion


# --------------------------------------------------------------------------------------------------------------------

class PSU(object):
    """
    South Coast Science PSU via UART
    """

    __BAUD_RATE =               1200

    __EOL =                     "\n"

    __SERIAL_LOCK_TIMEOUT =     6.0         # seconds
    __SERIAL_COMMS_TIMEOUT =    4.0         # seconds


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uart):
        """
        Constructor
        """
        self._serial = HostSerial(uart, self.__BAUD_RATE, False)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def status(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        response = self.communicate("version")

        try:
            jdict = json.loads(response, object_pairs_hook=OrderedDict)
            return PSUVersion.construct_from_jdict(jdict)

        except ValueError:
            return None


    def uptime(self):
        response = self.communicate("uptime")

        try:
            jdict = json.loads(response, object_pairs_hook=OrderedDict)
            return PSUUptime.construct_from_jdict(jdict)

        except ValueError:
            return None


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
        print("PSU.communicate - command:%s" % command, file=sys.stderr)

        try:
            self._serial.open(self.__SERIAL_LOCK_TIMEOUT, self.__SERIAL_COMMS_TIMEOUT)

            length = self._serial.write_line(command.strip(), self.__EOL)
            response = self._serial.read_line(self.__EOL, self.__SERIAL_COMMS_TIMEOUT)

            print("PSU.communicate - sent:%d response:%s" % (length, response), file=sys.stderr)

            return response

        finally:
            self._serial.close()
