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
    user_id     INT4        NOT NULL,
	username    CHAR(20)    NOT NULL UNIQUE,
	session_id  CHAR(20),
	first_name  CHAR(20),
	middle_name CHAR(20),
	surname     CHAR(20),
	email       TEXT,
	admin       BOOLEAN,
	password    CHAR(12),
	notes       TEXT,

	PRIMARY KEY (user_id)
)
"""

SQL_INSERT = """
INSERT INTO username (user_id, username, first_name, surname, email, admin )
VALUES ('1', '%(username)s', '%(first_name)s', '%(surname)s', '%(email)s', TRUE )
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
			self.con.cursor().execute('delete from username')
		self.con.commit()
		self.con.cursor().execute(SQL_INSERT % DATA_INSERT)
		self.con.commit()
		self.db = DataLayer.get_database('pgsql', DBNAME)

	def tearDown(self) :
	#	self.con.cursor().execute(SQL_DROP)
	#	self.con.commit()
	#	self.con.close()
		pass

	def test_get_user(self):
		u = self.db.get_user_by_name('david')
		self.assert_(isinstance(u,DataLayer.User))
		self.assert_(u.username == 'david')
		self.assert_(u.firstname == 'David')
		self.assert_(u.surname == '')
		self.assert_(u.name == 'Merrill')
		self.assert_(u.email == 'david@lupercalia.net')
		self.assert_(u.is_admin == 1)
		

if __name__ == "__main__":
	unittest.main()
