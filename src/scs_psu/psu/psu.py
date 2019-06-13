"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract PSU
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class PSU(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def open(self):
        pass


    @abstractmethod
    def close(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def status(self):
        pass


    @abstractmethod
    def construct_status_from_jdict(self, jdict):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def version(self):
        pass


    @abstractmethod
    def uptime(self):
        pass


    @abstractmethod
    def do_not_resuscitate(self, enable):
        pass


    @abstractmethod
    def watchdog_start(self, interval):
        pass


    @abstractmethod
    def watchdog_stop(self):
        pass


    @abstractmethod
    def watchdog_touch(self):
        pass


    @abstractmethod
    def charge_pause(self, on):
        pass


    @abstractmethod
    def charge_dead(self, on):
        pass
