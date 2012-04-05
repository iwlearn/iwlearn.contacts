"""Definition of the ContactOrganization content type
"""

from zope.interface import implements
#from plone.app.blob.field import ImageField

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATBackRef import backref

from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactOrganization
from iwlearn.contacts.config import PROJECTNAME
from iwlearn.contacts.content.address import AddressSchema


ContactOrganizationSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-


    atapi.ImageField('logo_image',
        max_size = (64,64),
        widget=atapi.ImageWidget(label=_(u'Logo'),
                        description=_(u'The organizations logo'),
                    ),
        validators=('isNonEmptyFile'),
    ),


)) + AddressSchema.copy() + atapi.Schema((

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
        allowed_types=('Project',),
        multiValued=True,
    ),


    backref.BackReferenceField(
        'projectpartner',
        widget=backref.BackReferenceBrowserWidget(
            label=_(u"Partner of projects"),
            description=_(u"Projects this organization is partnering with"),
        ),
        relationship='other_partner_project',
        allowed_types=('Project',),
    ),

))


schemata.finalizeATCTSchema(ContactOrganizationSchema, moveDiscussion=False)


class ContactOrganization(base.ATCTContent):
    """Organizaton"""
    implements(IContactOrganization)

    meta_type = "ContactOrganization"
    schema = ContactOrganizationSchema



atapi.registerType(ContactOrganization, PROJECTNAME)
