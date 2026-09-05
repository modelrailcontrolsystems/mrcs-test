"""
Created on 11 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

The application services required for MRCS operations to run.
It is assumed that all of these services are long-running.
Since no process should launch services more than once, the services collection is implemented as a class field.
"""

import os
import signal
import subprocess
import sys
from subprocess import DEVNULL, Popen

from mrcs_core.sys.env_paths import EnvPaths


# --------------------------------------------------------------------------------------------------------------------

class ServicesRunningException(RuntimeError):
    """
    Raised when one or more MRCS services are already running on the host.
    """
    pass


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
    def find_running_services(cls) -> list[str]:
        """
        Scans the system process table for any active MRCS service binaries.
        Returns a list of matching process descriptions.
        """
        current_pid = str(os.getpid())
        running = []

        for command in cls.__COMMANDS:
            cmd_name = command[0]
            res = subprocess.run(
                ['pgrep', '-f', '-l', cmd_name],
                stdout=subprocess.PIPE,
                stderr=DEVNULL,
                text=True
            )

            if res.returncode == 0 and res.stdout.strip():
                for line in res.stdout.strip().splitlines():
                    parts = line.strip().split(maxsplit=1)
                    if parts:
                        pid = parts[0]
                        cmd_line = parts[1] if len(parts) > 1 else ''
                        if pid != current_pid:
                            tokens = cmd_line.split()
                            if any(token == cmd_name or token.endswith('/' + cmd_name) for token in tokens):
                                running.append(f'{cmd_name} (PID: {pid})')
        return running


    @classmethod
    def is_running(cls) -> bool:
        return bool(cls.find_running_services())


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def start(cls, silent: bool = False, test_mode: bool = False):
        running = cls.find_running_services()
        if running:
            mode_str = 'test mode' if test_mode else 'standard mode'
            conflicts = ', '.join(running)
            raise ServicesRunningException(f'Cannot start services in {mode_str} - '
                                           f'the following service(s) are already running: {conflicts}.')

        stdout = DEVNULL if silent else sys.stdout
        stderr = DEVNULL if silent else sys.stderr
        env = EnvPaths.construct().as_dict()

        cls.__services = []
        for command in cls.__COMMANDS:
            cmd = list(command)
            if test_mode:
                cmd.append('--test')

            cls.__services.append(Popen(cmd, stdout=stdout, stderr=stderr, env=env,
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
