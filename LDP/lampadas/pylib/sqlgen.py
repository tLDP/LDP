"""
SQLGen is a module that helps generating SQL strings to use with Python's DB-API.

Released under the GNU General Public License.
"""

# SQLGenerator ##############################################################

class SQLGenerator :
    """
    Helper class to generate SQL strings to use with python's DB-API
    """

    def where(self,keys) :
        """
        keys : list of keys
        
        >>> s = SQLGenerator()
        >>> s.where(['nom'])
        'nom = %(nom)s'
        >>> s.where(['nom','prenom'])
        'nom = %(nom)s AND prenom = %(prenom)s'
        """
        return ' AND '.join(["%s = %%(%s)s" % (k,k) for k in keys])

    def set(self,keys) :
        """
        keys : list of keys
        
        >>> s = SQLGenerator()
        >>> s.set(['nom'])
        'nom = %(nom)s'
        >>> s.set(['nom','prenom'])
        'nom = %(nom)s, prenom = %(prenom)s'
        """
        return ', '.join(["%s = %%(%s)s" % (k,k) for k in keys])

    def insert(self,table,dict) :
        """
        table : name of the table
        dict :  dictionnary that will be used as in cursor.execute(sql,dict)
        
        >>> s = SQLGenerator()
        >>> s.insert('test',{'nom':'dupont'})
        'INSERT INTO test ( nom ) VALUES ( %(nom)s )'
        >>> s.insert('test',{'nom':'dupont','prenom':'jean'})
        'INSERT INTO test ( nom, prenom ) VALUES ( %(nom)s, %(prenom)s )'
        """
        keys = ', '.join(dict.keys())
        values = ', '.join(["%%(%s)s" % k for k in dict.keys()])
        sql='INSERT INTO %s ( %s ) VALUES ( %s )' % (table, keys, values)
        return sql

    def select(self,table,dict) :
        """
        table : name of the table
        dict :  dictionnary that will be used as in cursor.execute(sql,dict)

        >>> s = SQLGenerator()
        >>> s.select('test',{})
        'SELECT * FROM test'
        >>> s.select('test',{'nom':'dupont'})
        'SELECT * FROM test WHERE nom = %(nom)s'
        >>> s.select('test',{'nom':'dupont','prenom':'jean'})
        'SELECT * FROM test WHERE nom = %(nom)s AND prenom = %(prenom)s'
        """
        sql='SELECT * FROM %s' % table
        where = self.where(dict.keys())
        if where : sql = sql + ' WHERE %s' % where
        return sql

    def delete(self,table,dict) :
        """
        table : name of the table
        dict :  dictionnary that will be used as in cursor.execute(sql,dict)

        >>> s = SQLGenerator()
        >>> s.delete('test',{'nom':'dupont'})
        'DELETE FROM test WHERE nom = %(nom)s'
        >>> s.delete('test',{'nom':'dupont','prenom':'jean'})
        'DELETE FROM test WHERE nom = %(nom)s AND prenom = %(prenom)s'
        """
        where = self.where(dict.keys())
        sql='DELETE FROM %s WHERE %s' % (table,where)
        return sql

    def update(self,table,dict,unique) :
        """
        table : name of the table
        dict :  dictionnary that will be used as in cursor.execute(sql,dict)

        >>> s = SQLGenerator()
        >>> s.update('test',{'id':'001','nom':'dupont'},['id'])
        'UPDATE test SET nom = %(nom)s WHERE id = %(id)s'
        >>> s.update('test',{'id':'001','nom':'dupont','prenom':'jean'},['id'])
        'UPDATE test SET prenom = %(prenom)s, nom = %(nom)s WHERE id = %(id)s'
        """
        where = self.where(unique)
        set = self.set([k for k in dict.keys() if k not in unique])
        sql='UPDATE %s SET %s WHERE %s' % (table,set,where)
        return sql

sqlgen = SQLGenerator()

# Helper functions #############################################################

def name_fields(cursor,records) :
    """
    Take a cursor and a list of records fetched with that cursor, then return a
    list of dictionnaries (one for each record) whose keys are column names and
    values are records' values.

    cursor : cursor used to execute the query
    records : list returned by fetchXXX()
    """
    result = []
    for record in records :
        record_dict = {}
        for i in range(len(record)) :
            record_dict[cursor.description[i][0]] = record[i]
        result.append(record_dict)
    return result
    
        
def _test():
    import doctest, sqlgen
    return doctest.testmod(sqlgen)

if __name__ == "__main__":
    _test()
