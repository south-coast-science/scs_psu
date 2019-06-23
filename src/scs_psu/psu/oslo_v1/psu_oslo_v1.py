"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The Oslo PSU
"""

import json

from scs_psu.psu.serial_psu import SerialPSU
from scs_psu.psu.oslo_v1.psu_status import PSUStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUOsloV1(SerialPSU):
    """
    South Coast Science PSU v2 (Oslo) via UART
    """

    __BAUD_RATE =               1200


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def baud_rate(cls):
        return PSUOsloV1.__BAUD_RATE


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uart):
        """
        Constructor
        """
        super().__init__(uart)


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        response = self.communicate("state")

        try:
            jdict = json.loads(response)
            return PSUStatus.construct_from_jdict(jdict)

        except ValueError:
            return None


    def construct_status_from_jdict(self, jdict):
        return PSUStatus.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUOsloV1:{serial:%s}" % self._serial
