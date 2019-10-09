#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify

from scs_core.sync.interval_timer import IntervalTimer

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

pack = None

try:
    I2C.open(Host.I2C_SENSORS)

    pack = BattPackV1.construct()
    loaded = pack.initialise(Host)

    print(pack, file=sys.stderr)
    print("loaded:%s" % loaded, file=sys.stderr)
    sys.stderr.flush()

    timer = IntervalTimer(10.0)

    while timer.true():
        datum = pack.sample_fuel_status()

        print(JSONify.dumps(datum))
        sys.stdout.flush()

except KeyboardInterrupt:
    print()

finally:
    if pack:
        pack.save_learning(Host)
        print("saved learning", file=sys.stderr)

    I2C.close()
