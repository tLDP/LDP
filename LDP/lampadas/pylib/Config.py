#!/usr/bin/python
# 
# This file is part of the Lampadas Documentation System.
# 
# Copyright (c) 2000, 2001, 2002 David Merrill <david@lupercalia.net>.
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
Lampadas Configuration module

This module provides configuration information from lampadas.conf.
"""

# Modules ##################################################################


# Globals

CONF_FILE = '/etc/lampadas/lampadas.conf'

# BaseConfig ###############################################################

class ConfigFileReadErrorException(Exception) :
    pass
    
class Config:
    """
    Basic configuration options (dbname, dbtype), used to know where we can find
    the database.
    """

    db_type = ''
    db_name = ''
    log_file = ''
    log_level = 0
    log_sql = ''
    log_console = 0
    interface = ''
    port = 80
    hostname = ''
    root_dir = ''
    file_dir = ''
    cvs_root = ''
    cache_dir = ''
    xslt_html = ''
    xslt_chunk = ''
    xslt_print = ''

    def __init__(self) :
        import ConfigParser

        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(CONF_FILE))

        self.db_type        = self.read_var('DB', 'dbtype')
        self.db_name        = self.read_var('DB', 'dbname')
        self.log_file       = self.read_var('LOG', 'logfile')
        self.log_level      = int(self.read_var('LOG', 'loglevel'))
        self.log_sql        = int(self.read_var('LOG', 'logsql'))
        self.log_console    = int(self.read_var('LOG', 'logcon'))
        self.interface      = self.read_var('WEBSERVER', 'interface')
        self.port           = int(self.read_var('WEBSERVER', 'port'))
        self.hostname       = self.read_var('WEBSERVER', 'hostname')
        self.root_dir       = self.read_var('WEBSERVER', 'rootdir')
        self.file_dir       = self.read_var('WEBSERVER', 'filedir')
        self.cvs_root       = self.read_var('CVS', 'cvsroot')
        self.cache_dir      = self.read_var('MIRROR', 'cachedir')
        self.xslt_html      = self.read_var('XSLT', 'xslt_html')
        self.xslt_chunk     = self.read_var('XSLT', 'xslt_chunk')
        self.xslt_print     = self.read_var('XSLT', 'xslt_print')

    def read_var(self, section, name):
        if not self.config.has_section(section) :
            raise ConfigFileReadErrorException("File '" + CONF_FILE + "' is missing or does not contain a '" + section + "' section")

        if not self.config.has_option(section, name):
            raise ConfigFileReadErrorException("Can't read option '" + name + "' from " + CONF_FILE)

        return self.config.get(section, name)

## exports ##

config = Config()
        
# main
if __name__ == '__main__' :
    print "Running unit tests..."
    assert config.db_type > ''
    print "db_type= " + config.db_type
    assert config.db_name > ''
    print "db_name= " + config.db_name
    assert config.log_file > ''
    print "log_file=" + config.log_file
    print "log_level=" + str(config.log_level)
    print "log_sql=" + str(config.log_sql)
    print "log_console=" + str(config.log_console)
    print "interface=" + config.interface
    print "port=" + str(config.port)
    print "hostname=" + config.hostname
    print "root_dir=" + config.root_dir
    print "cvs_root=" + config.cvs_root
    print "file_dir=" + config.file_dir
    print "cache_dir=" + config.cache_dir
    print "xslt_html=" + config.xslt_html
    print "xslt_chunk=" + config.xslt_chunk
    print "xslt_print=" + config.xslt_print
    print "Unit tests complete."
