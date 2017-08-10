#!/usr/bin/env python3

"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./psu.py -v status
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_psu.cmd.cmd_psu import CmdPSU
from scs_psu.psu.psu import PSU



# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdPSU()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resource...

        psu = PSU()

        if cmd.verbose:
            print(psu, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.has_psu_command:
            # use cmd args...
            response = psu.communicate(cmd.psu_command)
            print(response)

        else:
            # use stdin...
            if cmd.prompt:
                print('> ', file=sys.stderr, end='')
                sys.stderr.flush()

            for line in sys.stdin:
                command = line.strip()

                response = psu.communicate(command)
                print(response)
                sys.stdout.flush()

                if cmd.prompt:
                    print('> ', file=sys.stderr, end='')
                    sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("psu: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
