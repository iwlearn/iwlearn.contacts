from datetime import datetime
import logging
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
import csv

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _

logger = logging.getLogger(__name__)

class IExportCSVView(Interface):
    """
    ExportCSV view interface
    """

    def test():
        """ test method"""


class ExportCSVView(BrowserView):
    """
    ExportCSV browser view
    """
    implements(IExportCSVView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()




class ExportPersonsCSVView(ExportCSVView):

    CSV_FIELDS =['salutation', 'firstname', 'lastname', 'jobtitle',
        'address', 'po_box', 'city', 'misc', 'zipcode', 'country',
        'email', 'remote_url', 'phone', 'fax', 'body',
         'organization', 'department', 'projectids', 'projecttitles',]


    def __call__(self):
        """
        return a CSV Representation of the data in the projectdb
        """
        output = StringIO()
        fieldnames = self.CSV_FIELDS
        writer = csv.DictWriter(output, fieldnames)
        brains = self.portal_catalog(portal_type='ContactPerson', portal_state='published')
        pd = {}
        for field in fieldnames:
            pd[field] = field
        writer.writerow(pd)
        for brain in brains:
            pd = {}
            logger.debug(brain.Title)
            obj = brain.getObject()
            pd['salutation']= obj.getSalutation()
            pd['firstname']= obj.getFirstname()
            pd['lastname']= obj.getLastname()
            pd['jobtitle']= obj.getJobtitle()
            pd['address']= obj.getAddress()
            pd['po_box']= obj.getPo_box()
            pd['city']= obj.getCity()
            pd['misc']= obj.getMisc()
            pd['zipcode']= obj.getZipcode()
            if obj.getCountry():
                pd['country']= obj.getCountry()[0]
            else:
                pd['country']= ''
            pd['email']= obj.getEmail()
            pd['remote_url']= obj.getRemoteUrl()
            pd['phone']= obj.getPhone()
            pd['fax']= obj.getFax()
            pd['body']= obj.getBody()
            if obj.getOrganization():
                pd['organization']= obj.getOrganization().Title()
            else:
                pd['organization'] = ''
            pd['department']= obj.getDepartment()
            projectids = []
            projecttitles = []
            for project in obj.getProjects():
                projectids.append(project.getGef_project_id())
                projecttitles.append(project.Title())
            pd['projectids']= '; '.join(projectids)
            pd['projecttitles']= '; '.join(projecttitles)
            writer.writerow(pd)
        output.seek(0)
        self.request.RESPONSE.setHeader('Content-Type','text/csv; charset=utf-8')
        filename = datetime.now().strftime('Contact_Persons_%Y-%m-%d.csv')
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s"' % filename)
        return output.read()
