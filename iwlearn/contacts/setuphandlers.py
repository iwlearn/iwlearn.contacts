# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
# The profile id of your package:
PROFILE_ID = 'profile-iwlearn.contacts:default'

def reindex_contacts(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.project')
    setup = getToolByName(context, 'portal_setup')
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(portal_type=['ContactPerson', 'ContactOrganization',
        'ContactGroup'])
    for brain in brains:
        obj = brain.getObject()
        logger.info('reindex: %s' % '/'.join(obj.getPhysicalPath()))
        obj.reindexObject()


def setupVarious(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('iwlearn.contacts_various.txt') is None:
        return
    logger = context.getLogger('iwlearn.contacts')
    site = context.getSite()
    # Add additional setup code here

