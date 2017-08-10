"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_host.sys.host_serial import HostSerial

from scs_psu.psu.psu_status import PSUStatus
from scs_psu.psu.psu_uptime import PSUUptime
from scs_psu.psu.psu_version import PSUVersion


# --------------------------------------------------------------------------------------------------------------------

class PSU(object):
    """
    South Coast Science PSU v1.0.0 via UART
    """

    __UART =                5
    __BAUD_RATE =           9600

    __SERIAL_TIMEOUT =      3.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__serial = HostSerial(PSU.__UART, PSU.__BAUD_RATE, False)


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        response = self.communicate("version")
        jdict = json.loads(response, object_pairs_hook=OrderedDict)

        return PSUVersion.construct_from_jdict(jdict)


    def status(self):
        response = self.communicate("status")
        jdict = json.loads(response, object_pairs_hook=OrderedDict)

        return PSUStatus.construct_from_jdict(jdict)


    def uptime(self):
        response = self.communicate("uptime")
        jdict = json.loads(response, object_pairs_hook=OrderedDict)

        return PSUUptime.construct_from_jdict(jdict)


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
        # TODO: implement charge_pause(..)
        pass


    def charge_dead(self, on):
        # TODO: implement charge_dead(..)
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def communicate(self, command):
        try:
            self.__serial.open(PSU.__SERIAL_TIMEOUT)

            self.__serial.write_line(command.strip())
            response = self.__serial.read_line("\r\n", PSU.__SERIAL_TIMEOUT)

            return response

        finally:
            self.__serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSU:{serial:%s}" % self.__serial
