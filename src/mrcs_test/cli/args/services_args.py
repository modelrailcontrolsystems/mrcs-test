"""
Created on 11 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)
"""

import argparse

from mrcs_core import version


# --------------------------------------------------------------------------------------------------------------------

class ServicesArgs(object):
    """unix command line handler"""


    def __init__(self, description):
        self._parser = argparse.ArgumentParser(description=description)

        self._parser.add_argument('-t', '--test', action='store_true',
                                  help='run services in test mode')

        self._parser.add_argument('-v', '--verbose', action='store_true',
                                  help='report narrative to stderr')

        self._parser.add_argument('--version', action='version',
                                  version=f'{self._parser.prog} {version()}')

        self._args = self._parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def test(self):
        return self._args.test


    @property
    def verbose(self):
        return self._args.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'ServicesArgs:{{test:{self.test}, verbose:{self.verbose}}}'
