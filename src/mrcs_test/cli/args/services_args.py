"""
Created on 11 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)
"""

from mrcs_core.cli.args.multimode_args import MultimodeArgs


# --------------------------------------------------------------------------------------------------------------------

class ServicesArgs(MultimodeArgs):
    """unix command line handler"""


    def __init__(self, description):
        super().__init__(description)

        self._parser.add_argument('-p', '--populate', action='store_true', help='populate database')

        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-b', '--backend', action='store_true', help='run backend services only')
        group.add_argument('-u', '--uvicorn', action='store_true', help='run uvicorn service only')
        group.add_argument('-a', '--all', action='store_true', help='run all services')

        self._args = self._parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def populate(self):
        return self._args.populate


    def run_backend(self):
        return self.backend or self.all


    def run_uvicorn(self):
        return self.uvicorn or self.all


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def backend(self):
        return self._args.backend


    @property
    def uvicorn(self):
        return self._args.uvicorn


    @property
    def all(self):
        return self._args.all


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (
            f'ServicesArgs:{{test:{self.test}, populate:{self.populate}, uvicorn:{self.uvicorn}, '
            f'backend:{self.backend}, all:{self.all}, indent:{self.indent}, verbose:{self.verbose}}}')
