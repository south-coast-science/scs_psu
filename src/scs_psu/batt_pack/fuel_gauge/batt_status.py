"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class BattStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        input_power_present = jdict.get('in')

        charge = ChargeLevel.construct_from_jdict(jdict.get('chrg'))

        tte = Timedelta.construct_from_jdict(jdict.get('tte'))
        ttf = Timedelta.construct_from_jdict(jdict.get('ttf'))

        v = jdict.get('v')
        current = jdict.get('curr')
        temperature = jdict.get('g-tmp')

        capacity = jdict.get('cap')
        cycles = jdict.get('cyc')

        return cls(input_power_present, charge, tte, ttf, v, current, temperature, capacity, cycles)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, input_power_present, charge, tte, ttf, v, current, temperature, capacity, cycles):
        """
        Constructor
        """
        self.__input_power_present = input_power_present        # bool

        self.__charge = charge                                  # ChargeLevel

        self.__tte = tte                                        # TimeDelta     time to empty
        self.__ttf = ttf                                        # TimeDelta     time to full

        self.__v = Datum.float(v)                               # float         voltage
        self.__current = Datum.int(current)                     # int           current (mA)
        self.__temperature = Datum.float(temperature, 1)        # float         temperature (°C)

        self.__capacity = Datum.int(capacity)                   # int           mAh
        self.__cycles = Datum.float(cycles, 1)                  # float         percentage


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['in'] = self.input_power_present

        jdict['chrg'] = self.charge

        jdict['tte'] = None if self.tte is None else self.tte.as_json()
        jdict['ttf'] = None if self.ttf is None else self.ttf.as_json()

        jdict['v'] = self.v
        jdict['curr'] = self.current
        jdict['g-tmp'] = self.temperature

        jdict['cap'] = self.capacity
        jdict['cyc'] = self.cycles

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def input_power_present(self):
        return self.__input_power_present


    @property
    def charge(self):
        return self.__charge


    @property
    def tte(self):
        return self.__tte


    @property
    def ttf(self):
        return self.__ttf


    @property
    def v(self):
        return self.__v


    @property
    def current(self):
        return self.__current


    @property
    def temperature(self):
        return self.__temperature


    @property
    def capacity(self):
        return self.__capacity


    @property
    def cycles(self):
        return self.__cycles


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BattStatus:{input_power_present:%s, charge:%s, tte:%s, ttf:%s, v:%s, current:%s, temperature:%s, " \
               "capacity:%s, cycles:%s}" % \
               (self.input_power_present, self.charge, self.tte, self.ttf, self.v, self.current, self.temperature,
                self.capacity, self.cycles)


# --------------------------------------------------------------------------------------------------------------------

class ChargeLevel(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        percent = jdict.get('%')
        mah = jdict.get('mah')

        return cls(percent, mah)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, percent, mah):
        """
        Constructor
        """
        self.__percent = Datum.float(percent, 1)                    # float         percentage
        self.__mah = Datum.int(mah)                                 # int           mAh


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['%'] = self.percent
        jdict['mah'] = self.mah

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def percent(self):
        return self.__percent


    @property
    def mah(self):
        return self.__mah


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChargeLevel:{percent:%s, mah:%s}" %  (self.percent, self.mah)
