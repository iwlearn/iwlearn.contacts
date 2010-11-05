# -*- coding: utf-8 -*-
# migrate mxmContacts to iwlearn.contacts
# 1) copy this script into the parts/clientX/Extension folder
# add an external method in the zmi in the plone root
#   Module Name: migratemxm
#   Function Name: migrate
# execute the script with the test tab.
# it will create a script update_uids.py in the zopeinstance root
# 2) which you have to copy into the  parts/clientX/Extension folder
# add an external method in the zmi in the plone root
#   Module Name: update_uids
#   Function Name: migrate
# execute the script with the test tab.

from plone.i18n.locales.countries import _countrylist

COUNTRY_MAP = {
 u"africa": None,
 u"america": None,
 u"antigua barbuda": u"Antigua and Barbuda",
 u"barbados, w.i": u"Barbados",
 u"bosnia & herzegovina": u"Bosnia and Herzegovina",
 u"bosnia herzegovina": u"Bosnia and Herzegovina",
 u"brasil": u"Brazil",
 u"central african repulic": u"Central African Republic",
 u"central america": None,
 u"china,": u"China",
 u"congo, democratic republic": u"Congo The Democratic Republic of",
 u"congo, democratic republic of the": u"Congo The Democratic Republic of",
 u"country": None,
 u"fiji islands": u"Fiji",
 u"fyr macedonia": u"Macedonia the former Yugoslavian Republic of",
 u"fyr of macedonia": u"Macedonia the former Yugoslavian Republic of",
 u"geneva": u"Switzerland",
 u"guinea bissau": u"Guinea-Bissau",
 u"i.r. iran": u"Iran Islamic Republic of",
 u"iran": u"Iran Islamic Republic of",
 u"iran,": u"Iran Islamic Republic of",
 u"iran, islamic republic": u"Iran Islamic Republic of",
 u"iran, islamic republic of": u"Iran Islamic Republic of",
 u"kingdom of saudi arabia": u"Saudi Arabia",
 u"korea": u"Korea Republic of",
 u"korea, democratic people's republic": u"Korea Democratic People's Republic of",
 u"korea, democratic people's republic of": u"Korea Democratic People's Republic of",
 u"korea, republic": u"Korea Republic of",
 u"korea, republic of": u"Korea Republic of",
 u"lao pdr": u"Lao People's Democratic Republic",
 u"libya": u"Libyan Arab Jamahiriya",
 u"luxemburg": u"Luxembourg",
 u"macedonia, former yugoslav republic": u"Macedonia the former Yugoslavian Republic of",
 u"macedonia, former yugoslav republic of": u"Macedonia the former Yugoslavian Republic of",
 u"micronesia": u"Micronesia Federated States of",
 u"micronesia, federated states": u"Micronesia Federated States of",
 u"moldova": u"Moldova Republic of",
 u"moldova, republic": u"Moldova Republic of",
 u"moldova, republic of": u"Moldova Republic of",
 u"méxico": u"Mexico",
 u"northern africa": None,
 u"null": None,
 u"palestinian territory, occupied": u"Palestinian Territory occupied",
 u"pr china": u"China",
 u"republic of chad": u"Chad",
 u"republic of kazakhstan": u"Kazakhstan",
 u"republic of korea": u"Korea Republic of",
 u"russia": u"Russian Federation",
 u"saint kitts nevis": u"Saint Kitts and Nevis",
 u"saint vincent grenadines": u"Saint Vincent and the Grenadines",
 u"sao tome principe": u"Sao Tome and Principe",
 u"serbia": u"Serbia and Montenegro",
 u"serbia and montegnegro": u"Serbia and Montenegro",
 u"serbia montenegro": u"Serbia and Montenegro",
 u"slovak republic": u"Slovakia",
 u"tanzania": u"Tanzania United Republic of",
 u"tanzania, united republic": u"Tanzania United Republic of",
 u"tanzania, united republic of": u"Tanzania United Republic of",
 u"the netherlands": u"Netherlands",
 u"trinidad tobago": u"Trinidad and Tobago",
 u"tunisie": u"Tunisia",
 u"usa": u"United States",
 u"vietnam": u"Viet Nam",
 u"western africa": None,
 u"western asia": None,
 u"western europe": None,
}
for k, v in _countrylist.iteritems():
    COUNTRY_MAP[v['name'].lower()] = v['name']

def update_countries(countries):
    cl = []
    if countries:
        for country in countries:
            c = COUNTRY_MAP.get(country.lower(), None)
            if c:
                cl.append(c)
    return cl


def uniquelist(seq):
    # order preserving
    seen={}
    result = []
    for item in seq:
        if item in seen.keys(): continue
        seen[item] = 1
        result.append(item)
    return result

def migrate_metadata(old, new, old_parent, new_parent):
    new.setCreationDate(old.CreationDate())
    if old.getEffectiveDate():
        new.setEffectiveDate(old.getEffectiveDate())
    else:
        new.setEffectiveDate(old.CreationDate())
    new.setCreators(old.Creators())
    new.setModificationDate(old.ModificationDate())
    new.setSubject(old.Subject())
    uid = old.UID()
    old._uncatalogUID(old_parent)
    new._setUID(uid)


