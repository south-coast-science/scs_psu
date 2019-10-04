"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU board is present, if any

example JSON:
{"model": "OsloV1"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1


# --------------------------------------------------------------------------------------------------------------------

class BattPackConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "batt_pack_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    __MODELS = [
        'V1'
    ]

    @classmethod
    def models(cls):
        return cls.__MODELS


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return BattPackConf(None)

        model = jdict.get('model')

        return BattPackConf(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        super().__init__()

        self.__model = model


    # ----------------------------------------------------------------------------------------------------------------

    def fuel_gauge(self, host):
        if self.model is None:
            return None

        if self.model == 'V1':
            return BattPackV1(host)

        raise ValueError('unknown battery pack model: %s' % self.model)


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
        return "BattPackConf:{model:%s}" % self.model
