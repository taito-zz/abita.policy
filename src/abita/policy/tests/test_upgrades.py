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

    @mock.patch('abita.policy.upgrades.reimport_profile')
    def test_reimport_actions(self, reimport_profile):
        from abita.policy.upgrades import reimport_actions
        reimport_actions(self.portal)
        reimport_profile.assert_called_with(self.portal, 'profile-abita.policy:default', 'actions')
