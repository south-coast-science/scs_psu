#!/usr/bin/env python3

"""
Created on 10 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify

from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

psu = PSU()
print(psu)
print("-")

version = psu.version()
print(version)
print(JSONify.dumps(version))
print("-")

status = psu.status()
print(status)
print(JSONify.dumps(status))
print("-")

uptime = psu.uptime()
print(uptime)
print(JSONify.dumps(uptime))
print("-")

touch = psu.watchdog_touch()
print(touch)
print("-")

start = psu.watchdog_start(10)
print(start)
print("-")

stop = psu.watchdog_stop()
print(stop)
print("-")
