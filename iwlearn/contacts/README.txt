Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The MailTo content type
===============================

In this section we are tesing the MailTo content type by performing
basic operations like adding, updadating and deleting MailTo content
items.

Adding a new MailTo content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'MailTo' and click the 'Add' button to get to the add form.

    >>> browser.getControl('MailTo').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'MailTo' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'MailTo Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'MailTo' content item to the portal.

Updating an existing MailTo content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New MailTo Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New MailTo Sample' in browser.contents
    True

Removing a/an MailTo content item
--------------------------------

If we go to the home page, we can see a tab with the 'New MailTo
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New MailTo Sample' in browser.contents
    True

Now we are going to delete the 'New MailTo Sample' object. First we
go to the contents tab and select the 'New MailTo Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New MailTo Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New MailTo
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New MailTo Sample' in browser.contents
    False

Adding a new MailTo content item as contributor
------------------------------------------------

Not only site managers are allowed to add MailTo content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'MailTo' and click the 'Add' button to get to the add form.

    >>> browser.getControl('MailTo').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'MailTo' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'MailTo Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new MailTo content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ContactPerson content type
===============================

In this section we are tesing the ContactPerson content type by performing
basic operations like adding, updadating and deleting ContactPerson content
items.

Adding a new ContactPerson content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ContactPerson' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactPerson').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactPerson' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactPerson Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ContactPerson' content item to the portal.

Updating an existing ContactPerson content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ContactPerson Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ContactPerson Sample' in browser.contents
    True

Removing a/an ContactPerson content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ContactPerson
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ContactPerson Sample' in browser.contents
    True

Now we are going to delete the 'New ContactPerson Sample' object. First we
go to the contents tab and select the 'New ContactPerson Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ContactPerson Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ContactPerson
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ContactPerson Sample' in browser.contents
    False

Adding a new ContactPerson content item as contributor
------------------------------------------------

Not only site managers are allowed to add ContactPerson content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'ContactPerson' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactPerson').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactPerson' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactPerson Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ContactPerson content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ContactOrganization content type
===============================

In this section we are tesing the ContactOrganization content type by performing
basic operations like adding, updadating and deleting ContactOrganization content
items.

Adding a new ContactOrganization content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ContactOrganization' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactOrganization').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactOrganization' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactOrganization Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ContactOrganization' content item to the portal.

Updating an existing ContactOrganization content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ContactOrganization Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ContactOrganization Sample' in browser.contents
    True

Removing a/an ContactOrganization content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ContactOrganization
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ContactOrganization Sample' in browser.contents
    True

Now we are going to delete the 'New ContactOrganization Sample' object. First we
go to the contents tab and select the 'New ContactOrganization Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ContactOrganization Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ContactOrganization
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ContactOrganization Sample' in browser.contents
    False

Adding a new ContactOrganization content item as contributor
------------------------------------------------

Not only site managers are allowed to add ContactOrganization content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'ContactOrganization' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactOrganization').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactOrganization' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactOrganization Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ContactOrganization content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ContactGroup content type
===============================

In this section we are tesing the ContactGroup content type by performing
basic operations like adding, updadating and deleting ContactGroup content
items.

Adding a new ContactGroup content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ContactGroup' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactGroup').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactGroup' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactGroup Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ContactGroup' content item to the portal.

Updating an existing ContactGroup content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ContactGroup Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ContactGroup Sample' in browser.contents
    True

Removing a/an ContactGroup content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ContactGroup
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ContactGroup Sample' in browser.contents
    True

Now we are going to delete the 'New ContactGroup Sample' object. First we
go to the contents tab and select the 'New ContactGroup Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ContactGroup Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ContactGroup
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ContactGroup Sample' in browser.contents
    False

Adding a new ContactGroup content item as contributor
------------------------------------------------

Not only site managers are allowed to add ContactGroup content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'ContactGroup' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactGroup').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactGroup' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactGroup Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ContactGroup content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ContactDb content type
===============================

In this section we are tesing the ContactDb content type by performing
basic operations like adding, updadating and deleting ContactDb content
items.

Adding a new ContactDb content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ContactDb' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactDb').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactDb' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactDb Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ContactDb' content item to the portal.

Updating an existing ContactDb content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ContactDb Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ContactDb Sample' in browser.contents
    True

Removing a/an ContactDb content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ContactDb
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ContactDb Sample' in browser.contents
    True

Now we are going to delete the 'New ContactDb Sample' object. First we
go to the contents tab and select the 'New ContactDb Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ContactDb Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ContactDb
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ContactDb Sample' in browser.contents
    False

Adding a new ContactDb content item as contributor
------------------------------------------------

Not only site managers are allowed to add ContactDb content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'ContactDb' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ContactDb').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ContactDb' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ContactDb Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ContactDb content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



