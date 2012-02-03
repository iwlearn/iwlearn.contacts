from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _

class IAdrView(Interface):
    """
    Adr view interface
    """

class AdrView(BrowserView):
    """
    Adr browser view
    """
    implements(IAdrView)

    render = ViewPageTemplateFile('adrview.pt')

    def po_box(self):
        addr = self.context.getAddress()
        if addr:
            if addr.startswith('P.O.'):
                return addr
        return None

    def street(self):
        addr = self.context.getAddress()
        if addr:
            if addr.startswith('P.O.'):
                return None
            else:
                return addr
        return None

    def country(self):
        c = self.context.getCountry()
        if c:
            return c[0]


    def __call__(self):
        return self.render()


