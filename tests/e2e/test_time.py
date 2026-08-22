"""
Created on 12 Feb 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v mrcs-test/tests/e2e/test_cli.py

https://stackoverflow.com/questions/58649679/resourcewarning-unclosed-file-io-bufferedreader-name-4
"""

import json
import time
import unittest

from mrcs_core.data.iso_datetime import ISODatetime
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

    def test_time_now(self):
        r = CLI.popen(['mrcs_cli_time', '-n'])
        datetime = ISODatetime.construct_from_jdict(json.loads(r.stdout))
        self.assertIsNotNone(datetime)


    def test_time_set(self):
        CLI.popen(['mrcs_control_recorder', '-t', '-c', '-r', 1])

        r = CLI.popen(['mrcs_cli_time', '-s', '-sr', '-ss', 4, '-sy', 1930, '-sm', 1, '-sd', 2, '-sh', 6])
        datetime = ISODatetime.construct_from_jdict(json.loads(r.stdout))
        self.assertIsNotNone(datetime)

        r = CLI.popen(['mrcs_cli_messages', '-l', 100])
        jdict = json.loads(r.stdout)
        self.assertEqual(len(jdict), 2)


    def test_crontab(self):
        CLI.popen(['mrcs_control_recorder', '-t', '-c', '-r', 1])
        CLI.popen(['mrcs_control_cron', '-t', '-c', '-l'])

        r = CLI.popen(['mrcs_cli_time', '-s', '-sr', '-ss', 4, '-sy', 1930, '-sm', 1, '-sd', 2, '-sh', 6])
        datetime = ISODatetime.construct_from_jdict(json.loads(r.stdout))
        self.assertIsNotNone(datetime)

        message = '{"event_id": "abc", "on": "1930-01-02T06:01:00.000"}'
        CLI.popen(['mrcs_cli_publisher', '-t', 'CRN', '-b', 0, '-n', 3, '-m', message])

        r = CLI.popen(['mrcs_control_crontab', '-t', '-l'])
        jdict = json.loads(r.stdout)
        self.assertEqual(len(jdict), 1)

        r = CLI.popen(['mrcs_cli_messages', '-l', 100])
        jdict = json.loads(r.stdout)
        self.assertEqual(len(jdict), 3)


    def test_cron(self):
        CLI.popen(['mrcs_control_recorder', '-t', '-c', '-r', 1])
        CLI.popen(['mrcs_control_cron', '-t', '-c', '-l'])

        r = CLI.popen(['mrcs_cli_time', '-s', '-sr', '-ss', 4, '-sy', 1930, '-sm', 1, '-sd', 2, '-sh', 6])
        datetime = ISODatetime.construct_from_jdict(json.loads(r.stdout))
        self.assertIsNotNone(datetime)

        message = '{"event_id": "abc", "on": "1930-01-02T06:00:12.000"}'
        CLI.popen(['mrcs_cli_publisher', '-t', 'CRN', '-b', 0, '-n', 3, '-m', message])

        time.sleep(4)

        r = CLI.popen(['mrcs_control_crontab', '-t', '-l'])
        jdict = json.loads(r.stdout)
        self.assertEqual(len(jdict), 0)

        r = CLI.popen(['mrcs_cli_messages', '-l', 100])
        jdict = json.loads(r.stdout)
        self.assertEqual(len(jdict), 4)


if __name__ == "__main__":
    unittest.main()
