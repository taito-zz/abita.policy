import mock
import unittest


class TestCase(unittest.TestCase):

    def test(self):
        from abita.policy.setuphandlers import setupVarious
        context = mock.Mock()
        context.readDataFile.return_value = None
        self.assertIsNone(setupVarious(context))
        context.readDataFile.assert_called_with('abita.policy_various.txt')
