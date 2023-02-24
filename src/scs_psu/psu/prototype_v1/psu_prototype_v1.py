"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The prototype PSU
"""

import json

from scs_psu.psu.serial_psu import SerialPSU
from scs_psu.psu.prototype_v1.psu_status import PSUStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUPrototypeV1(SerialPSU):
    """
    South Coast Science PSU v1 (prototype) via UART
    """

    __BAUD_RATE =               1200

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def name(cls):
        return 'PrototypeV1'


    @classmethod
    def report_class(cls):
        return PSUStatus


    @classmethod
    def baud_rate(cls):
        return PSUPrototypeV1.__BAUD_RATE


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uart):
        """
        Constructor
        """
        super().__init__(uart)


    # ----------------------------------------------------------------------------------------------------------------

    def status(self):
        response = self.communicate("state")

        if response is None:
            return PSUStatus.null_datum()

        try:
            jdict = json.loads(response)
            return PSUStatus.construct_from_jdict(jdict)

        except (TypeError, ValueError):
            return None


    def charge_min(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def batt_pack(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUPrototypeV1:{serial:%s}" % self._serial
