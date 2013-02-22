from Products.CMFCore.utils import getToolByName
from abita.policy.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_abita_policy_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.policy'))

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.policy'])
        self.failIf(installer.isProductInstalled('abita.policy'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-abita.policy:default'), u'2')

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

    def test_mailhost__smtp_host(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_host, 'smtp.gmail.com')

    def test_mailhost__smtp_port(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_port, 587)

    def test_languages__available(self):
        tool = getToolByName(self.portal, 'portal_languages')
        self.assertEquals(tool.listSupportedLanguages(), [
            ('en', u'English'), ('fi', u'Finnish'), ('ja', u'Japanese')])

    def test_languages__use_request_negotiation(self):
        tool = getToolByName(self.portal, 'portal_languages')
        self.assertTrue(tool.use_request_negotiation)

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

    def test_abita_development_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.development'))

    def test_abita_theme_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.theme'))
