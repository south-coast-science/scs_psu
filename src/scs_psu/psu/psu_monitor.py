"""
Created on 25 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

shutdown warning:
Please retry operation after closing inhibitors and logging out other users.
Alternatively, ignore inhibitors and users with 'systemctl poweroff -i'.
"""

import sys
import time

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

    def __init__(self, host, psu: PSU, ignore_standby, ignore_threshold):
        """
        Constructor
        """
        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self.__host = host                                                  # Host
        self.__psu = psu                                                    # PSU

        self.__ignore_standby = ignore_standby                              # bool
        self.__ignore_threshold = ignore_threshold                          # bool

        self.__shutdown_initiated = False
        self.__prev_charge = None
        self.__prev_params = None


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

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    def run(self):
        # initialise fuel guage...
        batt_pack = self.__psu.batt_pack

        if batt_pack is not None:
            params = batt_pack.initialise(self.__host, force_config=False)

            if params:
                print("PSUMonitor.run: battery pack initialised: %s" % params, file=sys.stderr)
                sys.stderr.flush()

        # monitor PSU...
        try:
            timer = IntervalTimer(self.__MONITOR_INTERVAL)

            while timer.true():
                status = self.__psu.status()

                if status is None:
                    continue

                # report...
                with self._lock:
                    status.as_list(self._value)

                # fuel gauge...
                self.__save_fuel_gauge_params(batt_pack)

                # shutdown...
                if not self.__ignore_standby and status.standby:
                    self.__enter_host_shutdown("STANDBY")

                if not self.__ignore_threshold and status.below_power_threshold(self.__psu.charge_min()):
                    self.__enter_host_shutdown("BELOW POWER THRESHOLD")

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------
    # process special operations...

    def __save_fuel_gauge_params(self, batt_pack):
        if batt_pack is None:
            return

        params = batt_pack.read_learned_params()

        if self.__prev_params is not None and params == self.__prev_params:
            return

        params.save(self.__host)
        self.__prev_params = params

        print("PSUMonitor: %s" % params, file=sys.stderr)
        sys.stderr.flush()


    def __enter_host_shutdown(self, reason):
        if self.__shutdown_initiated:
            return

        print("PSUMonitor.enter_host_shutdown: %s" % reason, file=sys.stderr)
        sys.stderr.flush()

        self.__psu.host_shutdown_initiated()
        self.__shutdown_initiated = True

        self.__psu.power_peripherals(False)

        time.sleep(2.0)                         # allow reporting to be completed

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

        return "PSUMonitor:{value:%s, host:%s, psu:%s, ignore_standby:%s, ignore_threshold:%s, prev_charge:%s, " \
               "shutdown_initiated:%s}" % \
               (self._value, host_name, self.__psu, self.__ignore_standby, self.__ignore_threshold, self.__prev_charge,
                self.__shutdown_initiated)
