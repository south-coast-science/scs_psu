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

    def __init__(self, host, psu):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__host = host
        self.__psu = psu

        self.__shutdown_initiated = False


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def start(self):
        print("PSUMonitor.start", file=sys.stderr)
        sys.stderr.flush()

        try:
            self.__psu.open()
            super().start()

        except KeyboardInterrupt:
            pass


    def stop(self):
        print("PSUMonitor.stop", file=sys.stderr)
        sys.stderr.flush()

        try:
            super().stop()
            self.__psu.close()

        except (BrokenPipeError, KeyboardInterrupt):
            pass


    def run(self):
        print("PSUMonitor.run", file=sys.stderr)
        sys.stderr.flush()

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
                if status.standby:
                    self.__enter_host_shutdown("standby")

                if status.below_power_threshold():
                    self.__enter_host_shutdown("below power threshold")

        except (BrokenPipeError, KeyboardInterrupt):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess special operations...

    def __enter_host_shutdown(self, reason):
        if self.__shutdown_initiated:
            return

        # TODO: test whether the message queue is empty

        self.__psu.host_shutdown_initiated()

        self.__shutdown_initiated = True

        print("PSUMonitor: %s: entering shutdown" % reason, file=sys.stderr)
        sys.stderr.flush()

        self.__host.shutdown()


    # ----------------------------------------------------------------------------------------------------------------
    # data retrieval for client process...

    def firmware(self):
        return self.__psu.version()


    def sample(self):
        with self._lock:
            status = self.__psu.construct_status_from_jdict(OrderedDict(self._value))

        return status


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        host_name = None if self.__host is None else self.__host.name()

        return "PSUMonitor:{value:%s, host:%s, psu:%s, shutdown_initiated:%s}" % \
               (self._value, host_name, self.__psu, self.__shutdown_initiated)
