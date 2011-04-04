from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactOrganization, IContactGroup

from Products.validation.validators.BaseValidators import baseValidators

for v in baseValidators:
    if v.name == 'isEmail':
        isEmail = v

class ISendView(Interface):
    """
    Send view interface
    """

    def test():
        """ test method"""


class SendView(BrowserView):
    """
    Send browser view
    """
    implements(ISendView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_recipients(self):
        recipients = []
        if self.context.getRecipients():
            for pg in self.context.getRecipients():
                if IContactGroup.providedBy(pg):
                    recipients += pg.getPersons()
                elif IContactOrganization.providedBy(pg):
                    recipients += pg.getContactpersons()
        else:
            brains = self.portal_catalog(portal_type='ContactPerson')
            for brain in brains:
                recipients.append(brain.getObject())

        return recipients


    def get_recipient_details(self, recipient):
        ''' return a dictionary with the details of the recipient'''
        #rd = {}
        rd = {'fullname': recipient.Title()}
            #'salutation': recipient.getSalutation(),
            #'firstname': recipient.getForstname()
            #'lastname': recipient.getLastname(),
            #'jobtitle':
            #'address':
            #'city':
            #'zipcode':
            #'misc':
            #'country':
            #'organization':
            #'department':
            #'email'
            #'remote_url':
            #'phone':
            #'mobile'
            #'fax'
            #'projects'
        for k in recipient.schema.keys():
            a = recipient.schema._fields.get(k).accessor
            rd[k] = str(getattr(recipient, a)())
        if recipient.getOrganization():
            rd ['organization'] = recipient.getOrganization().Title()
        if recipient.getCountry():
            rd['country'] =  recipient.getCountry()[0]
        return rd

    def send_mail(self):
        """
        """
        template = self.context.getText()
        mFrom=self.context.getSender()
        mail_subject=self.context.Title()
        putils = getToolByName(self.context, "plone_utils")
        mail_host = getToolByName(self, 'MailHost')
        for recipient in self.get_recipients():
            message = template % self.get_recipient_details(recipient)
            if isEmail(recipient.getEmail()):
                mTo = recipient.getEmail()
                mSubj = mail_subject
            else:
                mTo = mFrom
                mSubj = mail_subject + ' -- invalid email address'
            try:
                 mail_host.send(message, mTo, mFrom, mSubj)
                 #print  mTo, mFrom, mSubj, message
            except SMTPRecipientsRefused:
                 # Don't disclose email address on failure
                 raise SMTPRecipientsRefused('Recipient address rejected by server')

        putils.addPortalMessage(_("The mails have been send."))
        return self.request.response.redirect(self.context.absolute_url())


    def __call__(self):
        self.send_mail()

        return 'done'


