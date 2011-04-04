"""Definition of the MailTo content type
"""

from zope.interface import implements

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from iwlearn.contacts import contactsMessageFactory as _

from iwlearn.contacts.interfaces import IMailTo
from iwlearn.contacts.config import PROJECTNAME



MailToSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'sender',
        widget=atapi.StringWidget(
            label=_(u"From address"),
            description=_(u"Address of sender"),
        ),
        required=True,
        validators=('isEmail'),
    ),


    atapi.ReferenceField(
        'recipients',
        widget=ReferenceBrowserWidget(
            label=_(u"Recipients"),
            description=_(u"All members of these groups or organizations will be mailed, leave empty to mail to ALL contact persons"),
        ),
        relationship='mailto_recipients',
        allowed_types=('ContactGroup', 'ContactOrganization'), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.TextField(
        'text',
        widget=atapi.TextAreaWidget(
            label=_(u"Mail message"),
            description=_(u"Enter the text to be sent to all recipients"),
        ),
        required=True,
        default=u"""Dear %(fullname)s

In our contact database we have the following information about you:
Title:                      %(salutation)s
First name:                 %(firstname)s
Last name:                  %(lastname)s
Job title:                  %(jobtitle)s
Address:                    %(address)s
City:                       %(city)s
Postal code:                %(zipcode)s
Extra address information:  %(misc)s
Country:                    %(country)s
Organization:               %(organization)s
Department:                 %(department)s
e-mail address:             %(email)s
Website Address:            %(remote_url)s
Phone:                      %(phone)s
Mobile phone:               %(mobile)s
Fax:                        %(fax)s

        """,
    ),


))



schemata.finalizeATCTSchema(MailToSchema, moveDiscussion=False)


class MailTo(base.ATCTContent):
    """Mail to a group of persons"""
    implements(IMailTo)

    meta_type = "MailTo"
    schema = MailToSchema




atapi.registerType(MailTo, PROJECTNAME)
