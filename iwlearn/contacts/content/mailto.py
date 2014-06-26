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


from zope.interface import implements
from Products.validation.interfaces.IValidator import IValidator
from Products.validation.validators.BaseValidators import baseValidators

for v in baseValidators:
    if v.name == 'isEmail':
        isEmail = v


class NamedEmailValidator:
    implements(IValidator)
    def __init__(self, name):
        self.name = name
        self.title = name
        self.description = "Validate 'some name' <some@address>"

    def __call__(self, value, *args, **kwargs):
        email = value
        email = email.strip()
        if '<' in email:
            name, email = email.split('<')
            email = email.split('>')[0]
            if len(name) > 80:
                return 'Name too long'
        valid = isEmail(email)
        if not valid:
            return 'Invalid email address'
        return True

isNamedEmail = NamedEmailValidator('isNamedEmail')



MailToSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.DateTimeField(
        'senddate',
        widget=atapi.CalendarWidget(
            label=_(u"Sent at"),
            description=_(u"Date and Time this email was sent"),
            visible={'edit': 'invisible', 'view': 'visible'},
        ),
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'sender',
        widget=atapi.StringWidget(
            label=_(u"From address"),
            description=_(u"Address of sender"),
        ),
        required=True,
        validators=(NamedEmailValidator('isNamedEmail')),
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
Organization:               %(organization)s
Department:                 %(department)s
Address:                    %(address)s
P.O. Box                    %(po_box)s
City:                       %(city)s
Extra address information:  %(misc)s
Postal code:                %(zipcode)s
Country:                    %(country)s
e-mail address:             %(email)s
Website Address:            %(remote_url)s
Phone:                      %(phone)s
Fax:                        %(fax)s
Additional information:
%(plaintextbody)s

Link to record:             %(url)s
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
