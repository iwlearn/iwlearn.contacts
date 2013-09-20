from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _


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
         'organization', 'department', 'projectids', 'projecttitles',]


        def __call__(self):
        """
        return a CSV Representation of the data in the projectdb
        """
        output = StringIO()
        fieldnames = self.CSV_FIELDS
        writer = csv.DictWriter(output, fieldnames)
        form = self.request.form
        query = get_query(form)
        brains = self.portal_catalog(**query)
        pd = {}
        for field in fieldnames:
            pd[field] = field
        writer.writerow(pd)

        for brain in brains:
            pd = {}
            obj = brain.getObject()
            pd['salutation']= obj.getSalutation()
            pd['firstname']= obj.getFirstname()
            pd['lastname']= obj.getLastname()
            pd['jobtitle']= obj.getJobtitle()
            pd['organization']= obj.getOrganization().Title()
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
