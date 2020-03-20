"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which PSU board is present, if any

example JSON:
{"model": "OsloV1", "reporting-interval": 10, "report-file": "/tmp/southcoastscience/psu_report.json"}
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable

from scs_dfe.interface.pzhb.pzhb_mcu_t1_f1 import PZHBMCUt1f1
from scs_dfe.interface.pzhb.pzhb_mcu_t2_f1 import PZHBMCUt2f1

from scs_psu.psu.mobile_v1.psu_mobile_v1 import PSUMobileV1
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


    __MODELS = {
        PSUMobileV1.name():  PSUMobileV1,
        PSUOsloV1.name(): PSUOsloV1,
        PSUPrototypeV1.name(): PSUPrototypeV1
    }

    @classmethod
    def models(cls):
        return sorted(cls.__MODELS.keys())


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return PSUConf(None, None, None)

        model = jdict.get('model')
        reporting_interval = jdict.get('reporting-interval')
        report_file = jdict.get('report-file')

        return PSUConf(model, reporting_interval, report_file)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, reporting_interval, report_file):
        """
        Constructor
        """
        self.__model = model
        self.__reporting_interval = Datum.int(reporting_interval)
        self.__report_file = report_file


    # ----------------------------------------------------------------------------------------------------------------

    def psu(self, host, interface_model):
        if self.model is None:
            return None

        if self.model not in self.__MODELS.keys():
            raise ValueError('unknown psu model: %s' % self.model)

        psu_class = self.__MODELS[self.__model]

        if self.model == PSUMobileV1.name():
            if interface_model == 'PZHBt1':
                return psu_class(PZHBMCUt1f1(PZHBMCUt1f1.DEFAULT_ADDR))

            if interface_model == 'PZHBt2':
                return psu_class(PZHBMCUt2f1(PZHBMCUt2f1.DEFAULT_ADDR))

            raise ValueError('incompatible interface model for MobileV1: %s' % interface_model)

        return psu_class(host.psu_device())


    def psu_monitor(self, host, interface_model, auto_shutdown):
        psu = self.psu(host, interface_model)

        if psu is None:
            return None

        return PSUMonitor(host, psu, auto_shutdown)


    def psu_report_class(self):
        psu_class = self.__MODELS[self.__model]                 # may raise KeyError

        return psu_class.report_class()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def report_file(self):
        return self.__report_file


    @property
    def reporting_interval(self):
        return self.__reporting_interval


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model
        jdict['reporting-interval'] = self.__reporting_interval
        jdict['report-file'] = self.__report_file

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUConf:{model:%s, reporting_interval:%s, report_file:%s}" % \
               (self.model, self.reporting_interval, self.report_file)
