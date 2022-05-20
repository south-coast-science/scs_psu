#!/usr/bin/env python3

"""
Created on 29 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.json import JSONify

from scs_host.bus.i2c import I2C

from scs_psu.psu.opcube_v1.io_expander import PCA9534A


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.Utilities.open()

    io = PCA9534A()
    print(io)

    io.init()

    for i in range(2):
        io.set_leds(False, False)
        time.sleep(2.0)

        io.set_leds(False, True)
        time.sleep(2.0)

        io.set_leds(True, False)
        time.sleep(2.0)

        io.set_leds(True, True)
        time.sleep(2.0)

    io.set_leds(False, False)

    print("=")

    while True:
        status = io.sample()
        print(status)

        print(JSONify.dumps(status))
        print("-")

        time.sleep(2.0)

except KeyboardInterrupt:
    print()

finally:
    I2C.Utilities.close()
