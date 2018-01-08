"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_psu.psu.psu import PSU
from scs_psu.psu.v1.psu_status import PSUStatus


# --------------------------------------------------------------------------------------------------------------------

class PSUv1(PSU):
    """
    South Coast Science PSU v1 (prototype) via UART
    """

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUv1:{serial:%s}" % self._serial
