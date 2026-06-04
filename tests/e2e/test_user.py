"""
Created on 12 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v mrcs-test/tests/e2e/test_cli.py

https://stackoverflow.com/questions/58649679/resourcewarning-unclosed-file-io-bufferedreader-name-4
"""

import json
import time
import unittest

from mrcs_core.admin.user.user import User
from mrcs_test.internal.cli import CLI
from mrcs_test.internal.services import Services


# --------------------------------------------------------------------------------------------------------------------

class TestCLI(unittest.TestCase):
    """
    classdocs
    """


    @classmethod
    def setUpClass(cls):
        silent = True

        Services.start(silent=silent)
        time.sleep(2)
        CLI.popen(['mrcs_cli_session', '-c', 'bbeloff1@me.com', 'pass'])


    @classmethod
    def tearDownClass(cls):
        Services.stop()


    # ----------------------------------------------------------------------------------------------------------------

    def test_session_create_fail(self):
        r = CLI.popen(['mrcs_cli_session', '-c', 'bbeloff1@me.com', 'fail'])
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stderr, 'mrcs_cli_session: HTTPResponseException: HTTPResponse: 400: '
                                   'Bad Request: incorrect username or password')


    def test_session_create(self):
        r = CLI.popen(['mrcs_cli_session', '-c', 'bbeloff1@me.com', 'pass'])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stderr, '')


    def test_user_self(self):
        r = CLI.popen(['mrcs_cli_users', '-s'])
        user = User.construct_from_jdict(json.loads(r.stdout))
        self.assertEqual(user.email, 'bbeloff1@me.com')


if __name__ == "__main__":
    unittest.main()
