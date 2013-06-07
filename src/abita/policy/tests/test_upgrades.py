from abita.policy.tests.base import IntegrationTestCase

import mock


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def test_reimport_actions(self):
        from abita.policy.upgrades import reimport_actions
        setup = mock.Mock()
        reimport_actions(setup)
        setup.runImportStepFromProfile.assert_called_with('profile-abita.policy:default', 'actions', run_dependencies=False, purge_old=False)

    def test_reimport_propertiestool(self):
        from abita.policy.upgrades import reimport_propertiestool
        setup = mock.Mock()
        reimport_propertiestool(setup)
        setup.runImportStepFromProfile.assert_called_with('profile-abita.policy:default', 'propertiestool', run_dependencies=False, purge_old=False)

    def test_reimport_languagetool(self):
        from abita.policy.upgrades import reimport_languagetool
        setup = mock.Mock()
        reimport_languagetool(setup)
        setup.runImportStepFromProfile.assert_called_with('profile-abita.policy:default', 'languagetool', run_dependencies=False, purge_old=False)
