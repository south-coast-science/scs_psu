"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.psu.psu_status import PSUStatus
from scs_core.psu.psu_uptime import PSUUptime
from scs_core.psu.psu_version import PSUVersion

from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class PSU(object):
    """
    South Coast Science PSU v1.0.0 via UART
    """

    __BAUD_RATE =           1200

    __SERIAL_TIMEOUT =      4.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device):
        """
        Constructor
        """
        self.__device = device


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
        state = 1 if bool(on) else 0
        response = self.communicate("c-pause % d" % state)

        return response


    def charge_dead(self, on):
        state = 1 if bool(on) else 0
        response = self.communicate("c-dead % d" % state)

        return response


    # ----------------------------------------------------------------------------------------------------------------

    def communicate(self, command):
        ser = None

        try:
            ser = HostSerial(self.__device, PSU.__BAUD_RATE, False)

            ser.open(PSU.__SERIAL_TIMEOUT)

            ser.write_line(command.strip())
            response = ser.read_line("\r\n", PSU.__SERIAL_TIMEOUT)

            return response

        finally:
            if ser:
                ser.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSU:{device:%s}" % self.__device
