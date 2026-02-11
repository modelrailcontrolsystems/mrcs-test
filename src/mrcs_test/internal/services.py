"""
Created on 11 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

The application services required for operations to run.
It is assumed that all of these services are long-running.
"""

import sys
from subprocess import PIPE, Popen

from mrcs_core.sys.env_paths import EnvPaths


# --------------------------------------------------------------------------------------------------------------------

class Services(object):
    """
    the application services required for operations to run
    """

    __CMD_ARGS = [
        ['mrcs_clock_manager', '--verbose', '--test', '--subscribe'],
        ['mrcs_recorder', '--verbose', '--test', '--clean', '--subscribe'],
        ['mrcs_cron', '--verbose', '--test', '--run-save'],
        ['mrcs_crontab', '--verbose', '--test', '--subscribe'],
        ['mrcs_uvicorn', '--verbose', '--test', '--reload']
    ]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def start(cls, verbose=False):
        stderr = sys.stderr if verbose else PIPE
        env = EnvPaths.construct().as_dict()
        p = None

        for cmd_args in cls.__CMD_ARGS:
            p = Popen(cmd_args, stderr=stderr, env=env)

            # TODO: check that each service has not died at birth

        return p
