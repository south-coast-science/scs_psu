"""
Created on 29 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ChargerStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = list(str(jdict))

        ready = bool(int(items[0]))
        fault = bool(int(items[1]))
        charging = bool(int(items[2]))
        top_off_charge = bool(int(items[3]))

        return ChargerStatus(ready, fault, charging, top_off_charge)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ready, fault, charging, top_off_charge):
        """
        Constructor
        """
        self.__ready = ready                                # bool
        self.__fault = fault                                # bool
        self.__charging = charging                          # bool
        self.__top_off_charge = top_off_charge              # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        items = (self.ready, self.fault, self.charging, self.top_off_charge)

        item_string = ''.join(['1' if item else '0' for item in items])

        return item_string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ready(self):
        return self.__ready


    @property
    def fault(self):
        return self.__fault


    @property
    def charging(self):
        return self.__charging


    @property
    def top_off_charge(self):
        return self.__top_off_charge


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChargerStatus:{ready:%s, fault:%s, charging:%s, top_off_charge:%s}" % \
               (self.ready, self.fault, self.charging, self.top_off_charge)
