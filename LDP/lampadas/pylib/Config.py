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
    Object that stores configuration parameters
    """

    def __init__(self) :
        """
        Default values
        """
        self.config_file = ''
        # main
        self.project_name = ''
        self.project_short = ''
        # db
        self.db_type = ''
        self.db_name = ''
        self.db_host = ''
        # log
        self.log_file = ''
        self.log_level = 0
        self.log_sql = ''
        self.log_console = 0
        # webserver
        self.interface = ''
        self.port = ''
        self.hostname = ''
        self.root_dir = ''
        self.file_dir = ''
        self.theme = ''
        # cvs
        self.cvs_root = ''
        self.cache_dir = ''
        # xslt
        self.xslt_html = ''
        self.xslt_chunk = ''
        self.xslt_print = ''
        # mail
        self.smtp_server = ''
        self.admin_email = ''
        # make
        self.db2omf = ''
        self.wt2db = ''
        # permissions
        self.world_can_see_unpublished = 0
        self.user_can_see_unpublished = 0
        self.user_can_add_doc = 0
        self.admin_can_add_page = 0
        self.admin_can_edit_page = 0
        self.admin_can_add_string = 0
        self.admin_can_edit_string = 0
        self.admin_can_add_user = 0
        self.admin_can_edit_user = 0

    def __repr__(self):
        text = ['[MAIN]',
                'config_file=' + self.config_file, 
                'project_name=' + self.project_name ,
                'project_short=' + self.project_short ,
                '[DB]',
                'db_type=' + self.db_type ,
                'db_name=' + self.db_name ,
                'db_host=' + self.db_host ,
                '[LOG]',
                'log_file=' + self.log_file ,
                'log_level=' + str(self.log_level) ,
                'log_sql=' + str(self.log_sql) ,
                'log_console=' + str(self.log_console) ,
                '[WEBSERVER]',
                'interface=' + self.interface ,
                'port=' + self.port ,
                'hostname=' + self.hostname ,
                'root_dir=' + self.root_dir ,
                'file_dir=' + self.file_dir ,
                'theme=' + self.theme ,
                '[CVS]',
                'cvs_root=' + self.cvs_root ,
                'cache_dir=' + self.cache_dir ,
                '[XSLT]',
                'xslt_html=' + self.xslt_html ,
                'xslt_chunk=' + self.xslt_chunk ,
                'xslt_print=' + self.xslt_print ,
                '[MAIL]',
                'smtp_server=' + self.smtp_server ,
                'admin_email=' + self.admin_email ,
                '[MAKE]',
                'db2omf=' + self.db2omf ,
                'wt2db=' + self.wt2db ,
                '[PERMISSIONS]',
                'world_can_see_unpublished=' + str(self.world_can_see_unpublished) ,
                'user_can_see_unpublished=' + str(self.user_can_see_unpublished) ,
                'user_can_add_doc=' + str(self.user_can_add_doc) ,
                'admin_can_add_page=' + str(self.admin_can_add_page) ,
                'admin_can_edit_page=' + str(self.admin_can_edit_page) ,
                'admin_can_add_string=' + str(self.admin_can_add_string) ,
                'admin_can_edit_string=' + str(self.admin_can_edit_string) ,
                'admin_can_add_user=' + str(self.admin_can_add_user) ,
                'admin_can_edit_user=' + str(self.admin_can_edit_user) ,
                ]
        return '\n'.join(text)

def get_config_filepath() :
    """
    Returns filepath of config file. Respects LAMPADAS_ETC env variable.
    """
    import os

    msg = ''
    filename = os.getenv('LAMPADAS_ETC')
    if filename==None:
        filename = '/etc/lampadas'
        msg = 'Environment variable LAMPADAS_ETC is undefined.\n'
    filename += '/lampadas.conf'
    if not os.access(filename, os.F_OK):
        raise ConfigFileReadErrorException(msg + filename + " not found.")
    return filename

class ConfigReader :
    
    def __init__(self) :
        import ConfigParser
        self.parser = ConfigParser.ConfigParser()

    def read_config(self,file):
        """
        Read config parameters from open file passed in argument and
        return a Config instance.
        """
        c = Config()
        self.parser.readfp(file)
        r = self.read_var
        c.project_name              = r('MAIN', 'project_name')
        c.project_short             = r('MAIN', 'project_short')
        c.db_type                   = r('DB', 'db_type')
        c.db_name                   = r('DB', 'db_name')
        c.db_host                   = r('DB', 'db_host')
        c.log_file                  = r('LOG', 'log_file')
        c.log_level                 = int(r('LOG', 'log_level'))
        c.log_sql                   = int(r('LOG', 'log_sql'))
        c.log_console               = int(r('LOG', 'log_console'))
        c.interface                 = r('WEBSERVER', 'interface')
        c.port                      = r('WEBSERVER', 'port')
        c.hostname                  = r('WEBSERVER', 'hostname')
        c.root_dir                  = r('WEBSERVER', 'root_dir')
        c.file_dir                  = r('WEBSERVER', 'file_dir')
        c.theme                     = r('WEBSERVER', 'theme')
        c.cvs_root                  = r('CVS', 'cvs_root')
        c.cache_dir                 = r('MIRROR', 'cache_dir')
        c.xslt_html                 = r('XSLT', 'xslt_html')
        c.xslt_chunk                = r('XSLT', 'xslt_chunk')
        c.xslt_print                = r('XSLT', 'xslt_print')
        c.smtp_server               = r('MAIL', 'smtp_server')
        c.admin_email               = r('MAIL', 'admin_email')
        c.db2omf                    = r('MAKE', 'db2omf')
        c.wt2db                     = r('MAKE', 'wt2db')
        c.world_can_see_unpublished = int(r('PERMISSIONS', 'world_can_see_unpublished'))
        c.user_can_see_unpublished  = int(r('PERMISSIONS', 'user_can_see_unpublished'))
        c.user_can_add_doc          = int(r('PERMISSIONS', 'user_can_add_doc'))
        c.admin_can_add_page        = int(r('PERMISSIONS', 'admin_can_add_page'))
        c.admin_can_edit_page       = int(r('PERMISSIONS', 'admin_can_edit_page'))
        c.admin_can_add_string      = int(r('PERMISSIONS', 'admin_can_add_string'))
        c.admin_can_edit_string     = int(r('PERMISSIONS', 'admin_can_edit_string'))
        c.admin_can_add_user        = int(r('PERMISSIONS', 'admin_can_add_user'))
        c.admin_can_edit_user       = int(r('PERMISSIONS', 'admin_can_edit_user'))
        return c

    def _read_var(self, section, name):
        if not self.parser.has_section(section) :
            raise ConfigFileReadErrorException("File '%s' is missing or does not"
                                               " contain a '%s' section"
                                               % (self.config_file,section))

        if not self.parser.has_option(section, name):
            raise ConfigFileReadErrorException("Can't read option '%s' from %s"
                                               % (name,self.config_file))
        return self.parser.get(section, name)


## exports ##

config_file = get_config_filepath()
config = ConfigReader().read_config(open(config_file))
config.config_file = config_file

# main
if __name__=='__main__' :
    print "Running unit tests..."
    config.print_debug()
    print "Unit tests complete."
