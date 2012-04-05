#

from Products.Archetypes import atapi

from Products.ATExtensions.widget.url import UrlWidget
from Products.ATExtensions.widget.email import EmailWidget

from iwlearn.contacts import vocabulary
from iwlearn.contacts import contactsMessageFactory as _

AddressSchema = atapi.Schema((

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

))

