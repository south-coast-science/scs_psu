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


# TODO: subclass according to the version reported by the actual PSU

# --------------------------------------------------------------------------------------------------------------------

class PSU(object):
    """
    South Coast Science PSU v1 (firmware v1.1.x) via UART
    """

    __BAUD_RATE =           1200

    __EOL =                 "\n"

    __SERIAL_TIMEOUT =      3.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device):
        """
        Constructor
        """
        self.__device = device


    # ----------------------------------------------------------------------------------------------------------------

    def version(self):
        response = self.communicate("version")

        try:
            jdict = json.loads(response, object_pairs_hook=OrderedDict)
            return PSUVersion.construct_from_jdict(jdict)

        except ValueError:
            return None


    def status(self):
        response = self.communicate("status")

        try:
            jdict = json.loads(response, object_pairs_hook=OrderedDict)
            return PSUStatus.construct_from_jdict(jdict)

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
        ser = None

        try:
            ser = HostSerial(self.__device, PSU.__BAUD_RATE, False)

            ser.open(PSU.__SERIAL_TIMEOUT)

            ser.write_line(command.strip(), PSU.__EOL)
            response = ser.read_line(PSU.__EOL, PSU.__SERIAL_TIMEOUT)

            return response

        finally:
            if ser:
                ser.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSU:{device:%s}" % self.__device
