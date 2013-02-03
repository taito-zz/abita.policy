from Products.CMFCore.utils import getToolByName


def removeObjFromPortalRoot(context, objid):
    portal = context.getSite()
    if portal.get(objid):
        portal.manage_delObjects([objid])
        log = context.getLogger(__name__)
        message = '{0} removed.'.format(objid)
        log.info(message)


def exclude_from_nav(context, id):
    portal = context.getSite()
    folder = portal.get(id)
    if folder and not folder.exclude_from_nav():
        log = context.getLogger(__name__)
        folder.setExcludeFromNav(True)
        folder.reindexObject(idxs=['exclude_from_nav'])
        message = 'Folder "{0}" excluded from navigation.'.format(id)
        log.info(message)


def set_firstweekday(context):
    portal = context.getSite()
    tool = getToolByName(portal, 'portal_calendar')
    if tool.firstweekday != 0:
        tool.firstweekday = 0
        log = context.getLogger(__name__)
        log.info('Starting weekday for calendar is set to Monday.')


def uninstall_package(context, packages):
    """Uninstall packages.

    :param packages: List of package names.
    :type packages: list
    """
    portal = context.getSite()
    installer = getToolByName(portal, 'portal_quickinstaller')
    packages = [
        package for package in packages if installer.isProductInstalled(package)
    ]
    installer.uninstallProducts(packages)


def setupVarious(context):

    if context.readDataFile('abita.policy_various.txt') is None:
        return

    removeObjFromPortalRoot(context, 'front-page')
    exclude_from_nav(context, 'Members')
    exclude_from_nav(context, 'events')

    set_firstweekday(context)
    uninstall_package(context, ['plonetheme.classic'])
