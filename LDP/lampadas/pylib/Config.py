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


# BaseConfig ###############################################################

class ConfigFileReadErrorException(Exception) :
    pass
    
class Config:
    """
    Basic configuration options (db_name, db_type), used to know where we
    can find the database.
    """

    config_file = ''
    project_name = ''
    project_short = ''
    db_type = ''
    db_name = ''
    db_host = ''
    log_file = ''
    log_level = 0
    log_sql = ''
    log_console = 0
    interface = ''
    port = ''
    hostname = ''
    root_dir = ''
    file_dir = ''
    cvs_root = ''
    cache_dir = ''
    xslt_html = ''
    xslt_chunk = ''
    xslt_print = ''
    smtp_server = ''
    admin_email = ''
    db2omf = ''
    wt2db = ''

    def __init__(self) :
        import ConfigParser
        import os

    	msg = ''
        self.config = ConfigParser.ConfigParser()
        self.config_file = os.getenv('LAMPADAS_ETC')
        if self.config_file==None:
            self.config_file = '/etc/lampadas'
	    msg = 'Environment variable LAMPADAS_ETC is undefined.\n'
        self.config_file = self.config_file + '/lampadas.conf'
        if not os.access(self.config_file, os.F_OK):
            raise msg + self.config_file + " not found."

        self.config.readfp(open(self.config_file))

        self.project_name   = self.read_var('MAIN', 'project_name')
        self.project_short  = self.read_var('MAIN', 'project_short')
        self.db_type        = self.read_var('DB', 'dbtype')
        self.db_name        = self.read_var('DB', 'dbname')
        self.db_host        = self.read_var('DB', 'dbhost')
        self.log_file       = self.read_var('LOG', 'logfile')
        self.log_level      = int(self.read_var('LOG', 'loglevel'))
        self.log_sql        = int(self.read_var('LOG', 'logsql'))
        self.log_console    = int(self.read_var('LOG', 'logcon'))
        self.interface      = self.read_var('WEBSERVER', 'interface')
        self.port           = self.read_var('WEBSERVER', 'port')
        self.hostname       = self.read_var('WEBSERVER', 'hostname')
        self.root_dir       = self.read_var('WEBSERVER', 'rootdir')
        self.file_dir       = self.read_var('WEBSERVER', 'filedir')
        self.cvs_root       = self.read_var('CVS', 'cvsroot')
        self.cache_dir      = self.read_var('MIRROR', 'cachedir')
        self.xslt_html      = self.read_var('XSLT', 'xslt_html')
        self.xslt_chunk     = self.read_var('XSLT', 'xslt_chunk')
        self.xslt_print     = self.read_var('XSLT', 'xslt_print')
        self.smtp_server    = self.read_var('MAIL', 'smtp_server')
        self.admin_email    = self.read_var('MAIL', 'admin_email')
        self.db2omf         = self.read_var('MAKE', 'db2omf')
        self.wt2db          = self.read_var('MAKE', 'wt2db')

    def read_var(self, section, name):
        if not self.config.has_section(section) :
            raise ConfigFileReadErrorException("File '" + self.config_file + "' is missing or does not contain a '" + section + "' section")

        if not self.config.has_option(section, name):
            raise ConfigFileReadErrorException("Can't read option '" + name + "' from " + self.config_file)

        return self.config.get(section, name)

    def debug(self):
        text = 'config_file=' + self.config_file + '\n'
        text += 'project_name=' + self.project_name + '\n'
        text += 'project_short=' + self.project_short + '\n'
        text += 'db_type=' + self.db_type + '\n'
        text += 'db_name=' + self.db_name + '\n'
        text += 'db_host=' + self.db_host + '\n'
        text += 'log_file=' + self.log_file + '\n'
        text += 'log_level=' + str(self.log_level) + '\n'
        text += 'log_sql=' + str(self.log_sql) + '\n'
        text += 'log_console=' + str(self.log_console) + '\n'
        text += 'interface=' + self.interface + '\n'
        text += 'port=' + self.port + '\n'
        text += 'hostname=' + self.hostname + '\n'
        text += 'root_dir=' + self.root_dir + '\n'
        text += 'cvs_root=' + self.cvs_root + '\n'
        text += 'file_dir=' + self.file_dir + '\n'
        text += 'cache_dir=' + self.cache_dir + '\n'
        text += 'xslt_html=' + self.xslt_html + '\n'
        text += 'xslt_chunk=' + self.xslt_chunk + '\n'
        text += 'xslt_print=' + self.xslt_print + '\n'
        text += 'smtp_server=' + self.smtp_server + '\n'
        text += 'admin_email=' + self.admin_email + '\n'
        text += 'db2omf=' + self.db2omf + '\n'
        text += 'wt2db=' + self.wt2db + '\n'
        return text

    def print_debug(self):
        print self.debug()


## exports ##

config = Config()
        
# main
if __name__=='__main__' :
    print "Running unit tests..."
    config.print_debug()
    print "Unit tests complete."
