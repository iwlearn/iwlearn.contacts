"""Definition of the ContactOrganization content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATExtensions.widget.url import UrlWidget
from Products.ATExtensions.widget.email import EmailWidget

from Products.ATBackRef import backref

from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactOrganization
from iwlearn.contacts.config import PROJECTNAME
from iwlearn.contacts import vocabulary

ContactOrganizationSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-


    atapi.StringField(
        'address',
        widget=atapi.StringWidget(
            label=_(u"Address"),
            description=_(u"Street address or PO box"),
        ),
    ),


    atapi.StringField(
        'city',
        widget=atapi.StringWidget(
            label=_(u"City"),
            description=_(u"City"),
        ),
    ),


    atapi.StringField(
        'misc',
        widget=atapi.StringWidget(
            label=_(u"Extra address information"),
            description=_(u"Extra address information"),
        ),
    ),


    atapi.StringField(
        'zipcode',
        widget=atapi.StringWidget(
            label=_(u"Zip code"),
            description=_(u"Postal code"),
        ),
    ),



    atapi.LinesField(
        'country',
        vocabulary = vocabulary.get_countries(),
        widget=atapi.SelectionWidget(
            label=_(u"Country"),
            description=_(u"Country"),
        ),
    ),


    atapi.StringField(
        'email',
        widget=EmailWidget(
            label=_(u"e-mail"),
            description=_(u"e-mail address"),
        ),
        validators=('isEmail'),
    ),


    atapi.StringField(
        'remote_url',
        widget=UrlWidget(
            label=_(u"Web"),
            description=_(u"Web address"),
        ),
        validators=('isURL'),
        accessor='getRemoteUrl',
    ),


    atapi.StringField(
        'phone',
        widget=atapi.StringWidget(
            label=_(u"Phone"),
            description=_(u"Phone number"),
        ),
        validators=('isInternationalPhoneNumber'),
    ),


    atapi.StringField(
        'fax',
        widget=atapi.StringWidget(
            label=_(u"Fax"),
            description=_(u"Fax No."),
        ),
        validators=('isInternationalPhoneNumber'),
    ),


    atapi.TextField(
        'body',
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Body Text"),
            description=_(u"The body text of the document"),
        ),
        validators=('isTidyHtmlWithCleanup'),
        default_content_type="text/html",
        default_output_type='text/x-html-safe',
    ),

    backref.BackReferenceField(
        'contactpersons',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Members"),
            description=_(u"Persons in this organization"),
        ),
        relationship='contactperson_organization',
        allowed_types=('ContactPerson','mxmContactsPerson'), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

   backref.BackReferenceField(
        'projectlead',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Lead Implementing"),
            description=_(u"Projects for which this organization is the lead implementing agency"),
        ),
        relationship='leadagency_project',
        allowed_types=('Project',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

    backref.BackReferenceField(
        'projectimplementing',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Implementing"),
            description=_(u"Projects for which this organization is an implementing agency"),
        ),
        relationship='other_implementing_project',
        allowed_types=('Project',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),

    backref.BackReferenceField(
        'projectexecuting',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Executing"),
            description=_(u"Projects for which this organization is an executing agency"),
        ),
        relationship='executing_agency_project',
        allowed_types=('Project',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),



))


schemata.finalizeATCTSchema(ContactOrganizationSchema, moveDiscussion=False)


class ContactOrganization(base.ATCTContent):
    """Organizaton"""
    implements(IContactOrganization)

    meta_type = "ContactOrganization"
    schema = ContactOrganizationSchema



atapi.registerType(ContactOrganization, PROJECTNAME)
