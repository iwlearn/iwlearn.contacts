"""Definition of the ContactGroup content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATExtensions.widget.url import UrlWidget
from Products.ATExtensions.widget.email import EmailWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget


from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactGroup
from iwlearn.contacts.config import PROJECTNAME

ContactGroupSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'body',
        widget=atapi.RichWidget(
            label=_(u"Body text"),
            description=_(u"Body text"),
        ),
        validators=('isTidyHtmlWithCleanup'),
    ),

    atapi.StringField(
        'email',
        widget=EmailWidget(
            label=_(u"Group e-mail"),
            description=_(u"E-mail address of the group (mailing list)"),
        ),
        validators=('isEmail'),
    ),


    atapi.StringField(
        'remote_url',
        widget=UrlWidget(
            label=_(u"Web"),
            description=_(u"Web address of the groups activities"),
        ),
        validators=('isURL'),
    ),

    atapi.ReferenceField(
        'persons',
        widget=ReferenceBrowserWidget(
            label=_(u"Members"),
            description=_(u"Members of the group"),
        ),
        relationship='contactgroup_persons',
        allowed_types=('ContactPerson',), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


))


schemata.finalizeATCTSchema(ContactGroupSchema, moveDiscussion=False)


class ContactGroup(base.ATCTContent):
    """Contact Group"""
    implements(IContactGroup)

    meta_type = "ContactGroup"
    schema = ContactGroupSchema



atapi.registerType(ContactGroup, PROJECTNAME)
