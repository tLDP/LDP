#!/usr/bin/python

"""
Lampadas Configuration module

This module provides configuration information from lampadas.conf.
"""

# Modules ##################################################################


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

	def __init__(self) :
		import ConfigParser

		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open('../conf/lampadas.conf'))
		if not self.config.has_section('DB') :
			raise ConfigFileReadErrorException("File 'lampadas.conf' is missing or does not contain a '[DB]' section")
			
		if not self.config.has_option('DB', 'dbtype') :
			raise ConfigFileReadErrorException("Can't read option 'dbtype' from lampadas.conf")
		self.DBType = self.config.get('DB', 'dbtype')
		
		if not self.config.has_option('DB', 'dbname') :
			raise ConfigFileReadErrorException("Can't read option 'dbname' from lampadas.conf")
		self.DBName = self.config.get('DB', 'dbname')
		

# main
if __name__ == '__main__' :
	print "This module cannot be run from the command line"
