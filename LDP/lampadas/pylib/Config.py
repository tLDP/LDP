#!/usr/bin/python

"""
Lampadas Configuration module

This module provides configuration information from lampadas.conf.
"""

# Modules ##################################################################


# Globals

CONF_FILE = '../conf/lampadas.conf'


# BaseConfig ###############################################################

class ConfigFileReadErrorException(Exception) :
	pass
	
class Config:
	"""
	Basic configuration options (dbname, dbtype), used to know where we can find
	the database.
	"""

	DBType = ""
	DBName = ""
	Logfile = ""

	def __init__(self) :
		import ConfigParser

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(CONF_FILE))

		self.DBType	= self.ReadVar('DB', 'dbtype')
		self.DBName	= self.ReadVar('DB', 'dbname')
		self.Logfile	= self.ReadVar('LOG', 'logfile')


	def ReadVar(self, section, name):
		if not self.config.has_section(section) :
			raise ConfigFileReadErrorException("File '" + CONF_FILE + "' is missing or does not contain a '" + section + "' section")

		if not self.config.has_option(section, name):
			raise ConfigFileReadErrorException("Can't read option '" + name + "' from " + CONF_FILE)

		return self.config.get(section, name)
			
		
# main
if __name__ == '__main__' :
	print "Running unit tests..."
	Config = Config()
	assert Config.DBType > ''
	print "DBType= " + Config.DBType
	assert Config.DBName > ''
	print "DBName= " + Config.DBName
	assert Config.Logfile > ''
	print "Logfile=" + Config.Logfile
	print "Unit tests complete."
