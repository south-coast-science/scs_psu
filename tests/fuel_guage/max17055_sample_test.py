#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.json import JSONify

from scs_psu.fuel_gauage.max17055 import MAX17055
from scs_psu.fuel_gauage.max17055_config import MAX17055Config

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

des_cap = 6200
sense_res = 0.01
chrg_term = 10                 # 10, 20 or 250?
empty_v_target = 2.7
recovery_v = 3.0
chrg_v = MAX17055Config.CHRG_V_4_4_OR_4_35
batt_type = MAX17055Config.BATT_TYPE_LiCoO2

conf = MAX17055Config(des_cap, sense_res, chrg_term, empty_v_target, recovery_v, chrg_v, batt_type)

try:
    I2C.open(Host.I2C_SENSORS)

    gauge = MAX17055(conf)
    loaded = gauge.initialise(True)

    while True:
        datum = gauge.sample()
        print(JSONify.dumps(datum))

        time.sleep(5.0)

except KeyboardInterrupt:
    print()

finally:
    I2C.close()
