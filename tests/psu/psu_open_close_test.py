#!/usr/bin/env python3

"""
Created on 12 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

screen /dev/ttyUSB0 1200,cs8,-parenb,cstopb,-hupcl,clocal
"""

import sys
import time

from scs_core.data.datetime import LocalizedDatetime

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

# Interface...
interface_conf = InterfaceConf.load(Host)

psu_conf = PSUConf.load(Host)

psu = psu_conf.psu(Host, interface_conf.model)
print(psu)
print("-")

try:
    for i in range(1000000):
        now = LocalizedDatetime.now().utc()
        start = time.time()

        psu.open()

        response = psu.communicate('status')

        psu.close()

        elapsed = time.time() - start

        print("%7d: %s, %0.3f, '%s'" % ((i + 1), now.as_iso8601(), elapsed, response))
        print("-")

        sys.stdout.flush()
        time.sleep(1.0)

        if len(response) < 10:
            break

except KeyboardInterrupt:
    pass

finally:
    psu.close()
