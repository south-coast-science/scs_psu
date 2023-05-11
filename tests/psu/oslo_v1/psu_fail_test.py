#!/usr/bin/env python3

"""
Created on 11 May 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import os
import sys
import time

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_psu.psu.oslo_v1.psu_status import PSUStatus
from scs_psu.psu.psu_conf import PSUConf


# ------------------------------------------------------------------------------------------------------------

Logging.config("test", verbose=True)
logger = Logging.getLogger()


# ------------------------------------------------------------------------------------------------------------
# resources...

# PSU...
psu_conf = PSUConf.load(Host)
psu = psu_conf.psu(Host, None)

print("os: %s" % os.name, file=sys.stderr)
print("psu: %s" % psu, file=sys.stderr)


# --------------------------------------------------------------------------------------------------------------------

iteration = 0
fails = 0

try:
    while True:
        iteration += 1

        start_time = time.time()
        response = psu.communicate('state')
        elapsed_time = time.time() - start_time

        if response is None:
            fails += 1
            report = None

        else:
            status = PSUStatus.construct_from_jdict(json.loads(response))
            report = None if status is None else status.standby

            if report is None:
                logger.error("bad response: %s" % response)

        logger.error("%5d / %3d: %0.3f: %s" % (iteration, fails, round(elapsed_time, 3), report))

except KeyboardInterrupt:
    print(file=sys.stderr)
