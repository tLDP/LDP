"""
DataLayer UnitTest
"""

import unittest
import DataLayer

DBNAME = 'db_test'

def get_connection(name) :
    from pyPgSQL import PgSQL
    return PgSQL.connect(database=name)

SQL_DROP = "DROP TABLE username"

SQL_CREATE = """CREATE TABLE username (
	username	CHAR(20)	NOT NULL,
	first_name	CHAR(20),
	surname		CHAR(20),
	maintainer_id	INT4,
	email		TEXT,
	admin		BOOLEAN,
	editor_id	INT4,

	PRIMARY KEY (username)
)
"""

SQL_INSERT = """
INSERT INTO username ( username, first_name, surname, email )
VALUES ( %(username)s, %(first_name)s, %s(surname), %(email)s )
"""

DATA_INSERT = {'username':'david',
               'first_name':'David', 'surname':'Merrill',
               'email':'david@lupercalia.net'}

DATA_TUPLE = ('david', 'David', 'Merrill', '12', 'david@lupercalia.net',
              '1', '13' )

# tests ########################################################################

class DatabaseTest(unittest.TestCase) :

    def setUp(self):
        self.con = get_connection(DBNAME)
        try:
            self.con.cursor().execute(SQL_CREATE)
        except Exception, e :
            print e
            self.con.cursor().execute('delete from %s'%TABLE)
        self.con.commit()
        self.con.cursor().execute(SQL_INSERT, DATA_INSERT)
        self.con.commit()
        self.db = DataLayer.PgSQLDatabase(DBNAME)

    def tearDown(self) :
        self.con.cursor().execute(DROP_TABLE)
        self.con.commit()
        self.con.close()
        
    def test_get_user(self):
        u = self.db.get_user('david')
        self.assert_(isinstance(u,User))
        self.assert_(u.name == 'david')
        # etc.

if __name__ == "__main__":
    unittest.main()
