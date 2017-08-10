"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies whether on not a PSU is present

example JSON:
{"present": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "psu_conf.json"

    @classmethod
    def filename(cls, host):
        return host.conf_dir() + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


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
        self.__present = bool(present)


    # ----------------------------------------------------------------------------------------------------------------

    def psu(self, host):
        if not self.present:
            return None

        return PSU(host.psu_device())


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


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
