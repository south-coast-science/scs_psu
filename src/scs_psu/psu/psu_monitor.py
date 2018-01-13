"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

class PSUMonitor(SynchronisedProcess):
    """
    classdocs
    """
    __MONITOR_INTERVAL =        2.0             # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, psu):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__psu = psu
        self.__shutdown_initiated = False


    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        try:
            timer = IntervalTimer(self.__MONITOR_INTERVAL)

            while timer.true():
                status = self.__psu.status()

                if status is None:
                    print("PSUMonitor.run: got None", sys.stderr)
                    continue

                # report...
                with self._lock:
                    status.as_list(self._value)

                # act...
                if status.link_in:
                    self.__shutdown()

        except KeyboardInterrupt:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    def __shutdown(self):
        if self.__shutdown_initiated:
            return

        self.__shutdown_initiated = True
        print("SHUTDOWN!", file=sys.stdout)


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            self.__psu.open()
            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        try:
            super().stop()
            self.__psu.close()

        except KeyboardInterrupt:
            pass


    def sample(self):
        with self._lock:
            value = self._value

        return self.__psu.construct_status_from_jdict(OrderedDict(value))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUMonitor:{value:%s, psu:%s, shutdown_initiated:%s}" % \
               (self._value, self.__psu, self.__shutdown_initiated)
