from Products.CMFCore.utils import getToolByName


# def setUpMembersFolder(context):
#     portal = context.getSite()
#     members = portal.get('Members')
#     if members and not members.exclude_from_nav():
#         log = context.getLogger(__name__)
#         members.setExcludeFromNav(True)
#         members.reindexObject(idxs=['exclude_from_nav'])
#         log.info('Member folder excluded from navigation.')

def exclude_from_nav(context, id):
    portal = context.getSite()
    folder = portal.get(id)
    if folder and not folder.exclude_from_nav():
        log = context.getLogger(__name__)
        folder.setExcludeFromNav(True)
        folder.reindexObject(idxs=['exclude_from_nav'])
        message = 'Folder "{0}" excluded from navigation.'.format(id)
        log.info(message)


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


def createFolder(context, id, title=None, exclude=True):
    portal = context.getSite()
    folder = portal.get(id)
    if not folder:
        title = title or id.capitalize()
        folder = portal[
            portal.invokeFactory(
                'Folder',
                id,
                title=title,
                language='',
            )
        ]
        log = context.getLogger(__name__)
        message = 'Folder "{0}" created.'.format(id)
        log.info(message)
        if exclude:
            exclude_from_nav(context, folder)


def setNewsFolder(context):
    portal = context.getSite()
    folder = portal.get('news')
    if folder.Title() != 'News':
        folder.setTitle('News')
        folder.reindexObject(idxs=['title'])
    if folder.Description() != '':
        folder.setDescription('')
        folder.reindexObject(idxs=['description'])
    if folder.Language() != '':
        folder.setLanguage('')
        folder.reindexObject(idxs=['language'])


def setupVarious(context):

    if context.readDataFile('abita.policy_various.txt') is None:
        return

    exclude_from_nav(context, 'Members')
    exclude_from_nav(context, 'events')
    setNewsFolder(context)
    createFolder(context, 'topics', exclude=False)
    createFolder(context, 'services', exclude=False)
    createFolder(context, 'applications', exclude=False)
    createFolder(context, 'company', exclude=False)
    createFolder(context, 'contact', exclude=False)

    set_firstweekday(context)
