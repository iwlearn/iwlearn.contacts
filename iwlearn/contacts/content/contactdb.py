"""Definition of the ContactDb content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from iwlearn.contacts import contactsMessageFactory as _
from iwlearn.contacts.interfaces import IContactDb
from iwlearn.contacts.config import PROJECTNAME

ContactDbSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))




schemata.finalizeATCTSchema(
    ContactDbSchema,
    folderish=True,
    moveDiscussion=False
)


class ContactDb(folder.ATFolder):
    """Contact Database"""
    implements(IContactDb)

    meta_type = "ContactDb"
    schema = ContactDbSchema



    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(ContactDb, PROJECTNAME)
