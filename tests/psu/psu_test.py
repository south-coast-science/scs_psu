#!/usr/bin/env python3

"""
Created on 10 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

# Interface...
interface_conf = InterfaceConf.load(Host)

psu_conf = PSUConf.load(Host)

psu = psu_conf.psu(Host, interface_conf.model)
print(psu)
print("-")

try:
    psu.open()

    version = psu.version()
    print("version: %s" % version)
    print(JSONify.dumps(version))
    print("-")

    status = psu.status()
    print("status: %s" % status)
    print(JSONify.dumps(status))
    print("-")

    uptime = psu.uptime()
    print("uptime: %s" % uptime)
    print(JSONify.dumps(uptime))
    print("-")

    touch = psu.watchdog_touch()
    print("touch: %s" % touch)
    print("-")

    start = psu.watchdog_start(10)
    print("start: %s" % start)
    print("-")

    stop = psu.watchdog_stop()
    print("stop: %s" % stop)
    print("-")

    pause = psu.charge_pause(0)
    print("pause: %s" % pause)
    print("-")

    dead = psu.charge_dead(0)
    print("dead: %s" % dead)
    print("-")

finally:
    psu.close()
