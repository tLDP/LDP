#!/usr/bin/python

"""
Lampadas system

This modules defines Data Objects (Users, Documents, Notes, Topics, etc.)
and a Database object that manages SQL queries to the back-end and acts as
a data object factory.
"""

### THIS CODE IS NOT FUNCTIONAL YET ###

__version__ = '0.1.200205131'


# Modules ##################################################################

from types import StringType
#import mx.DateTime as DateTime


# BaseConfig ###############################################################

class ConfigFileReadErrorException(Exception) :
	pass
	
class ConfigFile :
	"""
	Basic configuration options (dbname, dbtype), used to know where we can find
	the database.
	"""

	def __init__(self) :
		import ConfigParser

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open('lampadas.conf'))
		self.parse()

	def parse(self) :
		if not self.config.has_section('DB') :
			raise ConfigFileReadErrorException("File 'lampadas.conf' is missing or does not contain a '[DB]' section")
			
		if not self.config.has_option('DB', 'dbtype') :
			raise ConfigFileReadErrorException("Can't read option 'dbtype' from lampadas.conf")
		self.dbtype = self.config.get('DB', 'dbtype')
		
		if not self.config.has_option('DB', 'dbname') :
			raise ConfigFileReadErrorException("Can't read option 'dbname' from lampadas.conf")
		self.dbname = self.config.get('DB', 'dbname')
		

# User ####################################################################

class UserNotFoundException(Exception) :
	pass
	
class User :
	"""
	A user is known by the system and can login to manipulate documents
	and act on the database according to his rights.
	"""

	def __init__(self) :
		self.username = None
		self.user_id = None
		self.firstname = None
		self.middlename = None
		self.surname = None
		self.name = None
		self.email = None
		self.is_admin = None


# Document ################################################################

class DocumentNotFoundException(Exception) :
	pass

class Document :
	"""
	A document is stored in the system to be collaboratively written,
	edited, proof-read and maintained. The system will also publish it.
	"""

	def __init__(self) :
		self.doc_id = None
		self.title = None
		self.filename = None
		self.type = Type()
		self.audience = Audience()
		self.format = Format()
		self.dtd = DTD()
		self.version = None
		self.last_update = None					## DateTime.strptime('2002-12-01', '%Y-%m-%d')
		self.url = None
		self.isbn = None
		self.pub_status = PubStatus()
		self.author_status = None				## XXX FIXME
		self.review_status = ReviewStatus()
		self.tickle_date = None
		self.pub_date = None
		self.ref_url = None
		self.tech_review_status = ReviewStatus()
		self.maintained = None
		self.license = License()
		self.abstract = None
		self.wiki = Wiki()
		self.rating = None


# Audience ################################################################

class Audience :
	"""
	The audience of a document (Novice, Beginners, etc.)
	"""

	def __init__(self) :
		self.name = None
		self.level = None
		self.description = None

# DTD #####################################################################

class DTD :
	"""
	A Document Type Definition
	"""

	def __init__(self) :
		self.name = None
		self.version = None

# Format ##################################################################

class Format :
	"""
	A document format
	"""

	def __init__(self) :
		self.name = None
		self.long_name = None

# License #################################################################

class License :
	"""
	A license for a document
	"""

	def __init__(self) :
		self.name = None
		self.free = None

# Note ####################################################################

class Note :
	"""
	A note is written by a user and attached to a document
	"""

	def __init__(self) :
		self.date_entered = None
		self.text = None
		self.user = None

# PubStatus ###############################################################

class PubStatus :
	"""
	The publication status of a document (Wishlist, pending, active, etc.)
	"""

	def __init__(self) :
		self.code = None
		self.name = None
		self.description = None

# ReviewStatus ###########################################################

class ReviewStatus :
	"""
	The review status of a document (in progress, reviewed, etc.)
	"""

	def __init__(self) :
		self.code = None
		self.name = None

# Revision ################################################################

