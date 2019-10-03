#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify

from scs_core.sync.interval_timer import IntervalTimer

from scs_psu.fuel_gauage.batt_pack_v1_gauge import BattPackV1Gauge

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    gauge = BattPackV1Gauge()
    gauge.initialise(True)

    print(gauge, file=sys.stderr)
    sys.stderr.flush()

    timer = IntervalTimer(10.0)

    while timer.true():
        datum = gauge.sample()

        print(JSONify.dumps(datum))
        sys.stdout.flush()

except KeyboardInterrupt:
    print()

finally:
    I2C.close()
