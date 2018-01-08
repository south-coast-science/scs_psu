"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not a PSU is present

example JSON:
{"present": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_psu.psu.v1.psu_v1 import PSUv1
from scs_psu.psu.v2.psu_v2 import PSUv2


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "psu_conf.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return PSUConf(False)

        present = jdict.get('present')

        return PSUConf(present)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, present):
        """
        Constructor
        """
        super().__init__()

        self.__present = bool(present)


    # ----------------------------------------------------------------------------------------------------------------

    def psu(self, host):                # TODO: select model of PSU
        if not self.present:
            return None

        return PSUv1(host.psu_device())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def present(self):
        return self.__present


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['present'] = self.present

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf:{present:%s}" %  self.present
