#!/usr/bin/python

"""
This is the base class upon which all persistent objects are built.
"""

class Persistence(object):
    """
    Subclassed to "object" so we can use the new (in Python 2.2)
    __getattribute__ hook that lets us know when a data member has been
    altered.
    """

    def __init__(self, dms, dm):
        # Instantiate CHANGE_ATTRIBUTES first, because it will be examined
        # when other attributes are set.
        super(Persistence, self).__setattr__('CHANGE_ATTRIBUTES', [])
        self.in_database = 0
        self.changed = 0
        self.dms = dms
        self.dm = dm

        # Build a list of attributes whose change will trigger my
        # changed property to become YES. By default, this includes
        # all attributes defined as database attributes in my
        # data manager's table's field list, except for timestamps.
        for key in self.dm.table.fields.keys():
            field = self.dm.table.fields[key]
            if field.attribute not in ['created', 'updated']:
                self.CHANGE_ATTRIBUTES.append(field.attribute)

    def __setattr__(self, attribute, value):
    	"""
        Traps setting of attributes.
        
        Calls the super() class to actually set the property,
        to avoid deadly recursion.
        
        If the attribute is listed in CHANGE_ATTRIBUTES,
        and the new value differs from theold value,
        sets the "changed" property to 1. This check is only
        performed if there *is* an earlier value.
        """
        if attribute in self.CHANGE_ATTRIBUTES:
#            print attribute + ' is in CHANGE_ATTRIBUTES'
            if attribute in self.__dict__.keys():
#                print attribute + ' is in the dictionary'
                if value <> getattr(self, attribute):
#                    print attribute + ' has changed.'
                    super(Persistence, self).__setattr__('changed', 1)
        super(Persistence, self).__setattr__(attribute, value)

    def delete(self):
        """Deletes the object."""
        self.dm.delete(self)

    def save(self):
        """Saves the object."""
        self.dm.save(self)
