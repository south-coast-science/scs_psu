#!/usr/bin/env python3

"""
Created on 17 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_host.sys.host import Host

from scs_psu.psu.psu import PSU


# --------------------------------------------------------------------------------------------------------------------

psu = PSU(Host.psu_device())
print(psu, file=sys.stderr)
print("-")


while True:
    now = LocalizedDatetime.now()
    start = time.time()

    response = psu.communicate('status')
    elapsed = time.time() - start

    print("%s, %0.3f, '%s'" % (now.as_iso8601(), elapsed, response))
    sys.stdout.flush()

    time.sleep(1.0)
