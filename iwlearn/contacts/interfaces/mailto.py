from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from iwlearn.contacts import contactsMessageFactory as _


class IMailTo(Interface):
    """Mail to a group of persons"""
