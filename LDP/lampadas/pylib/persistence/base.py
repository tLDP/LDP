#!/usr/bin/python

"""
This is the base class upon which all persistent objects are built.
"""

IGNORE_CHANGE_ATTRIBUTES = ['changed', 'in_database']

class Persistence(object):
    """
    Subclassed to "object" so we can use the new (in Python 2.2)
    __getattribute__ hook that lets us know when a data member has been
    altered.
    """

    def __init__(self, dms):
        self.in_database = 0
        self.changed = 0
        self.dms = dms

    def __setattr__(self, attribute, value):
    	"""
        Traps setting of attributes.
        
        Calls the super() class to actually set the property.
        
        If the attribute is not listed in IGNORE_CHANGE_ATTRIBUTES,
        sets the "changed" property to 1.
        """
        super(Persistence, self).__setattr__(attribute, value)
        if attribute not in IGNORE_CHANGE_ATTRIBUTES:
            super(Persistence, self).__setattr__('changed', 1)

    def delete(self):
        """Deletes the object."""

        self.dms.delete(self)

    def save(self):
        """Saves the object."""

        self.dms.save(self)