def migrate_group(old, old_parent, new_parent,f):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactGroup', new_parent, obj_id, None)
    new = new_parent[obj_id]
    new.update(title=old.Title(), description=old.Description() )
    new.SetBody(old.getText())
    migrate_metadata(old, new, old_parent, new_parent)
    old_parent.manage_delObjects(ids=[obj_id])
    print 'migrated group: ', obj_id

def migrate_person(old, old_parent, new_parent, f):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactPerson', new_parent, obj_id)
    new = new_parent[obj_id]
    new.setSalutation(old.Title())
    new.setFirstname(old.getFirstname() )
    new.setLastname(old.getLastname())
    new.setJobtitle(old.getJobtitle())
    new.setAddress(old.getAddress())
    new.setCity(old.getCity())
    new.setZipcode(old.getPo())
    new.setMisc(old.getMisc())
    countries = update_countries([old.getCountry(),])
    if countries:
        country = countries[0]
    else:
        country =''
    new.setCountry(countries)
    #reference
    new.setOrganization(old.getRawOrganization())
    new.setDepartment(old.getDepartment())
    new.setEmail(old.getEmail())
    new.setRemote_url(old.getWeb())
    new.setPhone(old.getOffice_phone())
    new.setMobile(old.getMobile_phone())
    new.setFax(old.getFax())
    new.setBody(old.getBody())
    try:
        new.setLocation(old.getCity() + ', ' + country)
    except:
        pass
    #backreference
    new.setProjects(uniquelist(old.getBRefs('Rel1')))
    #backreference
    #new.setRelatedItems([])
    print old.UID()
    f.write('    #person \n')
    f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
    if old.getRawOrganization():
        f.write('    try:\n')
        f.write('        obj.setOrganization("' + old.getRawOrganization() + '")\n')
        f.write('    except:\n')
        f.write('        print "set organization failed"\n')
    f.write('    obj.setProjects([')
    for project in new.getRawProjects():
        f.write(' "' + project + '",')
    f.write('])\n')
    migrate_metadata(old, new, old_parent, new_parent)
    old_parent.manage_delObjects(ids=[obj_id])

def migrate_organization(old, old_parent, new_parent, f):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactOrganization', new_parent, obj_id)
    new = new_parent[obj_id]
    new.update(title=old.Title())
    new.setAddress(old.getRawAddress())
    new.setCity(old.getRawCity())
    new.setMisc(old.getRawMisc())
    new.setZipcode(old.getRawPo())
    countries = update_countries([old.getCountry(),])
    if countries:
        country = countries[0]
    else:
        country =''
    new.setCountry(countries)
    new.setEmail(old.getRawEmail())
    new.setRemote_url(old.getRawWeb())
    new.setPhone(old.getRawPhone())
    new.setFax(old.getRawFax())
    new.setBody(old.getRawBody())
    city = old.getRawCity().decode('UTF8','ignore').encode('UTF8')
    try:
        new.setLocation(city + u', ' + country)
    except:
        pass
    #backreference
    new.setContactpersons(uniquelist(old.getBRefs('mxmContacts_employed_at')))
    #new.setRelatedItems([])
    f.write('    #organization \n')
    f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
    f.write('    obj.setContactpersons([')
    for person in new.getRawContactpersons():
        f.write(' "' + person + '",')
    f.write('])\n')
    migrate_metadata(old, new, old_parent, new_parent)
    old_parent.manage_delObjects(ids=[obj_id])

def migrate(self):
    print 'starting migration'
    f = open('update_contact_uids.py', 'w')
    f.write('def migrate(self):\n')
    f.write('    print "start setting uids"\n')
    f.write('    uid_tool = self.reference_catalog\n')
    for brain in self.portal_catalog(portal_type = 'mxmContacts'):
        obj=brain.getObject()
        parent = obj.getParentNode()

        if callable(obj.id):
            obj_id = obj.id()
        else:
            obj_id = obj.id
        parent.manage_renameObject(obj_id, obj_id + '_old')
        portal_types = parent.portal_types
        portal_types.constructContent('ContactDb', parent, obj_id)
        print 'created contact db: ', obj_id
        new = parent[obj_id]
        new.update(title=obj.title, description=obj.description )
        #migrate_metadata(obj, new, parent, parent)
        for child in obj.objectValues():
            if child.portal_type == 'mxmContactsGroup':
                migrate_group(child, obj, new, f)
            elif child.portal_type == 'mxmContactsOrganization':
                migrate_organization(child, obj, new, f)
            elif child.portal_type == 'mxmContactsPerson':
                migrate_person(child, obj, new, f)
            else:
                print 'ignored: ', child.portal_type, child.id
        parent.manage_delObjects(ids=[obj_id + '_old'])
    f.write('    print "finished setting uids"\n')
    f.close()
    print "migration step 1 finished"
    print "copy the generated script update_uids.py to your extensions folder"
    print "and execute it as an external method"
    return 'success'
