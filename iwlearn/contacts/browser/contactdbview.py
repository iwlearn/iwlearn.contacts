from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _


class IContactDBView(Interface):
    """
    ContactDB view interface
    """




class ContactDBView(BrowserView):
    """
    ContactDB browser view
    """
    implements(IContactDBView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def getContactTypes(self):
        "Returns selected contact types "
        form = self.request.form
        contact_type = []
        if form.has_key('portal_type'):
            if 'ContactPerson' in form['portal_type']:
                contact_type.append({'name': _('Person'),
                    'ctype':'ContactPerson', 'checked': 'checked'})
            else:
                contact_type.append({'name': _('Person'),
                    'ctype':'ContactPerson', 'checked': None})

            if 'ContactOrganization' in form['portal_type']:
                contact_type.append({'name': _('Organization'),
                    'ctype': 'ContactOrganization', 'checked': 'checked'})
            else:
                contact_type.append({'name': _('Organization'),
                    'ctype': 'ContactOrganization', 'checked': None})

            if 'ContactGroup' in form['portal_type']:
                contact_type.append({'name': _('Group'),
                    'ctype': 'ContactGroup', 'checked': 'checked'})
            else:
                contact_type.append({'name': _('Group'),
                    'ctype': 'ContactGroup', 'checked': None})
            return contact_type
        else:
            return [{'name': _('Person'), 'ctype':'ContactPerson', 'checked': 'checked'},
                {'name': _('Organization'), 'ctype': 'ContactOrganization', 'checked': 'checked'},
                {'name': _('Group'), 'ctype': 'ContactGroup', 'checked': 'checked'}]

    @property
    def search_term(self):
        return self.request.form.get('SearchableText', '')

    def search_results(self):
        form = self.request.form
        is_search = len(form)!=0
        if not is_search:
            return None
        catalog = self.portal_catalog
        ctype = form.get('portal_type', None)
        batch_size = form.get('b_size', 20)
        batch_start = form.get('b_start', 0)
        is_search = len(form)!=0
        if ctype is None:
            ctype=['ContactPerson', 'ContactOrganization', 'ContactGroup']
        results = catalog(SearchableText=self.search_term, portal_type=ctype)
        return {'results': results, 'size': batch_size, 'start': batch_start}


