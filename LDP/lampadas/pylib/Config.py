#!/usr/bin/python

"""
Lampadas Configuration module

This module provides configuration information from lampadas.conf.
"""

# Modules ##################################################################


# Globals

CONF_FILE = '/etc/lampadas.conf'


# BaseConfig ###############################################################

class ConfigFileReadErrorException(Exception) :
	pass
	
class Config:
	"""
	Basic configuration options (dbname, dbtype), used to know where we can find
	the database.
	"""

	DBType = ''
	DBName = ''
	LogFile = ''
	LogLevel = 0
	LogSQL = ''
	LogConsole = 0
	Interface = ''
	Port = 80
	Hostname = ''
	RootDir = ''
	FileDir = ''
	CVSRoot = ''
	CacheDir = ''

	def __init__(self) :
		import ConfigParser

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(CONF_FILE))

		self.DBType	= self.ReadVar('DB', 'dbtype')
		self.DBName	= self.ReadVar('DB', 'dbname')
		self.LogFile	= self.ReadVar('LOG', 'logfile')
		self.LogLevel	= int(self.ReadVar('LOG', 'loglevel'))
		self.LogSQL	= int(self.ReadVar('LOG', 'logsql'))
		self.LogConsole	= int(self.ReadVar('LOG', 'logcon'))
		self.Interface	= self.ReadVar('WEBSERVER', 'interface')
		self.Port	= int(self.ReadVar('WEBSERVER', 'port'))
		self.Hostname	= self.ReadVar('WEBSERVER', 'hostname')
		self.RootDir	= self.ReadVar('WEBSERVER', 'rootdir')
		self.FileDir	= self.ReadVar('WEBSERVER', 'filedir')
		self.CVSRoot	= self.ReadVar('CVS', 'cvsroot')
		self.cache_dir	= self.ReadVar('MIRROR', 'cachedir')

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
	assert Config.LogFile > ''
	print "LogFile=" + Config.LogFile
	print "LogSQL=" + str(Config.LogSQL)
	print "LogConsole=" + str(Config.LogConsole)
	print "Interface=" + Config.Interface
	print "Port=" + str(Config.Port)
	print "Hostname=" + Config.Hostname
	print "RootDir=" + Config.RootDir
	print "CVSRoot=" + Config.CVSRoot
	print "FileDir=" + Config.FileDir
	print "cache_dir=" + Config.cache_dir
	print "Unit tests complete."
