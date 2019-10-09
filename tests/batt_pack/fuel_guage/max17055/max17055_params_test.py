#!/usr/bin/env python3

"""
Created on 3 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/electricimp/MAX17055
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_psu.batt_pack.fuel_gauge.max17055.max17055_params import MAX17055Params


# --------------------------------------------------------------------------------------------------------------------

r_comp_0 = 1
temp_co = 2
full_cap_rep = 3
full_cap_nom = 4
cycles = 5

params = MAX17055Params(r_comp_0, temp_co, full_cap_rep, full_cap_nom, cycles)
print(params)
print("-")

jstr = JSONify.dumps(params)
print(jstr)
print("-")

params.save(Host)

params = MAX17055Params.load(Host)
print(params)
