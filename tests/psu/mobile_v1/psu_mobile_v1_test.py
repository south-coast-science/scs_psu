#!/usr/bin/env python3

"""
Created on 24 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

See also: scs_dfe_end/tests/interface/components/rpz_header_test.py
"""

# from scs_dfe.interface.pzhb.pzhb_mcu_t1_f1 import PZHBMCUt1f1
from scs_dfe.interface.pzhb.pzhb_mcu_t2_f1 import PZHBMCUt2f1

from scs_psu.psu.mobile_v1.psu_mobile_v1 import PSUMobileV1


# --------------------------------------------------------------------------------------------------------------------

# psu = PSUMobileV1(PZHBMCUt1f1(PZHBMCUt1f1.DEFAULT_ADDR))
psu = PSUMobileV1(PZHBMCUt2f1(PZHBMCUt2f1.DEFAULT_ADDR))
print(psu)
print("-")

try:
    psu.open()

    status = psu.status()
    print(status)

finally:
    psu.close()
