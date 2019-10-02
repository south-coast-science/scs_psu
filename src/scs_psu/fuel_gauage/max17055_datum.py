"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class MAX17055Datum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        charge = MAX17055Charge.construct_from_jdict(jdict.get('chrg'))
        tte = Timedelta(seconds=jdict.get('tte'))
        ttf = Timedelta(seconds=jdict.get('ttf'))

        current = jdict.get('curr')
        temperature = jdict.get('g-tmp')

        return MAX17055Datum(charge, tte, ttf, current, temperature)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, charge, tte, ttf, current, temperature):
        """
        Constructor
        """
        self.__charge = charge                                  # MAX17055Charge
        self.__tte = tte                                        # TimeDelta     time to empty
        self.__ttf = ttf                                        # TimeDelta     time to full

        self.__current = Datum.int(current)                     # int           current (mA)
        self.__temperature = Datum.float(temperature, 1)        # float         temperature (°C)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['chrg'] = self.charge
        jdict['tte'] = None if self.tte is None else int(self.tte.total_seconds())
        jdict['ttf'] = None if self.ttf is None else int(self.ttf.total_seconds())

        jdict['curr'] = self.current
        jdict['g-tmp'] = self.temperature

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

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
    def current(self):
        return self.__current


    @property
    def temperature(self):
        return self.__temperature


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MAX17055Datum:{charge:%s, tte:%s, ttf:%s, current:%s, temperature:%s}" % \
               (self.charge, self.tte, self.ttf, self.current, self.temperature)


# --------------------------------------------------------------------------------------------------------------------

class MAX17055Charge(JSONable):
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

        return MAX17055Charge(percent, mah)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, percent, mah):
        """
        Constructor
        """
        self.__percent = Datum.float(percent, 1)                    # float         %
        self.__mah = Datum.int(mah)                                 # int           mAh


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
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
        return "MAX17055Charge:{percent:%s, mah:%s}" %  (self.percent, self.mah)
