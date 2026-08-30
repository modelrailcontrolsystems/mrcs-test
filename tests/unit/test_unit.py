"""
Created on 29 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v mrcs-test/tests/unit/test_unit.py
"""

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

    @classmethod
    def setUpClass(cls):
        cls._reset_state()


    @classmethod
    def tearDownClass(cls):
        cls._reset_state()


    def setUp(self):
        self._reset_state()


    def tearDown(self):
        self._reset_state()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def _reset_state(cls):
        if 'mrcs_control.messaging.mq_topology' in sys.modules:
            mq_topology = sys.modules['mrcs_control.messaging.mq_topology']
            if hasattr(mq_topology, 'MQTopology'):
                mq_topology.MQTopology.SINGLE_PROCESS.value._QueueConfiguration__queue_name = None
                mq_topology.MQTopology.MULTI_PROCESS.value._QueueConfiguration__queue_name = None

        if 'mrcs_control.test.test_helper' in sys.modules:
            control_test_helper = sys.modules['mrcs_control.test.test_helper']
            if hasattr(control_test_helper, 'TestHelper'):
                try:
                    control_test_helper.TestHelper.dbTeardown()
                except Exception:
                    pass

        if 'mrcs_api.test.test_helper' in sys.modules:
            test_helper = sys.modules['mrcs_api.test.test_helper']
            if hasattr(test_helper, 'TestHelper'):
                try:
                    test_helper.TestHelper.dbTeardown()
                except Exception:
                    pass


    def _run_stage(self, module_name: str, unit_dir: Path):
        self._reset_state()

        if not unit_dir.exists():
            return

        test_root = str(unit_dir)
        added_to_path = False
        if test_root not in sys.path:
            sys.path.insert(0, test_root)
            added_to_path = True

        before_modules = set(sys.modules.keys())

        try:
            loader = unittest.TestLoader()
            suite = loader.discover(start_dir=str(unit_dir), top_level_dir=test_root)

            if suite.countTestCases() == 0:
                return

            runner = unittest.TextTestRunner(stream=sys.stdout)
            result = runner.run(suite)

            self.assertTrue(
                result.wasSuccessful(),
                f'{module_name} unit tests failed: {len(result.failures)} failure(s), {len(result.errors)} error(s)'
            )
        finally:
            if added_to_path and test_root in sys.path:
                sys.path.remove(test_root)

            for mod in list(sys.modules.keys()):
                if mod not in before_modules and mod != 'unit' and not mod.startswith('unit.'):
                    sys.modules.pop(mod, None)

            self._reset_state()


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
