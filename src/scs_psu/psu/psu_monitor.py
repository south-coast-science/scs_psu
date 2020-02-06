"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from collections import OrderedDict
from multiprocessing import Manager

from scs_core.psu.psu import PSU

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess


# --------------------------------------------------------------------------------------------------------------------

class PSUMonitor(SynchronisedProcess):
    """
    classdocs
    """
    __MONITOR_INTERVAL =        1.0             # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, psu: PSU, auto_shutdown):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__host = host
        self.__psu = psu
        self.__auto_shutdown = auto_shutdown

        self.__shutdown_initiated = False


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

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

        except (BrokenPipeError, KeyboardInterrupt, SystemExit):
            pass


    def run(self):
        try:
            timer = IntervalTimer(self.__MONITOR_INTERVAL)

            while timer.true():
                status = self.__psu.status()

                if status is None:
                    continue

                # report...
                with self._lock:
                    status.as_list(self._value)

                # monitor...
                if not self.__auto_shutdown:
                    continue

                if status.standby:
                    self.__enter_host_shutdown("standby")

                # if status.below_power_threshold():                            # TODO: use fuel gauge when available
                #     self.__enter_host_shutdown("below power threshold")

        except (BrokenPipeError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # process special operations...

    def __enter_host_shutdown(self, reason):
        if self.__shutdown_initiated:
            return

        print("PSUMonitor.enter_host_shutdown: %s" % reason, file=sys.stderr)
        sys.stderr.flush()

        self.__psu.host_shutdown_initiated()
        self.__shutdown_initiated = True

        self.__host.shutdown()


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def firmware(self):
        return self.__psu.version()


    def sample(self):
        with self._lock:
            status = self.__psu.report_class().construct_from_jdict(OrderedDict(self._value))

        return status


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        host_name = None if self.__host is None else self.__host.name()

        return "PSUMonitor:{value:%s, host:%s, psu:%s, auto_shutdown:%s, shutdown_initiated:%s}" % \
               (self._value, host_name, self.__psu, self.__auto_shutdown, self.__shutdown_initiated)
