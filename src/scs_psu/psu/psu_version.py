"""
Created on 13 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"id": "South Coast Science PSU Oslo", "tag": "2.1.4", "c-date": "Jan  4 2019", "c-time": "08:19:11"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUVersion(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # TODO: handle single-string

        id = jdict.get('id')
        tag = jdict.get('tag')
        c_date = jdict.get('c-date')
        c_time = jdict.get('c-time')

        return cls(id, tag, c_date, c_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, tag, c_date, c_time):
        """
        Constructor
        """
        self.__id = id                              # string
        self.__tag = tag                            # string
        self.__c_date = c_date                      # string
        self.__c_time = c_time                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['tag'] = self.tag
        jdict['c-date'] = self.c_date
        jdict['c-time'] = self.c_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def tag(self):
        return self.__tag


    @property
    def c_date(self):
        return self.__c_date


    @property
    def c_time(self):
        return self.__c_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUVersion:{id:%s, tag:%s, c_date:%s, c_time:%s}" % (self.id, self.tag, self.c_date, self.c_time)
