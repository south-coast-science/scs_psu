"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU is present, if any

example JSON:
{"model": "MobileV2", "batt-model": "PackV1", "ignore-threshold": true, "reporting-interval": 10,
"report-file": "/tmp/southcoastscience/psu_status_report.json"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_dfe.interface.pzhb.pzhb_mcu_t1_f1 import PZHBMCUt1f1
from scs_dfe.interface.pzhb.pzhb_mcu_t2_f1 import PZHBMCUt2f1
from scs_dfe.interface.pzhb.pzhb_mcu_t3_f1 import PZHBMCUt3f1

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1

from scs_psu.psu.mobile_v1.psu_mobile_v1 import PSUMobileV1
from scs_psu.psu.mobile_v2.psu_mobile_v2 import PSUMobileV2

from scs_psu.psu.oslo_v1.psu_oslo_v1 import PSUOsloV1
from scs_psu.psu.prototype_v1.psu_prototype_v1 import PSUPrototypeV1

from scs_psu.psu.psu_monitor import PSUMonitor


# --------------------------------------------------------------------------------------------------------------------

class PSUConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "psu_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    __PSU_CLASSES = {
        PSUMobileV1.name():  PSUMobileV1,
        PSUMobileV2.name():  PSUMobileV2,
        PSUOsloV1.name(): PSUOsloV1,
        PSUPrototypeV1.name(): PSUPrototypeV1
    }

    @classmethod
    def psu_models(cls):
        return sorted(cls.__PSU_CLASSES.keys())


    __BATT_CLASSES = {
        BattPackV1.name():  BattPackV1
    }

    @classmethod
    def batt_models(cls):
        return sorted(cls.__BATT_CLASSES.keys())


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return PSUConf(None, None, False, 0, None)

        psu_model = jdict.get('model')
        batt_model = jdict.get('batt-model')
        ignore_threshold = jdict.get('ignore-threshold', False)

        reporting_interval = jdict.get('reporting-interval')
        report_file = jdict.get('report-file')

        return PSUConf(psu_model, batt_model, ignore_threshold, reporting_interval, report_file)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, psu_model, batt_model, ignore_threshold, reporting_interval, report_file):
        """
        Constructor
        """
        self.__psu_model = psu_model                                        # string
        self.__batt_model = batt_model                                      # string
        self.__ignore_threshold = ignore_threshold                          # bool

        self.__reporting_interval = int(reporting_interval)                 # int
        self.__report_file = report_file                                    # string


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

        return psu_class(host.psu_device())


    def psu_monitor(self, host, interface_model, ignore_standby):
        psu = self.psu(host, interface_model)

        if psu is None:
            return None

        return PSUMonitor(host, psu, ignore_standby, self.__ignore_threshold)


    def psu_class(self):
        if self.__psu_model is None:
            return None

        return self.__PSU_CLASSES[self.__psu_model]


    def psu_report_class(self):
        if self.__psu_model is None:
            return None

        psu_class = self.__PSU_CLASSES[self.__psu_model]                 # may raise KeyError

        return psu_class.report_class()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def psu_model(self):
        return self.__psu_model


    @property
    def batt_model(self):
        return self.__batt_model


    @property
    def ignore_threshold(self):
        return self.__ignore_threshold


    @property
    def report_file(self):
        return self.__report_file


    @property
    def reporting_interval(self):
        return self.__reporting_interval


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__psu_model
        jdict['batt-model'] = self.__batt_model
        jdict['ignore-threshold'] = self.__ignore_threshold

        jdict['reporting-interval'] = self.__reporting_interval
        jdict['report-file'] = self.__report_file

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf:{psu_model:%s, batt_model:%s, ignore_threshold:%s, reporting_interval:%s, report_file:%s}" % \
               (self.psu_model, self.batt_model, self.ignore_threshold, self.reporting_interval, self.report_file)
