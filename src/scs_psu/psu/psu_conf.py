"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU board is present, if any

example JSON:
{"model": "OsloV1"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_psu.psu.prototype_v1.psu_prototype_v1 import PSUPrototypeV1
from scs_psu.psu.oslo_v1.psu_oslo_v1 import PSUOsloV1


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
            return PSUConf(None)

        model = jdict.get('model')

        return PSUConf(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        super().__init__()

        self.__model = model


    # ----------------------------------------------------------------------------------------------------------------

    def psu(self, host):
        if self.model is None:
            return None

        if self.model == 'PrototypeV1':
            return PSUPrototypeV1(host.psu_device())

        if self.model == 'OsloV1':
            return PSUOsloV1(host.psu_device())

        raise ValueError('unknown model: %s' % self.model)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf:{model:%s}" % self.model
