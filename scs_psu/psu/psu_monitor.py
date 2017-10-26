"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.psu.psu_status import PSUStatus

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

class PSUMonitor(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, psu):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__psu = psu


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        try:
            timer = IntervalTimer(60)         # self.__conf.sample_period

            while timer.true():
                datum = self.__psu.status()

                with self._lock:
                    datum.as_list(self._value)

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def sample(self):
        with self._lock:
            value = self._value

        return PSUStatus.construct_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUMonitor:{sample:%s, psu:%s}" % (self.sample(), self.__psu)
