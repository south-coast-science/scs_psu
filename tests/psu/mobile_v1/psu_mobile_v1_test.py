#!/usr/bin/env python3

"""
Created on 24 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

See also: scs_dfe_end/tests/interface/components/rpz_header_test.py
"""

from scs_psu.psu.mobile_v1.psu_mobile_v1 import PSUMobileV1


# --------------------------------------------------------------------------------------------------------------------

psu = PSUMobileV1()
print(psu)
print("-")

try:
    psu.open()

    status = psu.status()
    print(status)

finally:
    psu.close()
