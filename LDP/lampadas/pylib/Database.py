#!/usr/bin/python

"""
Lampadas Database Module

This module generates a Database object for accessing a back-end RDBMS
"""

# Modules ##################################################################

import pyPgSQL
import Config
import Log

# Database

class UnknownDBException(Exception):
	pass

class Database:
	"""
	The database contains all users and documents
	"""

	Config = Config.Config()
	Log = Log.Log()
	Connected = 0

	def __del__(self):
		if self.Connected:
			self.db.connection.close()
		
	def Connect(self, dbtype, dbname):
		"""
		Connect to the database specified in Config.
		"""

		if dbname == '':
			raise UnknownDBException('Database name not specified')
		elif dbtype == 'pgsql':
			self.db = PgSQLDatabase(dbname)
			self.Connected = 1
		else:
			raise UnknownDBException('Unknown database type %s' % dbtype)

#		self.Log(3, 'Thread safety ' + str(self.db.connection.threadsafety()))

	def Connection(self):
		return self.db.connection

	def Cursor(self):
		return self.db.connection.cursor()

	# FIXME : the python DB-API 2.0 states that you can transfer the burden
	# of quoting values to the cursor as in
	#
	# sql = "select * from document where doc_id = %(did)s"
	# param = {'did':'123'}
	# my_cursor.execute(sql,param)
	#
	# I like Python :-)
	#
	def Select(self, sql):
		if self.Config.LogSQL:
			self.Log(3, sql)
		self.cursor = self.db.connection.cursor()
		self.cursor.execute(sql)
		return self.cursor

	def Value(self, sql):
		if self.Config.LogSQL:
			self.Log(3, sql)
		self.cursor = self.db.connection.cursor()
		self.cursor.execute(sql)
		self.row = self.cursor.fetchone()
		if self.row == None:
			self.value = None
		else:
			self.value = self.row[0]
		return self.value

	def Exec(self, sql):
		if self.Config.LogSQL:
			self.Log(3, sql)
		self.cursor = self.db.connection.cursor()
		self.cursor.execute(sql)
		return self.cursor.rowcount

	def Commit(self):
		self.Log(3, 'Committing database')
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
	print "Running unit tests..."
	print "Unit tests run."

