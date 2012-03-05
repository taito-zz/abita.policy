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

    def test_mailhost__smtp_host(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_host, 'smtp.nebula.fi')

    def test_mailhost__smtp_port(self):
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEqual(mailhost.smtp_port, 25)

    # def test_portlets__news_removed_from_right_column(self):
    #     from zope.component import getUtility
    #     from zope.component import getMultiAdapter
    #     from plone.portlets.interfaces import IPortletManager
    #     from plone.portlets.interfaces import IPortletAssignmentMapping
    #     column = getUtility(IPortletManager, name=u"plone.rightcolumn")
    #     assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
    #     self.assertFalse('news' in assignable.keys())

    # def test_portlets__events_removed_from_right_column(self):
    #     from zope.component import getUtility
    #     from zope.component import getMultiAdapter
    #     from plone.portlets.interfaces import IPortletManager
    #     from plone.portlets.interfaces import IPortletAssignmentMapping
    #     column = getUtility(IPortletManager, name=u"plone.rightcolumn")
    #     assignable = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
    #     self.assertFalse('events' in assignable.keys())

    def test_disable_self_reg(self):
        perms = self.portal.rolesOfPermission(permission='Add portal member')
        anon = [perm['selected'] for perm in perms if perm['name'] == 'Anonymous'][0]
        self.assertEqual(anon, '')

    # def test_Topic__global_allow(self):
    #     tool = getToolByName(self.portal, 'portal_types')
    #     content = tool.getTypeInfo('Topic')
    #     self.assertFalse(content.global_allow)

    # def test_News__Item_global_allow(self):
    #     tool = getToolByName(self.portal, 'portal_types')
    #     content = tool.getTypeInfo('News Item')
    #     self.assertFalse(content.global_allow)

    # def test_Event__global_allow(self):
    #     tool = getToolByName(self.portal, 'portal_types')
    #     content = tool.getTypeInfo('Event')
    #     self.assertFalse(content.global_allow)

    # def test_Folder__global_allow(self):
    #     tool = getToolByName(self.portal, 'portal_types')
    #     content = tool.getTypeInfo('Folder')
    #     self.assertFalse(content.global_allow)

    # def test_Document__global_allow(self):
    #     tool = getToolByName(self.portal, 'portal_types')
    #     content = tool.getTypeInfo('Document')
    #     self.assertFalse(content.global_allow)

    def test_calendar_firstweekday(self):
        ctool = getToolByName(self.portal, 'portal_calendar')
        self.assertEqual(ctool.firstweekday, 0)

    def test_Member_folder_exclude_from_nav(self):
        folder = self.portal['Members']
        self.assertTrue(folder.exclude_from_nav())

    # def test_news_folder_removed(self):
    #     self.assertRaises(KeyError, lambda: self.portal['news'])

    # def test_events_folder_removed(self):
    #     self.assertRaises(KeyError, lambda: self.portal['events'])

    # def test_videot_folder(self):
    #     folder = self.portal['videot']
    #     self.assertEqual(folder.Title(), 'Videot')
    #     self.assertTrue(folder.exclude_from_nav)
    #     from abita.policy.setuphandlers import PERMISSIONS
    #     permissions = PERMISSIONS.copy()
    #     ctype = 'file'
    #     self.assertEqual(
    #         len(self.checkRoles(folder, PERMISSIONS[ctype])),
    #         1
    #     )
    #     del permissions[ctype]
    #     for perm in permissions:
    #         self.assertFalse(
    #             self.checkRoles(folder, permissions[perm])
    #         )

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

    def test_roles__Manage_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage portlets',
                self.portal
            )
        )

    def test_roles__Manage_Events_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage Events portlets',
                self.portal
            )
        )

    def test_roles__Manage_Login_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage Login portlets',
                self.portal
            )
        )

    def test_roles__Manage_Navigation_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage Navigation portlets',
                self.portal
            )
        )

    def test_roles__Manage_QuickUpload_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage QuickUpload portlets',
                self.portal
            )
        )

    def test_roles__Manage_RSS_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage RSS portlets',
                self.portal
            )
        )

    def test_roles__Manage_Recent_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage Recent portlets',
                self.portal
            )
        )

    def test_roles__Manage_Review_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage Review portlets',
                self.portal
            )
        )

    def test_roles__Manage_Search_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'Portlets: Manage Search portlets',
                self.portal
            )
        )

    def test_roles__Manage_Collection_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'plone.portlet.collection: Add collection portlet',
                self.portal
            )
        )

    def test_roles__Manage_Static_portlets(self):
        from AccessControl.PermissionRole import rolesForPermissionOn
        self.assertTrue(
            'Editor' in rolesForPermissionOn(
                'plone.portlet.static: Add static portlet',
                self.portal
            )
        )

    def test_dependencies_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        # self.failUnless(installer.isProductInstalled('abita.theme'))
        self.failUnless(installer.isProductInstalled('PloneFormGen'))
