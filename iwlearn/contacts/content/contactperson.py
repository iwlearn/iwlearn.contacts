"""Definition of the ContactPerson content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATExtensions.widget.url import UrlWidget
from Products.ATExtensions.widget.email import EmailWidget


from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactPerson
from iwlearn.contacts.config import PROJECTNAME

ContactPersonSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ComputedField(
        'title',
        searchable=True,
        accessor='Title'
        widget=atapi.ComputedWidget(
            label=_(u"Name"),
            description=_(u"Full name"),
            
        ),
        expression = 'context._computeTitle()',
    ),


    atapi.StringField(
        'salutation',
        searchable=False,
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title"),
            description=_(u"Salutation (Mrs., Mr.) or academical title (Dr, ...)"),
        ),
    ),


    atapi.StringField(
        'firstname',
        searchable=False,
        required=True,
        widget=atapi.StringWidget(
            label=_(u"First name"),
            description=_(u"First and middle name(s)"),
        ),
        required=True,
    ),


    atapi.StringField(
        'lastname',
        searchable=False,
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Last name"),
            description=_(u"Last name"),
        ),
    ),


    atapi.StringField(
        'jobtitle',
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u"Job title"),
            description=_(u"Job title"),
        ),
    ),


    atapi.StringField(
        'address',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Address"),
            description=_(u"Street address or PO box"),
        ),
    ),


    atapi.StringField(
        'city',
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u"City"),
            description=_(u"City"),
        ),
    ),


    atapi.StringField(
        'zipcode',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Zip code"),
            description=_(u"Postal code"),
        ),
    ),


    atapi.StringField(
        'misc',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Extra address information"),
            description=_(u"Extra address information"),
        ),
    ),


    atapi.LinesField(
        'country'
        searchable=True,,
        widget=atapi.LinesWidget(
            label=_(u"Country"),
            description=_(u"Country"),
        ),
    ),


    atapi.ReferenceField(
        'organization',
        widget=atapi.ReferenceWidget(
            label=_(u"Organization"),
            description=_(u"The persons organization of employment"),
        ),
        relationship='contactperson_organization',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.StringField(
        'department',
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u"Department"),
            description=_(u"The organization department"),
        ),
    ),


    atapi.StringField(
        'email',
        searchable=True,
        widget=EmailWidget(
            label=_(u"e-mail"),
            description=_(u"e-mail address"),
        ),
         validators=('isEmail'),
    ),


    atapi.StringField(
        'remote_url',
        searchable=False,
        widget=UrlWidget(
            label=_(u"Web Address"),
            description=_(u"Website Address"),
        ),
        validators=('isURL'),
    ),


    atapi.StringField(
        'phone',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Phone"),
            description=_(u"Office phone number"),
        ),
        validators=('isInternationalPhoneNumber'),
    ),


    atapi.StringField(
        'mobile',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Mobile phone"),
            description=_(u"Mobile phone number"),
        ),
        validators=('isInternationalPhoneNumber'),
    ),


    atapi.StringField(
        'fax',
        searchable=False,
        widget=atapi.StringWidget(
            label=_(u"Fax"),
            description=_(u"Fax"),
        ),
        validators=('isInternationalPhoneNumber'),
    ),


    atapi.TextField(
        'body',
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"Body text"),
            description=_(u"Body text"),
        ),
        validators=('isTidyHtmlWithCleanup'),
    ),


    atapi.ReferenceField(
        'projects',
        widget=atapi.ReferenceWidget(
            label=_(u"Projects"),
            description=_(u"Projects of this person"),
        ),
        relationship='persons_project_contacts',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
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
        return self.getSalutation + ' ' +\
                self.getFirstname + ' ' + self.getLastname


atapi.registerType(ContactPerson, PROJECTNAME)