class Revision :
	"""
	A revision describes a document version
	"""

	def __init__(self) :
		self.rev_id = None
		self.version = None
		self.pub_date = None
		self.initials = None
		self.notes = None

# Role ####################################################################

class Role :
	"""
	A role that can be taken by a user
	"""

	def __init__(self) :
		self.name = None

# Topic ####################################################################

class Topic :
	"""
	A topic tells what a document is about
	"""

	def __init__(self) :
		self.num = None
		self.name = None
		self.description = None
		self.subtopic_num = None		# XXX FIXME
		self.subtopic_name = None		# XXX FIXME

# Type ####################################################################

class Type :
	"""
	The class of a document (HOWTO, Guide, FAQ, etc.)
	"""

	def __init__(self) :
		self.name = None
		self.long_name = None

# Wiki #####################################################################

class Wiki :
	"""
	A wiki attached to a document
	"""

	def __init__(self) :
		self.revision = None
		self.date_entered = None
		self.wiki = None
		self.notes = None
		self.user = None


# main
if __name__ == '__main__' :
	print "This should start the unit tests"


# Database ###############################################################

class UnknownDBException(Exception) :
	pass

def get_database(dbtype = '', dbname = '') :
	"""
	To let people use different DBs, use specific class derived from Database
	"""
	# Use config file
	dbconfig = ConfigFile()

	# Overwrite options if arguments specified
	if dbtype != '' :
		dbconfig.dbtype = dbtype
	if dbname != '' :
		dbconfig.dbname = dbname

	if dbconfig.dbtype == 'pgsql' :
		return PgSQLDatabase(dbconfig.dbname)
	elif dbconfig.dbtype == 'mysql' :
		return MySQLDatabase(dbconfig.dbname)
	else :
		raise UnknownDBException('Unknown database type %s' % dbconfig.dbtype)

