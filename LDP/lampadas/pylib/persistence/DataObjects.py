# Copyright (c) 2002 Nicolas Chauvat <nicolas.chauvat@logilab.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
"""
DataObjects is a simple module that implements persistent objects over
a SQL back-end.

Nice reading:

* DB API - http://www.python.org/topics/database/DatabaseAPI-2.0.html

* Persistence SIG - http://www.python.org/sigs/persistence-sig/

* PyDO - http://skunkweb.sourceforge.net/PyDO/

TODO: explain how this module relates and compares to the above.

XXXFIXME: do more testing of this module!
"""

from sqlgen import sqlgen

class DataObject :

    primary_keys = []
    table = ''
    
    def __init__(self,transaction,**id) :
        """
        transaction is database transaction
        id is a dictionnary describing the identifier of the object
        """
        self._t = transaction
        # create id dictionnary
        self._id = {}
        try:
            for k in self.primary_keys :
                self._id[k] = id[k]
        except KeyError :
            raise Exception('Missing id key %s for user instance' % k)

        # create attributes dictionnary
        self._attr = {}
        sql = sqlgen.select(table,self._id)
        cnx = 
        # if user_with_this_id exist in DB :
        #    exec SELECT and update self._attr with result
        # else :
        #     self._attr.update(self.attributes)

    def update(self,attrs) :
        for k,v in attrs :
            self.__setitem__(k,v)

    def __getitem__(self,key) :
        try:
            return self._id[key]
        except KeyError :
            return self._attr[key]

    def __setitem__(self,key,value) :
        if key in self.primary_keys :
            raise Exception('Can not modify primary key %s of instance' % key)
        else :
            self._attr[key] = value

class Transaction :
    """
    A transaction manages persistent objects. It is used as a factory that
    instanciates objects. It also contains a connection to a back-end and
    handles commits and rollbacks.
    """

    def __init__(self,connection) :
        """
        connection is a connection to a database (see DB API).
        """
        self._connection = connection
        self._managed = []
        
    def new_object(self,klass,**id) :
        """
        Inserts a new row with given id in the table that stores objects
        of class klass and return an instance of klass.
        """
        # insert
        # make instance
        # append instance to list of managed
        raise NotImplementedError()

    def get_object(self,klass,**id) :
        """
        Checks that given id exists in the table that stores objects of class
        klass and return an instance of klass. Look up list of managed objects
        to avoid creating duplicates.
        """
        raise NotImplementedError()
    
    def get_objects(self,klass,**where) :
        """
        Return list of objects that fit the given where description.
        """
        raise NotImplementedError()

    def commit(self) :
        """
        Get from every object a SQL query to update its state, then execute them
        all and commit the changes.
        """
        raise NotImplementedError()

    def rollback(self) :
        """
        Rollback then refresh every managed object.
        """
        raise NotImplementedError()
    
class Database:
    """
    A database represents a back-end storage and is used as a factory that
    creates transactions.
    """

    def __init__(self,init_str) :
        """
        init_str is a connection init string (see DB API).
        """
        self._init_str = init_str
        
    def new_transaction(self) :
        """
        Factory method that produces transactions.
        """
        return Transaction( self.new_connection() )

    def new_connection(self) :
        """
        Template method to be overriden by derived classes implementing a
        specific DB type.
        """
        raise NotImplementedError()
    
class PgSQLDatabase(Database):

    def new_connection(self):
        from pyPgSQL import PgSQL
        return PgSQL.connect(database=self._init_str)

class MySQLDatabase(Database):

    def new_connection(self):
        from pyMySQL import MySQL
        return MySQL.connection(db_name=self._init_str)

class UnknownDBException(Exception):
    pass

def get_database(db_type, db_name):
    """
    Connect to the database specified in Config.

    See Factory Method design pattern.
    """
    if db_type=='pgsql':
        db = PgSQLDatabase(db_name)
    elif db_type=='mysql':
        db = MySQLDatabase(db_name)
    else:
        raise UnknownDBException('Unknown database type %s' % db_type)
    return db


