#!/usr/bin/env python3

"""
Created on 12 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

psu = PSU()
print(psu)

psu.power_cycle(10, 10)
