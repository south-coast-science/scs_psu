#!/usr/bin/env python3

"""
Created on 30 Sep 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_psu.fuel_gauage.max17055 import MAX17055
from scs_psu.fuel_gauage.max17055_config import MAX17055Config

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

des_cap = 6200
sense_res = 0.01
chrg_term = 20                 # 20 or 250?
empty_v_target = 2.7
recovery_v = 3.0
chrg_v = MAX17055Config.CHRG_V_4_4_OR_4_35
batt_type = MAX17055Config.BATT_TYPE_LiCoO2

conf = MAX17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)
print(conf)
print("-")

try:
    I2C.open(Host.I2C_SENSORS)

    gauge = MAX17055(conf)
    loaded = gauge.initialise(False)
    print("conf loaded: %s" % loaded)
    print(gauge)
    print("-")

    while True:
        # print('\033[2J')            # clear screen

        charge_percent = gauge.get_charge_state_percent()
        charge_mah = gauge.get_charge_state_mah()
        print("charge level:%s%%, %smAh" % (charge_percent, charge_mah))
        print()

        tte = gauge.get_time_until_empty()
        print("tte:%s" % tte)
        print()

        ttf = gauge.get_time_until_full()
        print("ttf:%s" % ttf)
        print()

        current = gauge.get_current()
        print("current:%smA" % current)
        print()

        voltage = gauge.get_voltage()
        print("voltage:%sV" % voltage)
        print()

        temperature = gauge.get_temperature()
        print("gauge temperature:%s°C" % temperature)
        print()

        print("-")
        print()
        time.sleep(5.0)

except KeyboardInterrupt:
    print()

finally:
    I2C.close()
