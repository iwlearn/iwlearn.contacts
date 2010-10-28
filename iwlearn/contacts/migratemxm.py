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

def migrate_metadata(old, new, old_parent, new_parent):
    new.update(creation_date=old.creation_date)
    if old.effective_date:
        new.setEffectiveDate(old.effective_date)
    else:
        new.setEffectiveDate(old.creation_date)
    new.setCreators(old.Creators())
    new.setModificationDate(old.creation_date)
    new.setSubject(old.Subject())
    uid = old.UID()
    old._uncatalogUID(new_parent)
    new._setUID(uid)


def migrate_group(old, old_parent, new_parent,f):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactGroup', new_parent, obj_id, None)
    new = new_parent[obj_id]
    new.update(title=old.title, description=obj.description )
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
    new.setSalutation(old.title )
    new.setFirstname(old.getFirstname() )
    new.setLastname(old.getLastname())
    new.setJobtitle(old.getJobtitle())
    new.setAddress(old.getAddress())
    new.setCity(old.getCity())
    new.setZipcode(old.getPo())
    new.setMisc(old.getMisc())
    new.setCountry([old.getCountry(),])
    #reference
    new.setOrganization(old.getRawOrganization())
    new.setDepartment(old.getDepartment())
    new.setEmail(old.getEmail())
    new.setRemote_url(old.getWeb())
    new.setPhone(old.getOffice_phone())
    new.setMobile(old.getMobile_phone())
    new.setFax(old.getFax())
    new.setBody(old.getBody())
    #backreference
    new.setProjects(old.getBRefs('Rel1'))
    #backreference
    new.setLocation(old.getRawCity() + ', ' + old.getRawCountry())
    new.setRelatedItems([])
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
    new.update(title=old.title)
    new.setAddress(old.getRawAddress())
    new.setCity(old.getRawCity())
    new.setMisc(old.getRawMisc())
    new.setZipcode(old.getRawPo())
    new.setCountry([old.getRawCountry(),])
    new.setEmail(old.getRawEmail())
    new.setRemote_url(old.getRawWeb())
    new.setPhone(old.getRawPhone())
    new.setFax(old.getRawFax())
    new.setBody(old.getRawBody())
    new.setLocation(old.getRawCity() + ', ' + old.getRawCountry())
    #backreference
    new.setContactpersons(old.getBRefs())
    new.setRelatedItems([])
    f.write('    #organization \n')
    f.write('    obj=uid_tool.lookupObject("' + old.UID() + '")\n')
    f.write('    obj.setContactpersons([')
    for person in new.getRawContactpersons():
        f.write(' "' + person + '",')
    f.write('])\n')
    print old.UID()
    migrate_metadata(old, new, old_parent, new_parent)
    old_parent.manage_delObjects(ids=[obj_id])

def migrate(self):
    print 'starting migration'
    f = open('update_uids.py', 'w')
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
        migrate_metadata(obj, new, parent, parent)
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
