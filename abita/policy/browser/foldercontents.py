from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import isExpired
from Products.CMFPlone.utils import pretty_title_or_id
from Products.CMFPlone.utils import safe_unicode
from plone.app.content.browser.foldercontents import FolderContentsKSSView
from plone.app.content.browser.foldercontents import FolderContentsTable
from plone.app.content.browser.foldercontents import FolderContentsView
from zope.component import getMultiAdapter
from zope.i18n import translate

import urllib


class FolderContentsTable(FolderContentsTable):

    pagesize = 100

    def __init__(self, context, request, contentFilter=None):
        super(self.__class__, self).__init__(context, request, contentFilter)
        self.table.pagesize = self.pagesize

    def folderitems(self):
        """
        """
        context = aq_inner(self.context)
        plone_utils = getToolByName(context, 'plone_utils')
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        plone_layout = getMultiAdapter((context, self.request), name=u'plone_layout')
        portal_workflow = getToolByName(context, 'portal_workflow')
        portal_properties = getToolByName(context, 'portal_properties')
        portal_types = getToolByName(context, 'portal_types')
        site_properties = portal_properties.site_properties

        use_view_action = site_properties.getProperty('typesUseViewActionInListings', ())
        browser_default = plone_utils.browserDefault(context)

        contentsMethod = self.contentsMethod()

        show_all = self.request.get('show_all', '').lower() == 'true'
        pagesize = self.pagesize
        pagenumber = int(self.request.get('pagenumber', 1))
        start = (pagenumber - 1) * pagesize
        end = start + pagesize

        results = []
        for i, obj in enumerate(contentsMethod(self.contentFilter)):
            path = obj.getPath or "/".join(obj.getPhysicalPath())

            # avoid creating unnecessary info for items outside the current
            # batch;  only the path is needed for the "select all" case...
            if not show_all and not start <= i < end:
                results.append(dict(path=path))
                continue

            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"

            url = obj.getURL()
            icon = plone_layout.getIcon(obj)
            type_class = 'contenttype-' + plone_utils.normalizeString(
                obj.portal_type)

            review_state = obj.review_state
            state_class = 'state-' + plone_utils.normalizeString(review_state)
            relative_url = obj.getURL(relative=True)

            fti = portal_types.get(obj.portal_type)
            if fti is not None:
                type_title_msgid = fti.Title()
            else:
                type_title_msgid = obj.portal_type
            url_href_title = u'%s: %s' % (translate(type_title_msgid,
                                                    context=self.request),
                                          safe_unicode(obj.Description))

            modified = plone_view.toLocalizedTime(
                obj.ModificationDate, long_format=1)

            if obj.portal_type in use_view_action:
                view_url = url + '/view'
            elif obj.is_folderish:
                view_url = url + "/folder_contents"
            else:
                view_url = url

            is_browser_default = len(browser_default[1]) == 1 and (
                obj.id == browser_default[1][0])

            results.append(dict(
                # provide the brain itself to allow cleaner customisation of
                # the view.
                #
                # this doesn't add any memory overhead, a reference to
                # the brain is already kept through its getPath bound method.
                brain=obj,
                url=url,
                url_href_title=url_href_title,
                id=obj.getId,
                quoted_id=urllib.quote_plus(obj.getId),
                path=path,
                title_or_id=safe_unicode(pretty_title_or_id(plone_utils, obj)),
                obj_type=obj.Type,
                size=obj.getObjSize,
                modified=modified,
                icon=icon.html_tag(),
                type_class=type_class,
                wf_state=review_state,
                state_title=portal_workflow.getTitleForStateOnType(review_state,
                                                                 obj.portal_type),
                state_class=state_class,
                is_browser_default=is_browser_default,
                folderish=obj.is_folderish,
                relative_url=relative_url,
                view_url=view_url,
                table_row_class=table_row_class,
                is_expired=isExpired(obj),
            ))
        return results


class FolderContentsView(FolderContentsView):

    def contents_table(self):
        table = FolderContentsTable(aq_inner(self.context), self.request)
        return table.render()


class FolderContentsKSSView(FolderContentsKSSView):
    table = FolderContentsTable
