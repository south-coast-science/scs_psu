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
    I2C.Utilities.open()

    pack = BattPackV1.construct()
    loaded = pack.initialise(Host, force_config=True)

    print(pack, file=sys.stderr)
    print("loaded: %s" % loaded, file=sys.stderr)
    sys.stderr.flush()

    timer = IntervalTimer(10.0)

    while timer.true():
        datum = pack.sample()

        print(JSONify.dumps(datum))
        # print(datum)

        params = pack.read_learned_params()
        params.save(Host)

        print(JSONify.dumps(params))
        # print(params, file=sys.stderr)
        print("-")
        sys.stdout.flush()

except KeyboardInterrupt:
    print()

finally:
    I2C.Utilities.close()
