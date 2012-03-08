from abita.policy.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def checkRoles(self, obj, permission):
        return [
                item for item in obj.rolesOfPermission(
                    permission
                ) if item['selected'] == 'SELECTED'
            ]

    def test_is_abita_policy_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.policy'))

    def test_uninstall(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.policy'])
        self.failIf(installer.isProductInstalled('abita.policy'))

    def test_browserlayer(self):
        from abita.policy.browser.interfaces import IAbitaPolicyLayer
        from plone.browserlayer import utils
        self.failUnless(IAbitaPolicyLayer in utils.registered_layers())

    def test_dashboard(self):
        tool = getToolByName(self.portal, 'portal_actions')
        actions = getattr(tool, 'user')
        action = getattr(actions, 'dashboard')
        self.assertFalse(action.getProperty('visible'))

    def test_properties_title(self):
        self.assertEqual(self.portal.getProperty('title'), 'ABITA')

    def test_properties_description(self):
        self.assertEqual(
            self.portal.getProperty('description'),
            'Open Source Technologies and Open Businesses'
        )

    def test_properties__email_from_address(self):
        self.assertEqual(self.portal.getProperty('email_from_address'), 'info@abita.fi')

    def test_properties__email_from_name(self):
        self.assertEqual(self.portal.getProperty('email_from_name'), 'ABITA')

    def test_propertiestool__disable_nonfolderish_sections(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertTrue(site_props.getProperty('disable_nonfolderish_sections'))

    def test_propertiestool__default_language(self):
        properties = getToolByName(self.portal, 'portal_properties')
        site_props = properties.site_properties
        self.assertEqual(site_props.getProperty('default_language'), 'ja')

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
        self.assertEqual(mailhost.smtp_host, 'smtp.nebula.fi')

    def test_mailhost__smtp_port(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_port, 25)

    def test_languages__site(self):
        self.assertEquals('en', self.portal.Language())

    def test_languages__available(self):
        tool = getToolByName(self.portal, 'portal_languages')
        self.assertEquals(
            tool.listSupportedLanguages(),
            [('en', u'English'), ('ja', u'Japanese')]
        )

    def test_languages__use_request_negotiation(self):
        tool = getToolByName(self.portal, 'portal_languages')
        self.assertTrue(tool.use_request_negotiation)

    def test_portlets_left_column__navigation_removed(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        column = getUtility(IPortletManager, name=u"plone.leftcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('navigation' in assignable.keys())

    def test_portlets_right_column__news_removed(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        column = getUtility(IPortletManager, name=u"plone.rightcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('news' in assignable.keys())

    def test_portlets_right_column__events_removed(self):
        from zope.component import getUtility
        from zope.component import getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        column = getUtility(IPortletManager, name=u"plone.rightcolumn")
        assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        self.assertFalse('events' in assignable.keys())

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

    def test_Member_folder_exclude_from_nav(self):
        folder = self.portal['Members']
        self.assertTrue(folder.exclude_from_nav())

    def test_news_folder__title(self):
        folder = self.portal['news']
        self.assertEqual(folder.Title(), 'News')

    def test_news_folder__description(self):
        folder = self.portal['news']
        self.assertEqual(folder.Description(), '')

    def test_news_folder__language(self):
        folder = self.portal['news']
        self.assertEqual(folder.Language(), '')

    def test_news_folder__exclude_from_nav(self):
        folder = self.portal['news']
        self.assertFalse(folder.exclude_from_nav())

    def test_events_folder_exclude_from_nav(self):
        folder = self.portal['events']
        self.assertTrue(folder.exclude_from_nav())

    def test_topics_folder__title(self):
        folder = self.portal['topics']
        self.assertEqual(folder.Title(), 'Topics')

    def test_topic_folder__language(self):
        folder = self.portal['topics']
        self.assertEqual(folder.Language(), '')

    def test_topics_folder__exclude_from_nav(self):
        folder = self.portal['topics']
        self.assertFalse(folder.exclude_from_nav())

    def test_services_folder__title(self):
        folder = self.portal['services']
        self.assertEqual(folder.Title(), 'Services')

    def test_services_folder__language(self):
        folder = self.portal['services']
        self.assertEqual(folder.Language(), '')

    def test_services_folder__exclude_from_nav(self):
        folder = self.portal['services']
        self.assertFalse(folder.exclude_from_nav())

    def test_applications_folder__title(self):
        folder = self.portal['applications']
        self.assertEqual(folder.Title(), 'Applications')

    def test_applications_folder__language(self):
        folder = self.portal['applications']
        self.assertEqual(folder.Language(), '')

    def test_applications_folder__exclude_from_nav(self):
        folder = self.portal['applications']
        self.assertFalse(folder.exclude_from_nav())

    def test_company_folder__title(self):
        folder = self.portal['company']
        self.assertEqual(folder.Title(), 'Company')

    def test_company_folder__language(self):
        folder = self.portal['company']
        self.assertEqual(folder.Language(), '')

    def test_company_folder__exclude_from_nav(self):
        folder = self.portal['company']
        self.assertFalse(folder.exclude_from_nav())

    def test_contact_folder__title(self):
        folder = self.portal['contact']
        self.assertEqual(folder.Title(), 'Contact')

    def test_contact_folder__language(self):
        folder = self.portal['contact']
        self.assertEqual(folder.Language(), '')

    def test_contact_folder__exclude_from_nav(self):
        folder = self.portal['contact']
        self.assertFalse(folder.exclude_from_nav())

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

    def test_dependencies_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('abita.theme'))
        self.failUnless(installer.isProductInstalled('PloneFormGen'))
