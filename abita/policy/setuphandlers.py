from Products.CMFCore.utils import getToolByName


def setUpMembersFolder(context):
    portal = context.getSite()
    members = portal.get('Members')
    if members and not members.exclude_from_nav():
        log = context.getLogger(__name__)
        members.setExcludeFromNav(True)
        members.reindexObject(idxs=['exclude_from_nav'])
        log.info('Member folder excluded from navigation.')


def set_global_allow(context, name, state=True):
    portal = context.getSite()
    tool = getToolByName(portal, 'portal_types')
    content = tool.getTypeInfo(name)
    if content.global_allow != state:
        content.global_allow = state
        log = context.getLogger(__name__)
        message = 'global_allow for {0} is set to {1}'.format(
            content.getId(), state)
        log.info(message)


def set_firstweekday(context):
    portal = context.getSite()
    tool = getToolByName(portal, 'portal_calendar')
    if tool.firstweekday != 0:
        tool.firstweekday = 0
        log = context.getLogger(__name__)
        log.info('Starting weekday for calendar is set to Monday.')


def exclude_from_nav(context, content):
    if not hasattr(content, 'exclude_from_nav'):
        log = context.getLogger(__name__)
        setattr(content, 'exclude_from_nav', True)
        content.reindexObject(idxs=['exclude_from_nav'])
        message = 'Folder "{0}" excluded from navigation.'.format(content.id)
        log.info(message)


# def createFolder(context, id, title=None, exclude=True, limits=None):
#     portal = context.getSite()
#     folder = portal.get(id)
#     if not folder:
#         title = title or id.capitalize()
#         folder = portal[
#             portal.invokeFactory(
#                 'Folder',
#                 id,
#                 title=title,
#             )
#         ]
#         log = context.getLogger(__name__)
#         message = 'Folder "{0}" created.'.format(id)
#         log.info(message)
#         if exclude:
#             exclude_from_nav(context, folder)
#         if limits:
#             if isinstance(limits, str):
#                 limits = [limits]
#             permissions = PERMISSIONS.copy()
#             for limit in limits:
#                 del permissions[limit]
#             for key in permissions:
#                 perm = PERMISSIONS[key]
#                 folder.manage_permission(perm)
#                 message = 'Folder "{0}" now has no roles for permission "{1}".'.format(
#                     id,
#                     perm
#                 )
#                 log.info(message)


def setupVarious(context):

    if context.readDataFile('abita.policy_various.txt') is None:
        return

    setUpMembersFolder(context)

    # createFolder(context, 'kuvat', limits='image')
    # createFolder(context, 'tiedostot', limits='file')
    # createFolder(context, 'lomakkeet', limits='form')
    # createFolder(context, 'videot', limits='file')

    # set_global_allow(context, 'Topic', state=False)
    # set_global_allow(context, 'News Item', state=False)
    # set_global_allow(context, 'Event', state=False)
    # set_global_allow(context, 'Folder', state=False)
    # set_global_allow(context, 'Document', state=False)
    set_firstweekday(context)
