#!/usr/bin/python

"""
Lampadas Database Module

This module generates a Database object for accessing a back-end RDBMS
"""

# Modules ##################################################################

import pyPgSQL


# Database ###############################################################

class UnknownDBException(Exception):
	pass

class Database:
	"""
	The database contains all users and documents
	"""

	def Connect(self, dbtype, dbname):
		"""
		Connect to the database specified in Config.
		"""

		if dbname == '':
			raise UnknownDBException('Database name not specified')
		elif dbtype == 'pgsql':
			self.db = PgSQLDatabase(dbname)
		else:
			raise UnknownDBException('Unknown database type %s' % dbtype)

	def Connection(self):
		return self.db.connection

	def Cursor(self):
		return self.db.connection.cursor()

	def Value(self, sql):
		self.cursor = self.db.connection.cursor()
		self.cursor.execute(sql)
		self.value = self.cursor.fetchone()
		self.value = self.value[0]
		return self.value

	def Exec(self, sql):
		self.cursor = self.db.connection.cursor()
		self.cursor.execute(sql)
		return self.cursor.rowcount

	def Commit(self):
		self.db.connection.commit()


# Specific derived DB classes ##################################################

class PgSQLDatabase(Database):

	def __init__(self,dbname):
		from pyPgSQL import PgSQL
		self.connection = PgSQL.connect(database=dbname)

#	except ImportError:
#		# PostgresSQL back-end is not available
#		pass

class MySQLDatabase(Database):

	def __init__(self,dbname):
		from pyMySQL import MySQL
		self.cnx = MySQL.connection(dbname=dbname)

#	except ImportError:
#		# MySQL back-end is not available
#		pass


# main
if __name__ == '__main__':
	print "This should start the unit tests"

