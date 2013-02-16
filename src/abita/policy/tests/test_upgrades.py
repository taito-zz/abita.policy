from abita.policy.tests.base import IntegrationTestCase

import mock


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    @mock.patch('abita.policy.upgrades.utils')
    def test_remove_browser_layer(self, utils):
        from abita.policy.upgrades import remove_browser_layer
        remove_browser_layer(self.portal)
        utils.unregister_layer.assert_called_with('abita.policy')
