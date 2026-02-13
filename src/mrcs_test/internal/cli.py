"""
Created on 13 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

A wrapper for Popen to simplify invocation of command-line utilities
"""

from subprocess import Popen, PIPE

from mrcs_core.sys.env_paths import EnvPaths


# --------------------------------------------------------------------------------------------------------------------

class CLIResponse(object):
    """
    simplifying the CLI response
    """


    def __init__(self, stdout: str, stderr: str, returncode: int):
        self.__stdout = stdout
        self.__stderr = stderr
        self.__returncode = returncode


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def stdout(self):
        return self.__stdout


    @property
    def stderr(self):
        return self.__stderr


    @property
    def returncode(self):
        return self.__returncode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'CLIResponse:{{stdout:{self.stdout}, stderr:{self.stderr}, returncode:{self.returncode}}}'


# --------------------------------------------------------------------------------------------------------------------

class CLI(object):
    """
    a wrapper for Popen to simplify invocation of command-line utilities
    """

    env = EnvPaths.construct().as_dict()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def popen(cls, cmd_args) -> CLIResponse:
        str_args = [str(arg) for arg in cmd_args if arg is not None]

        with Popen(str_args, stdout=PIPE, stderr=PIPE, env=cls.env) as p:
            p.wait()

            stdout = p.stdout.read().decode().strip()
            stderr = p.stderr.read().decode().strip()
            returncode = p.returncode

        return CLIResponse(stdout, stderr, returncode)
