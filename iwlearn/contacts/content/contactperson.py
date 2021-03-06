"""Definition of the ContactPerson content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATBackRef import backref
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget


from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactPerson
from iwlearn.contacts.config import PROJECTNAME
from iwlearn.contacts.content.address import AddressSchema

ContactPersonSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ComputedField(
        'title',
        searchable=True,
        accessor='Title',
        widget=atapi.ComputedWidget(
            label=_(u"Name"),
            description=_(u"Full name"),
            visible={'edit': 'invisible', 'view': 'invisible'},

        ),
        expression = 'context._computeTitle()',
    ),


    atapi.ComputedField(
        'description',
        searchable=True,
        accessor='Description',
        widget=atapi.ComputedWidget(
            label=_(u"Description"),
            description=_(u"Used in item listings and search results."),
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
        expression = 'context._computeDescription()',
    ),


    atapi.StringField(
        'salutation',
        searchable=False,
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title"),
            description=_(u"Salutation (Mrs., Mr.) or academical title (Dr, ...)"),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),


    atapi.StringField(
        'firstname',
        searchable=False,
        required=True,
        widget=atapi.StringWidget(
            label=_(u"First name"),
            description=_(u"First and middle name(s)"),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),


    atapi.StringField(
        'lastname',
        searchable=False,
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Last name"),
            description=_(u"Last name"),
            visible={'edit': 'visible', 'view': 'invisible'},
        ),
    ),


    atapi.StringField(
        'jobtitle',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Job title"),
            description=_(u"Job title"),
        ),
    ),


    atapi.ReferenceField(
        'organization',
        widget=ReferenceBrowserWidget(
            label=_(u"Organization"),
            description=_(u"The persons organization of employment"),
            allow_search =True,
            allow_sorting = True,
            allow_browse =True,
            hide_inaccessible=True,
            show_review_state=True,
            history_length=3,
        ),
        relationship='contactperson_organization',
        allowed_types=('ContactOrganization',), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.StringField(
        'department',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Department"),
            description=_(u"The organization department"),
        ),
    ),

)) + AddressSchema.copy() + atapi.Schema((

    backref.BackReferenceField(
        'projects',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"GEF IW Project Involvement"),
            description=_(u"Projects this person is involved in"),
            allow_search =True,
            allow_sorting = True,
            allow_browse =True,
            startup_directory_method='_getProjectsDirectory',
            hide_inaccessible=True,
            show_review_state=True,
            history_length=3,
        ),
        relationship='persons_project_contacts',
        allowed_types=('Project',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

    backref.BackReferenceField(
        'groups',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Groups"),
            description=_(u"Groups of this person"),
            allow_search =True,
            allow_sorting = True,
            allow_browse =True,
            hide_inaccessible=True,
            show_review_state=True,
            history_length=3,
        ),
        relationship='contactgroup_persons',
        allowed_types=('ContactGroup',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

))


schemata.finalizeATCTSchema(ContactPersonSchema, moveDiscussion=False)


class ContactPerson(base.ATCTContent):
    """Person"""
    implements(IContactPerson)

    meta_type = "ContactPerson"
    schema = ContactPersonSchema

    def _computeTitle(self):
        """Get object's title."""
        return (self.getSalutation() + ' ' +
                self.getFirstname() + ' ' +
                self.getLastname())

    def _computeDescription(self):
        """ Objects Description """
        org = self.getOrganization()
        if org is None:
            org = ''
        else:
            org = org.Title() + ', '
        return self.getJobtitle() + ', ' + org + self.getDepartment()

    def _getProjectsDirectory(self):
        """ get the path projects database """
        for brain in self.portal_catalog(
            portal_type = 'Project Database', review_state='published'):
            # return the first match found
            return brain.getPath()

atapi.registerType(ContactPerson, PROJECTNAME)
