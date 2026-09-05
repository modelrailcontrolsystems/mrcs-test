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

    __COMMANDS = [
        ['mrcs_control_clock_manager', '--verbose', '--subscribe'],
        ['mrcs_control_cron', '--verbose', '--clean', '--run-save'],
        ['mrcs_control_crontab', '--verbose', '--subscribe'],
        ['mrcs_control_mpu', '--verbose', '--drain', '--run'],
        ['mrcs_control_recorder', '--verbose', '--drain', '--clean', '--subscribe'],
        ['mrcs_control_router', '--verbose', '--run'],
        ['mrcs_control_track', '--verbose', '--drain', '--run'],
        ['mrcs_api_uvicorn', '--verbose', '--reload']
    ]

    __services = []


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def start(cls, silent: bool = False, test_mode: bool = False):
        stdout = DEVNULL if silent else sys.stdout
        stderr = DEVNULL if silent else sys.stderr
        env = EnvPaths.construct().as_dict()

        for command in cls.__COMMANDS:
            if test_mode:
                command.append('--test')

            cls.__services.append(Popen(command, stdout=stdout, stderr=stderr, env=env,
                                        start_new_session=True))


    @classmethod
    def wait(cls):
        for service in cls.__services:
            service.wait()


    @classmethod
    def stop(cls):
        for service in cls.__services:
            if service.poll() is None:
                service.send_signal(signal.SIGINT)

        for service in cls.__services:
            service.wait()

        cls.__services = []
