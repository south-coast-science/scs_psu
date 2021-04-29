#!/usr/bin/env python3

"""
Created on 26 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.sync.interval_timer import IntervalTimer

from scs_psu.batt_pack.batt_pack_v2 import BattPackV2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Utilities.open()

    pack = BattPackV2.construct()
    print(pack)

    # overwrite any previous BattPack version...
    params = pack.default_params()
    print("default params: %s" % JSONify.dumps(params))
    params.save(Host)

    loaded = pack.initialise(Host, force_config=True)
    # loaded = pack.initialise(Host)
    print("loaded: %s" % loaded, file=sys.stderr)
    sys.stderr.flush()

    timer = IntervalTimer(10.0)

    while timer.true():
        print(LocalizedDatetime.now().as_iso8601(), file=sys.stderr)
        sys.stdout.flush()

        datum = pack.sample()
        print(JSONify.dumps(datum))

        params = pack.read_learned_params()
        print(JSONify.dumps(params), file=sys.stderr)
        # params.save(Host)

        print("-", file=sys.stderr)
        sys.stdout.flush()

except KeyboardInterrupt:
    print()

finally:
    I2C.Utilities.close()
