# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES

# The profile id of your package:
PROFILE_ID = 'profile-iwlearn.contacts:default'
TYPES_TO_VERSION = ('ContactPerson','ContactOrganization', 'ContactGroup')

def setVersionedTypes(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('iwlearn.contacts')
    portal_repository = getToolByName(context, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())
    for type_id in TYPES_TO_VERSION:
        if type_id not in versionable_types:
            # use append() to make sure we don't overwrite any
            # content-types which may already be under version control
            logger.info('Adding %s to versionable types' % type_id)
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)

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


