"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU is present, if any

example JSON:
{"model": "MobileV2", "batt-model": "PackV1", "ignore-threshold": true, "reporting-interval": 10}
"""

from scs_core.psu.psu_conf import PSUConf as AbstractPSUConf

from scs_dfe.interface.opcube.opcube_mcu_t1 import OPCubeMCUt1

from scs_dfe.interface.pzhb.pzhb_mcu_t1_f1 import PZHBMCUt1f1
from scs_dfe.interface.pzhb.pzhb_mcu_t2_f1 import PZHBMCUt2f1
from scs_dfe.interface.pzhb.pzhb_mcu_t3_f1 import PZHBMCUt3f1

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.batt_pack.batt_pack_v2 import BattPackV2

from scs_psu.psu.opcube_v1.psu_opcube_v1 import PSUOPCubeV1p0, PSUOPCubeV1p1

from scs_psu.psu.mobile_v1.psu_mobile_v1 import PSUMobileV1
from scs_psu.psu.mobile_v2.psu_mobile_v2 import PSUMobileV2

from scs_psu.psu.oslo_v1.psu_oslo_v1 import PSUOsloV1

from scs_psu.psu.prototype_v1.psu_prototype_v1 import PSUPrototypeV1

from scs_psu.psu.psu_monitor import PSUMonitor


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(AbstractPSUConf):
    """
    classdocs
    """

    __PSU_CLASSES = {
        PSUMobileV1.name():  PSUMobileV1,
        PSUMobileV2.name():  PSUMobileV2,
        PSUOPCubeV1p0.name(): PSUOPCubeV1p0,
        PSUOPCubeV1p1.name(): PSUOPCubeV1p1,
        PSUOsloV1.name(): PSUOsloV1,
        PSUPrototypeV1.name(): PSUPrototypeV1
    }

    @classmethod
    def psu_models(cls):
        return sorted(cls.__PSU_CLASSES.keys())


    __BATT_CLASSES = {
        BattPackV1.name(): BattPackV1,
        BattPackV2.name(): BattPackV2
    }

    @classmethod
    def batt_models(cls):
        return sorted(cls.__BATT_CLASSES.keys())


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return PSUConf(None, None, False, 0)

        psu_model = jdict.get('model')
        batt_model = jdict.get('batt-model')
        ignore_threshold = jdict.get('ignore-threshold', False)

        reporting_interval = jdict.get('reporting-interval')

        return cls(psu_model, batt_model, ignore_threshold, reporting_interval)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, psu_model, batt_model, ignore_threshold, reporting_interval):
        """
        Constructor
        """
        super().__init__(psu_model, batt_model, ignore_threshold, reporting_interval)


    # ----------------------------------------------------------------------------------------------------------------

    def psu(self, host, interface_model):
        if self.psu_model is None:
            return None

        if self.psu_model not in self.__PSU_CLASSES.keys():
            raise ValueError('unknown PSU model: %s' % self.psu_model)

        psu_class = self.__PSU_CLASSES[self.__psu_model]

        batt_class = None if self.__batt_model is None else self.__BATT_CLASSES[self.__batt_model]
        batt_pack = None if batt_class is None else batt_class.construct()

        if self.psu_model == PSUMobileV1.name():
            if interface_model == 'PZHBt1':
                return psu_class(PZHBMCUt1f1(PZHBMCUt1f1.DEFAULT_ADDR))

            if interface_model == 'PZHBt2':
                return psu_class(PZHBMCUt2f1(PZHBMCUt2f1.DEFAULT_ADDR))

            raise ValueError('incompatible interface model for MobileV1: %s' % interface_model)

        if self.psu_model == PSUMobileV2.name():
            if interface_model == 'PZHBt3':
                return psu_class(PZHBMCUt3f1(PZHBMCUt3f1.DEFAULT_ADDR), batt_pack)

            raise ValueError('incompatible interface model for MobileV2: %s' % interface_model)

        if self.psu_model in (PSUOPCubeV1p0.name(), PSUOPCubeV1p1.name()):
            return psu_class(OPCubeMCUt1(OPCubeMCUt1.DEFAULT_ADDR), batt_pack)

        return psu_class(host.psu_device())


    def psu_monitor(self, host, interface_model, ignore_standby):
        psu = self.psu(host, interface_model)

        if psu is None:
            return None

        return PSUMonitor(host, psu, ignore_standby, self.ignore_threshold)


    def psu_class(self):
        if self.psu_model is None:
            return None

        return self.__PSU_CLASSES[self.psu_model]


    def psu_report_class(self):
        if self.psu_model is None:
            return None

        psu_class = self.__PSU_CLASSES[self.psu_model]                 # may raise KeyError

        return psu_class.report_class()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf(psu):{psu_model:%s, batt_model:%s, ignore_threshold:%s, reporting_interval:%s}" % \
               (self.psu_model, self.batt_model, self.ignore_threshold, self.reporting_interval)