class Database :
	"""
	The database contains all users and documents
	"""
	
	def __init__(self, dbname) :
		"""
		Init database connection
		"""
		pass

	def get_config(self, name) :
		"""
		Return value of config parameter
		"""
		cur = self.connection.cursor()
		cur.execute("SELECT value FROM config WHERE name = %s", name)
		tmp = cur.fetchone()
		return tmp[0]


	# users ###
	
	def mk_user(self, row) :
		"""
		User factory (takes a single row query result as argument)
		QUERY = SELECT user_id, username, first_name, middle_name, surname, email, admin, notes from username
		"""
		if row == None :
			raise UserNotFoundException
		
		u = User()
		
		u.user_id = row[0]
		u.username = row[1].rstrip()
		
		if isinstance(row[2], StringType) :
			u.firstname = row[2].rstrip()
			u.name = u.firstname
			
		if isinstance(row[3], StringType) :
			u.middlename = row[3].rstrip()
		if u.middlename :
			if u.name :
				u.name = '%s %s' % (u.name, u.middlename)
			else :
				u.name = u.middlename
		
		if isinstance(row[4], StringType) :
			u.surname = row[4].rstrip()
		if u.surname :
			if u.name :
				u.name = '%s %s' % (u.name, u.surname)
			else :
				u.name = u.surname

		if isinstance(row[5], StringType) :
			u.email = row[5].rstrip()

		u.is_admin = row[6]
		u.notes = row[7]
		
		return u

	def get_user_by_name(self, username) :
		"""
		Return user by username entry
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT user_id, username, first_name, middle_name, surname, email, admin, notes from username WHERE username = %s', username)
		return self.mk_user(cur.fetchone())
	
	def get_user_by_id(self, user_id) :
		"""
		Return user by user_id entry
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT user_id, username, first_name, middle_name, surname, email, admin, notes from username WHERE user_id = %s', user_id)
		return self.mk_user(cur.fetchone())

	def get_users(self) :
		"""
		Return the list of all users. User list Factory.
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT user_id, username, first_name, middle_name, surname, email, admin, notes from username')
		return [self.mk_user(row) for row in cur.fetchall()]
	
	def get_user_by_sessionid(self, session_id) :
		"""
		Return a user that has corresponding session_id
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT user_id, username, first_name, middle_name, surname, email, admin, notes FROM username WHERE session_id = %s', session_id)
		return self.mk_user(cur.fetchone())

	def is_maintainer(self, user) :
		"""
		Return true if user is a maintainer or an admin
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT COUNT(*) FROM document_user WHERE active = TRUE AND user_id = %s', user.user_id)
		return user.is_admin or cur.fetchone()[0]
	
	
	# documents ###
	
	def mk_document(self, row) :
		"""
		Document factory (takes a single row query result as argument)
		QUERY = SELECT d.doc_id, d.title, df.filename, c.class, c.class_name, a.audience, a.audience_level, a.audience_description, f.format, f.format_name, d.dtd, d.dtd_version, d.version, d.last_update, d.url, d.isbn, p.pub_status, p.pub_status_name, p.pub_status_desc, r.review_status, r.review_status_name, d.tickle_date, d.pub_date, d.ref_url, r2.review_status, r2.review_status_name, d.maintained, l.license, l.free, d.abstract, d.rating FROM document d, document_file df, class c, audience a, document_audience da, format f, pub_status p, review_status r, review_status r2, license l WHERE d.doc_id = df.doc_id AND d.class = c.class AND d.doc_id = da.doc_id AND da.audience = a.audience AND d.format = f.format AND d.pub_status = p.pub_status AND d.review_status = r.review_status AND d.tech_review_status = r2.review_status AND d.license = l.license
		"""
		if row == None :
			raise DocumentNotFoundException
		
		d = Document()
		
		d.doc_id = row[0]
		
		if isinstance(row[1], StringType) :
			d.title = row[1].rstrip()
		
		if isinstance(row[2], StringType) :
			d.filename = row[2].rstrip()
		
		if isinstance(row[3], StringType) :
			d.type.name = row[3].rstrip()
		
		if isinstance(row[4], StringType) :
			d.type.long_name = row[4].rstrip()
		
		if isinstance(row[5], StringType) :
			d.audience.name = row[5].rstrip()
		
		d.audience.level = row[6]
		
		if isinstance(row[7], StringType) :
			d.audience.description = row[7].rstrip()
		
		if isinstance(row[8], StringType) :
			d.format.name = row[8].rstrip()
		
		if isinstance(row[9], StringType) :
			d.format.long_name = row[9].rstrip()
		
		if isinstance(row[10], StringType) :
			d.dtd.name = row[10].rstrip()
		
		if isinstance(row[11], StringType) :
			d.dtd.version = row[11].rstrip()
		
		if isinstance(row[12], StringType) :
			d.version = row[12].rstrip()
		
		d.last_update = row[13]
		
		if isinstance(row[14], StringType) :
			d.url = row[14].rstrip()
		
		if isinstance(row[15], StringType) :
			d.isbn = row[15].rstrip()
		
		if isinstance(row[16], StringType) :
			d.pub_status.code = row[16].rstrip()
		
		if isinstance(row[17], StringType) :
			d.pub_status.name = row[17].rstrip()
		
		if isinstance(row[18], StringType) :
			d.pub_status.description = row[18].rstrip()
		
		if isinstance(row[19], StringType) :
			d.review_status.code = row[19].rstrip()
		
		if isinstance(row[20], StringType) :
			d.review_status.name = row[20].rstrip()
		
		d.tickle_date = row[21]
		
		d.pub_date = row[22]
		
		if isinstance(row[23], StringType) :
			d.ref_url = row[23].rstrip()
		
		if isinstance(row[24], StringType) :
			d.tech_review_status.code = row[24].rstrip()
		
		if isinstance(row[25], StringType) :
			d.tech_review_status.name = row[25].rstrip()
		
		d.maintained = row[26]
		
		if isinstance(row[27], StringType) :
			d.license.name = row[27].rstrip()
		
		d.license.free = row[28]
		
		if isinstance(row[29], StringType) :
			d.abstract = row[29].rstrip()
		
		d.rating = row[30]

		return d
	
	def get_document(self, doc_id) :
		"""
		Return document by doc_id entry
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT d.doc_id, d.title, df.filename, c.class, c.class_name, a.audience, a.audience_level, a.audience_description, f.format, f.format_name, d.dtd, d.dtd_version, d.version, d.last_update, d.url, d.isbn, p.pub_status, p.pub_status_name, p.pub_status_desc, r.review_status, r.review_status_name, d.tickle_date, d.pub_date, d.ref_url, r2.review_status, r2.review_status_name, d.maintained, l.license, l.free, d.abstract, d.rating FROM document d, document_file df, class c, audience a, document_audience da, format f, pub_status p, review_status r, review_status r2, license l WHERE d.doc_id = df.doc_id AND d.class = c.class AND d.doc_id = da.doc_id AND da.audience = a.audience AND d.format = f.format AND d.pub_status = p.pub_status AND d.review_status = r.review_status AND d.tech_review_status = r2.review_status AND d.license = l.license AND d.doc_id = %s', doc_id)
		return self.mk_document(cur.fetchone())

	def get_documents_by_user(self, user_id) :
		"""
		Return list of documents for a given user
		"""
		cur = self.connection.cursor()
		cur.execute('SELECT d.doc_id, d.title, df.filename, c.class, c.class_name, a.audience, a.audience_level, a.audience_description, f.format, f.format_name, d.dtd, d.dtd_version, d.version, d.last_update, d.url, d.isbn, p.pub_status, p.pub_status_name, p.pub_status_desc, r.review_status, r.review_status_name, d.tickle_date, d.pub_date, d.ref_url, r2.review_status, r2.review_status_name, d.maintained, l.license, l.free, d.abstract, d.rating FROM document d, document_file df, class c, audience a, document_audience da, format f, pub_status p, review_status r, review_status r2, license l, document_user du WHERE d.doc_id = df.doc_id AND d.class = c.class AND d.doc_id = da.doc_id AND da.audience = a.audience AND d.format = f.format AND d.pub_status = p.pub_status AND d.review_status = r.review_status AND d.tech_review_status = r2.review_status AND d.license = l.license AND du.user_id = %s AND du.doc_id = d.doc_id', user_id)
		return [self.mk_document(row) for row in cur.fetchall()]

	def add_document(self, document) :
		"""
		Add a new document
		"""
		# turn Document instance into SQL INSERT
		pass

	def update_document(self, document) :
		"""
		Update document description
		"""
		# turn Document instance into SQL UPDATE
		pass

	def get_document_count(self, type=None, tuple=[]) :
		"""
		return number of documents
		"""
		if type == 'byClass' :
			# SELECT COUNT(*) FROM document WHERE class IN (" . $class . ")")	# SELECT COUNT(*) FROM document
			pass
		elif type == 'byPubStatus' :
			# SELECT COUNT(*) FROM document WHERE pub_status in (" . $pub_status . ")")
			pass
		else :
			# SELECT COUNT(*) FROM document
			pass

	def get_users_by_document(self, doc_id) :
		"""
		Return list of users with their roles
		"""
		# "SELECT document_user.user_id, role, document_user.email, active, username, first_name, middle_name, surname FROM document_user, username WHERE document_user.user_id = username.user_id AND doc_id=$doc_id"
		pass

	
	# topics ###
	
	def get_topics_by_document(self, doc_id) :
		"""
		Return a list of topics
		"""
		# SELECT dt.topic_num, dt.subtopic_num, t.topic_name, s.subtopic_name FROM topic t, subtopic s, document_topic dt WHERE t.topic_num = s.topic_num AND dt.topic_num = s.topic_num AND dt.subtopic_num = s.subtopic_num AND dt.doc_id = $doc_id
		pass

	def get_topic(self, topic_num) :
		"""
		Return the topic
		"""
		# SELECT topic_num, topic_name, topic_description FROM topic WHERE topic_num=$topic_num
		pass

	def get_topics(self, father_id=0) :
		"""
		Return list of topics
		"""
		# SELECT topic_num, topic_name, topic_description FROM topic
		pass

	def add_topic(self, topic) :
		"""
		Add a new topic
		"""
		# UPDATE topic SET topic_name=" . wsq($topic_name) . ", topic_description=" . wsq($topic_description) . " WHERE topic_num=$topic_num
		pass

	def update_topic(self, topic) :
		"""
		Update a given topic
		"""
		# UPDATE topic SET topic_name=" . wsq($topic_name) . ", topic_description=" . wsq($topic_description) . " WHERE topic_num=$topic_num
		pass

	
	# notes ###
	
	def get_notes_by_document(self, doc_id) :
		"""
		Return a list of notes
		"""
		# "SELECT n.date_entered, n.notes, u.username FROM notes n, username u WHERE n.creator_id = u.user_id AND n.doc_id = $doc_id ORDER BY n.date_entered"
		pass

	def get_notes_by_user(self, user_id) :
		"""
		Return list of notes. notes list factory.
		"""
		# SELECT un.date_entered, un.notes, u.username FROM username u, username_notes un WHERE u.user_id = un.user_id AND u.user_id = $user_id
		pass

	def add_note(self, note) :
		"""
		Add a new note
		"""
		# INSERT INTO username (user_id, notes, creator_id) VALUES ($user_id, " . wsq($notes) . ", " . CurrentUserID() . ")
		pass


	# revisions ###
	
	def get_revisions_by_document(self, doc_id) :
		"""
		Return a list of revisions
		"""
		#
		pass

	def add_revision(self, revision) :
		"""
		Add a new revision
		"""
		# Turn revision into an INSERT
	# INSERT INTO document_rev(doc_id, rev_id, version, pub_date, initials, notes) VALUES ($doc_id, $rev_id, $version, " . &wsq($pub_date) . ", " . &wsq($initials) . ", " . &wsq($notes) . ")
		pass

	def update_revision(self, revision) :
		"""
		Update an existing revision
		"""
		# doc_id, rev_id, version, pub_date, initials, notes) :
	# UPDATE document_rev SET version=" . wsq($version) . ", pub_date=" . wsq($pub_date) . ", initials=" . wsq($initials) . ", notes=" . wsq($notes) . " WHERE doc_id=$doc_id AND rev_id=$rev_id"
		pass

	def remove_revision(self, revision_id) :
		"""
		Remove a document revision
		"""
	# DELETE FROM document_rev WHERE doc_id=$doc_id AND rev_id=$rev_id
		pass
	
  
	# roles ###
	
	def get_roles(self) :
		"""
		Return list of roles
		"""
		# SELECT role FROM role
		pass

	# licenses ###
	
	def get_licenses(self) :
		"""
		Return list of licenses
		"""
		# SELECT license FROM license
		pass

	# formats ###
	
	def get_formats(self) :
		"""
		Return list of formats
		"""
		# SELECT format, format_name FROM format"
		pass

	# dtds ###
	
	def get_dtds(self) :
		"""
		Return list of dtds
		"""
		# SELECT dtd FROM dtd"
		pass


try:
	import pyPgSQL
	
	class PgSQLDatabase(Database) :

		def __init__(self,dbname) :
			from pyPgSQL import PgSQL
			self.connection = PgSQL.connect(database=dbname)
except ImportError:
	# PostgresSQL back-end is not available
	pass

try:
	import pyMySQL

	class MySQLDatabase(Database) :

		def __init__(self,dbname) :
			from pyMySQL import MySQL
			self.cnx = MySQL.connection(dbname=dbname)

except ImportError:
	# MySQL back-end is not available
	pass
