"""
This is the base class upon which all persistent objects are built.
"""

class Persistence(object):
    """
    Subclassed to "object" so we can use the new (in Python 2.2)
    __getattribute__ hook that lets us know when a data member has been
    altered.
    """
    
    IGNORE_CHANGE_ATTRIBUTES = ('changed', 'in_database')
    
    def __init__(self):
        self.in_database = 0
        self.changed = 0

    def __setattr__(self, attribute, value):
        super(Persistence, self).__setattr__(attribute, value)
        if attribute not in self.IGNORE_CHANGE_ATTRIBUTES:
            super(Persistence, self).__setattr__('changed', 1)

