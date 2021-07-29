#!/usr/bin/env python3

"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_psu.batt_pack.batt_pack_v1 import BattPackV1
from scs_psu.batt_pack.fuel_gauge.max17055.max17055 import Max17055

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

conf = BattPackV1.gauge_conf()
print(conf)
print("-")

try:
    I2C.Utilities.open()

    gauge = Max17055(conf)
    loaded = gauge.initialise()
    print("conf loaded: %s" % loaded)
    print(gauge)

    rev = gauge.read_device_rev()
    print("rev:0x%04x" % rev)
    print("-")

    cycles = gauge.read_cycles()
    print("cycles:%s" % cycles)
    print("-")

    while True:
        # print('\033[2J')            # clear screen

        charge_percent = gauge.read_charge_percent()
        charge_mah = gauge.read_charge_mah()
        print("charge level:%s%%, %smAh" % (charge_percent, charge_mah))
        print()

        tte = gauge.read_time_until_empty()
        print("tte:%s" % tte)
        print()

        ttf = gauge.read_time_until_full()
        print("ttf:%s" % ttf)
        print()

        current = gauge.read_current()
        print("current:%smA" % current)
        print()

        voltage = gauge.read_voltage()
        print("voltage:%sV" % voltage)
        print()

        temperature = gauge.read_temperature()
        print("gauge temperature:%s°C" % temperature)
        print()

        input_power_present = gauge.input_power_present()
        print("input power present:%s" % input_power_present)
        print()

        print("-")
        print()
        time.sleep(5.0)

except KeyboardInterrupt:
    print()

finally:
    I2C.Utilities.close()
