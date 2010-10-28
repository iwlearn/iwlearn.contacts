"""Common configuration constants
"""

PROJECTNAME = 'iwlearn.contacts'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'ContactPerson': 'iwlearn.contacts: Add ContactPerson',
    'ContactOrganization': 'iwlearn.contacts: Add ContactOrganization',
    'ContactGroup': 'iwlearn.contacts: Add ContactGroup',
    'ContactDb': 'iwlearn.contacts: Add ContactDb',
}

PRODUCT_DEPENDENCIES = ('ATBackRef','ATExtensions')
