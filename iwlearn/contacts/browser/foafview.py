import hashlib
import DateTime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _

from collective.geo.contentlocations.interfaces import IGeoManager

class IFOAFView(Interface):
    """
    FOAF view interface
    """



class FOAFView(BrowserView):
    """
    FOAF browser view
    """
    implements(IFOAFView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def mbox_sha1sum(self):
        if self.context.getEmail():
            mbox = self.context.getEmail().strip().lower()
            return hashlib.sha1('mailto:' + mbox).hexdigest()

    def country(self):
        c = self.context.getCountry()
        if c:
            return c[0]



class FOAFPersonView(FOAFView):
    """
    FOAF person browser view
    """

    def get_projects(self):
        projects = self.context.getProjects()
        for p in projects:
            project = {'url': p.absolute_url() + '/@@rdf',
                        'current' : True,
                        'past': False}
            if p.getEnd_date():
                if p.getEnd_date() < DateTime.DateTime():
                    project = {'url': p.absolute_url() + '/@@rdf',
                        'current' : False,
                        'past': True}
            yield project

    def get_organization(self):
        org = self.context.getOrganization()
        if org:
            return org.absolute_url() + '/@@foaf.rdf'



class FOAFOrgView(FOAFView):
    """
    FOAF Organization browser view
    """
    def get_projects(self):
        projects = []
        if self.context.getProjectlead():
            projects += list(self.context.getProjectlead())
        if self.context.getProjectimplementing():
            projects += list(self.context.getProjectimplementing())
        if self.context.getProjectexecuting():
            projects += list(self.context.getProjectexecuting())
        if self.context.getProjectpartner():
            projects += list(self.context.getProjectpartner())
        for project in projects:
            yield project.absolute_url() + '/@@rdf'

    def get_persons(self):
        persons = self.context.getContactpersons()
        for person in persons:
            yield person.absolute_url() + '/@@foaf.rdf'


    def get_latlon(self):
        geo = IGeoManager(self.context)
        geom = geo.getCoordinates()
        if geom:
            if geom[0] == 'Point':
                return '<geo:Point geo:lat="%f" geo:long="%f"/>' % (
                    geom[1][1], geom[1][0])


class FOAFDbView(FOAFView):
    """
    Organizations and persons in a single foaf.rdf file
    """

    def get_persons(self):
        results = self.portal_catalog(portal_type='ContactPerson')
        return results

    def get_organizations(self):
        results = self.portal_catalog(portal_type='ContactOrganization')
        return results


