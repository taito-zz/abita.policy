from Products.CMFCore.utils import getToolByName
from abita.policy.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_package_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.policy'))

    def test_actions__user__dashboard(self):
        actions = getToolByName(self.portal, 'portal_actions')
        category = getattr(actions, 'user')
        self.assertFalse(getattr(category, 'dashboard').getProperty('visible'))

    def test_actions__user__login(self):
        actions = getToolByName(self.portal, 'portal_actions')
        category = getattr(actions, 'user')
        self.assertFalse(getattr(category, 'login').getProperty('visible'))

    def test_actions__portal_tabs__index_html(self):
        actions = getToolByName(self.portal, 'portal_actions')
        category = getattr(actions, 'portal_tabs')
        self.assertFalse(getattr(category, 'index_html').getProperty('visible'))

    def test_mailhost__smtp_host(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_host, 'smtp.gmail.com')

    def test_mailhost__smtp_port(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_port, 587)

    def test_metadata__dependency__abita_development(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.development'))

    def test_metadata__dependency__abita_theme(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.theme'))

    def test_metadata__dependency__plone_app_multilingual(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('plone.app.multilingual'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-abita.policy:default'), u'4')

    def test_portal_languages__supported_langs(self):
        tool = getToolByName(self.portal, 'portal_languages')
        self.assertEquals(tool.listSupportedLanguages(), [
            ('en', u'English'), ('fi', u'Finnish'), ('ja', u'Japanese')])

    def test_portal_languages__use_request_negotiation(self):
        tool = getToolByName(self.portal, 'portal_languages')
        self.assertTrue(tool.use_request_negotiation)

    def test_properties_title(self):
        self.assertEqual(self.portal.getProperty('title'), 'ABITA')

    def test_properties_description(self):
        self.assertEqual(
            self.portal.getProperty('description'), 'Open Source Technologies and Open Businesses')

    def test_properties__email_from_address(self):
        self.assertEqual(self.portal.getProperty('email_from_address'), 'info@abita.fi')

    def test_properties__email_from_name(self):
        self.assertEqual(self.portal.getProperty('email_from_name'), 'ABITA')

    def test_propertiestool__default_page(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(site_props.getProperty('default_page'), ('abita-view',))

    def test_propertiestool__disable_nonfolderish_sections(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertTrue(site_props.getProperty('disable_nonfolderish_sections'))

    def test_propertiestool__displayPublicationDateInByline(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertTrue(site_props.getProperty('displayPublicationDateInByline'))

    def test_propertiestool__external_links_open_new_window(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(site_props.getProperty('external_links_open_new_window'), 'true')

    def test_propertiestool__webstats_js(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(
            site_props.getProperty('webstats_js'),
            '<script type="text/javascript">\n\nvar _gaq = _gaq || [];\n_gaq.push([\'_setAccount\', \'UA-789306-1\']);\n_gaq.push([\'_trackPageview\']);\n\n(function() {\nvar ga = document.createElement(\'script\'); ga.type = \'text/javascript\'; ga.async = true;\nga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\nvar s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\n})();\n\n</script>'
        )

    def test_propertiestool__use_email_as_login(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertTrue(
            site_props.getProperty('use_email_as_login')
        )

    def test_disable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    def test_calendar_firstweekday(self):
        ctool = getToolByName(self.portal, 'portal_calendar')
        self.assertEqual(ctool.firstweekday, 0)

    def test_tinymce__link_using_uids(self):
        tinymce = getToolByName(self.portal, 'portal_tinymce')
        self.assertTrue(tinymce.link_using_uids)

    def test_front_page_removed(self):
        self.assertRaises(KeyError, lambda: self.portal['front-page'])

    def test_Member_folder_exclude_from_nav(self):
        folder = self.portal['Members']
        self.assertTrue(folder.exclude_from_nav())

    def test_content_rule(self):
        items = [
            item['name'] for item in self.portal.rolesOfPermission(
                "Content rules: Manage rules"
            ) if item['selected'] == 'SELECTED'
        ]
        self.assertEqual(len(items), 2)
        permissions = ['Site Administrator', 'Manager']
        for item in items:
            self.assertTrue(item in permissions)
        self.assertFalse(
            self.portal.acquiredRolesAreUsedBy(
                "Content rules: Manage rules"
            )
        )

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.policy'])
        self.assertFalse(installer.isProductInstalled('abita.policy'))
