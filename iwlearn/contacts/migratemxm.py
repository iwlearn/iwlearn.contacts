# migrate mxmContacts to iwlearn.contacts
# copy this script into the Extension folder and execute it

def migrate_metadata(old, new, old_parent):
    new.update(creation_date=old.creation_date)    
    if old.effective_date:
        new.setEffectiveDate(old.effective_date)
    else:
        new.setEffectiveDate(old.creation_date)    
    new.setCreators(old.Creators())
    new.setModificationDate(old.creation_date)    

    uid = old.UID()
    old._uncatalogUID(old_parent)
    new._setUID(uid)


def migrate_group(old, old_parent, new_parent):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactDb', new_parent, obj_id, None)
    new = new_parent[obj_id]
    new.update(title=old.title, description=obj.description ) 
    new.SetBody(old.GetText) 
    migrate_metadata(old, new, old_parent)
    old_parent.manage_delObjects(ids=[obj_id])

def migrate_person(old, old_parent, new_parent):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactPerson', new_parent, obj_id, None)
    new = new_parent[obj_id]
    new.setSalutation(old.title )
    new.setFirstname(old.getFirstname )
    new.setLastname(old.getLastname )
    new.setJobtitle(old.getJobtitle )
    new.setAddress(old.getAddress )
    new.setCity(old.getCity )
    new.setZipcode(old.getPo )
    new.setMisc(old.getMisc )
    new.setCountry(old.getCountry )
    #reference
    new.setOrganization(old.getRawOrganization )
    new.setDepartment(old.getDepartment )
    new.setEmail(old.getEmail )
    new.setRemote_url(old.getWeb )
    new.setPhone(old.getOffice_phone )
    new.setMobile(old.getMobile_phone )
    new.setFax(old.getFax )
    new.setBody(old.getBody )
    #backreference
    new.setProjects(old.get )
    #backreference
    #new.setGroups(old.get )    

    migrate_metadata(old, new, old_parent)
    old_parent.manage_delObjects(ids=[obj_id])
    
def migrate_organization(old, old_parent, new_parent):
    if callable(old.id):
        obj_id = old.id()
    else:
        obj_id = old.id
    portal_types = old_parent.portal_types
    portal_types.constructContent('ContactOrganization', new_parent, obj_id, None)
    new = new_parent[obj_id]
    new.update(title=old.title)    
    
    
    
    
    migrate_metadata(old, new, old_parent)
    old_parent.manage_delObjects(ids=[obj_id])
    
migrate(self)
    for brain in self.portal_catalog(portal_type = 'mxmContacts'):
        obj=brain.getObject()
        parent = obj.getParentNode()
        
        if callable(obj.id):
            obj_id = obj.id()
        else:
            obj_id = obj.id
        parent.manage_renameObject(obj_id, obj_id + '_old')
        portal_types = parent.portal_types
        portal_types.constructContent('ContactDb', parent, obj_id, None)
        new = parent[obj_id]
        new.update(title=obj.title, description=obj.description ) 
        migrate_metadata(new, obj, parent)   
        for child in obj.objectValues():
            if child.portal_type == 'mxmContactsGroup':
                migrate_group(child, parent, new)
            elif child.portal_type == 'mxmContactsPerson':
                migrate_person(child, parent, new)
            elif child.portal_type == 'mxmContactsOrganization':
                migrate_organization(child, parent, new)
        parent.manage_delObjects(ids=[obj_id + '_old'])
