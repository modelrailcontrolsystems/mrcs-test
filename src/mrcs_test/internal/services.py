"""
Created on 11 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

The application services required for MRCS operations to run.
It is assumed that all of these services are long-running.
Since no process should launch services more than once, the services collection is implemented as a class field.
"""

import signal
import sys
from subprocess import DEVNULL, Popen

from mrcs_core.sys.env_paths import EnvPaths


# --------------------------------------------------------------------------------------------------------------------

class Services(object):
    """
    the application services required for MRCS operations to run
    """

    __CMD_ARGS = [
        ['mrcs_control_clock_manager', '--verbose', '--test', '--subscribe'],
        ['mrcs_control_recorder', '--verbose', '--test', '--clean', '--subscribe'],
        ['mrcs_control_cron', '--verbose', '--test', '--clean', '--run-save'],
        ['mrcs_control_crontab', '--verbose', '--test', '--subscribe'],
        ['mrcs_api_uvicorn', '--verbose', '--test', '--reload']
    ]

    __services = []


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def start(cls, silent=False):
        stdout = DEVNULL if silent else sys.stdout
        stderr = DEVNULL if silent else sys.stderr
        env = EnvPaths.construct().as_dict()

        for cmd_args in cls.__CMD_ARGS:
            cls.__services.append(Popen(cmd_args, stdout=stdout, stderr=stderr, env=env))


    @classmethod
    def wait(cls):
        for service in cls.__services:
            service.wait()


    @classmethod
    def stop(cls):
        for service in cls.__services:
            service.send_signal(signal.SIGINT)
            service.wait()

        cls.__services = []
