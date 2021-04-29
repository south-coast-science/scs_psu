"""
Created on 25 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

From Max17055 Software Implementation Guide p12:

    # designCap = 0x1450
    # ichgterm = 0x333
    # modelcfg = 0x8000
    # QRTable00 = 0x1050
    # QRTable10 = 0x2012
    # VEmpty = 0xa561
    # RCOMP0 = 0x004d
    # TempCo = 0x223e
"""

from abc import ABC, abstractmethod

from scs_psu.batt_pack.fuel_gauge.max17055.max17055 import Max17055
from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import Max17055Params


# --------------------------------------------------------------------------------------------------------------------

class BattPack(ABC):
    """
    classdocs
    """

    @staticmethod
    @abstractmethod
    def name():
        pass


    @staticmethod
    @abstractmethod
    def gauge_conf():
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def charge_min(cls):
        pass


    @classmethod
    @abstractmethod
    def default_params(cls):
        pass


    @classmethod
    def param_save_interval(cls):
        return Max17055.param_save_interval()


    @classmethod
    def construct(cls):
        conf = cls.gauge_conf()
        gauge = Max17055(conf)

        return cls(gauge)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, gauge):
        """
        Constructor
        """
        self.__gauge = gauge


    # ----------------------------------------------------------------------------------------------------------------

    def initialise(self, host, force_config=False):
        try:
            if not self.__gauge.read_power_on_reset() and not force_config:
                return None

            params = Max17055Params.load(host)

            if params is None:
                params = self.default_params()

            self.__gauge.initialise_as_github(force_config=force_config)    # was initialise
            self.__gauge.write_params(params)
            self.__gauge.clear_power_on_reset()

            return params

        except OSError:
            return None


    def read_learned_params(self):
        try:
            return self.__gauge.read_learned_params()
        except OSError:
            return None


    def write_params(self, params: Max17055Params):
        try:
            self.__gauge.write_params(params)
            return True

        except OSError:
            return False


    def sample(self):
        try:
            return self.__gauge.sample()
        except OSError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cycles(self):
        try:
            return self.__gauge.read_learned_params().cycles
        except OSError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{gauge:%s}" %  self.__gauge
