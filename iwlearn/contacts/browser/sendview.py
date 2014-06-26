from zope.interface import implements, Interface
from DateTime import DateTime

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactOrganization, IContactGroup
from iwlearn.contacts.content.mailto import isNamedEmail

import logging

log = logging.getLogger("iwlearn.contacts")


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
    render = ViewPageTemplateFile('sendview.pt')
    mailto = ''
    max_mails=1

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
        rd['plaintextbody'] = recipient.getBody(mimetype="text/plain")
        rd['url'] = recipient.absolute_url()
        return rd

    def send_mail(self, mailto=None, maxsend=None):
        """
        """
        if mailto:
            if not isNamedEmail(mailto):
                putils.addPortalMessage( 'Invalid mailto address')
                return
        else:
            self.context.setSenddate(DateTime())
        template = self.context.getText()
        mFrom=self.context.getSender()
        mail_subject=self.context.Title()
        putils = getToolByName(self.context, "plone_utils")
        mail_host = getToolByName(self, 'MailHost')
        i = 0
        for recipient in self.get_recipients():
            if maxsend:
                if i > maxsend:
                    break
            i +=1
            message = template % self.get_recipient_details(recipient)
            if mailto:
                # send test email to mailto
                mTo = mailto
                mSubj = mail_subject
            else:
                if isNamedEmail(recipient.getEmail()):
                    mTo = recipient.getEmail()
                    mSubj = mail_subject
                else:
                    mTo = mFrom
                    mSubj = mail_subject + ' -- invalid email address'
            try:
                 mail_host.send(message, mTo, mFrom, mSubj)
                 #print  mTo, mFrom, mSubj, message
                 log.info("Send email to \"%s\"" % mTo)
            except Exception, e:
                 # Don't disclose email address on failure
                 log.info("Sending mail to \"%s\" failed, with error \"%s\"!" % (mTo, e))
        putils.addPortalMessage("%d mails have been sent." % i )
        return self.request.response.redirect(self.context.absolute_url())


    def __call__(self):
        form = self.request.form
        if form.get('test', None):
            self.mailto = form.get('mailto_addr', None)
            if isNamedEmail(self.mailto):
                try:
                    self.max_mails = abs(int(self.request.get('max_mails', '1')))
                except ValueError:
                    self.max_mails=1
                return self.send_mail(self.mailto, self.max_mails)
            else:
                putils = getToolByName(self.context, "plone_utils")
                putils.addPortalMessage( 'Invalid mailto address')
        elif form.get('send', None):
            return self.send_mail()
        return self.render()


