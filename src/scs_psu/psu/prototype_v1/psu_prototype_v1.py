"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The prototype PSU
"""

import json

from collections import OrderedDict

from scs_psu.psu.psu import PSU
from scs_psu.psu.prototype_v1.psu_status import PSUStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUPrototypeV1(PSU):
    """
    South Coast Science PSU v1 (prototype) via UART
    """

    __BAUD_RATE =               1200

    # ----------------------------------------------------------------------------------------------------------------

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

        try:
            jdict = json.loads(response, object_pairs_hook=OrderedDict)
            return PSUStatus.construct_from_jdict(jdict)

        except ValueError:
            return None


    def construct_status_from_jdict(self, jdict):
        return PSUStatus.construct_from_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUPrototypeV1:{serial:%s}" % self._serial
