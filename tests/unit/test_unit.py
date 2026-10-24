"""
Created on 29 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v mrcs-test/tests/unit/test_unit.py
"""

import subprocess
import sys
import unittest
from pathlib import Path


# --------------------------------------------------------------------------------------------------------------------

class TestUnit(unittest.TestCase):
    """
    Facility to run all project unit tests in isolated stages and combine coverage reporting.
    """

    __PROJECT_ROOT = Path(__file__).resolve().parents[3]

    __MODULES = [
        ('mrcs-api', __PROJECT_ROOT / 'mrcs-api' / 'api_tests' / 'unit'),
        ('mrcs-cli', __PROJECT_ROOT / 'mrcs-cli' / 'cli_tests' / 'unit'),
        ('mrcs-control', __PROJECT_ROOT / 'mrcs-control' / 'control_tests' / 'unit'),
        ('mrcs-core', __PROJECT_ROOT / 'mrcs-core' / 'core_tests' / 'unit'),
    ]


    # ----------------------------------------------------------------------------------------------------------------

    def _run_stage(self, module_name: str, unit_dir: Path):
        # each stage runs in a fresh interpreter, so no module state (e.g. the embedded SWI-Prolog engine) is shared
        if not unit_dir.exists():
            return

        test_root = str(unit_dir)
        command = [sys.executable, '-m', 'unittest', 'discover', '-s', test_root, '-t', test_root]

        sys.stdout.flush()
        result = subprocess.run(command)

        # unittest exits with 5 when no tests were found
        if result.returncode == 5:
            return

        self.assertEqual(0, result.returncode, f'{module_name} unit tests failed: exit code {result.returncode}')


    # ----------------------------------------------------------------------------------------------------------------

    def test_mrcs_api(self):
        self._run_stage('mrcs-api', self.__PROJECT_ROOT / 'mrcs-api' / 'api_tests' / 'unit')


    def test_mrcs_cli(self):
        self._run_stage('mrcs-cli', self.__PROJECT_ROOT / 'mrcs-cli' / 'cli_tests' / 'unit')


    def test_mrcs_control(self):
        self._run_stage('mrcs-control', self.__PROJECT_ROOT / 'mrcs-control' / 'control_tests' / 'unit')


    def test_mrcs_core(self):
        self._run_stage('mrcs-core', self.__PROJECT_ROOT / 'mrcs-core' / 'core_tests' / 'unit')


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
