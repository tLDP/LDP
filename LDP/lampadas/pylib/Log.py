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
Lampadas Log Module

This module generates the system log for Lampadas.

Logs are assigned one of the following severities:

0 critical errors
1 errors
2 warnings
3 system events
4 debugging messages
"""

from Config import config
import time


# Modules ##################################################################


class Log:
    """
    Write to the system log.
    """

    def __call__(self, level, message):
        self.write(level, message)

    def write(self, level, message):
        if config.log_level >= level:
            logmessage = time.ctime(time.time()) + ' ' + message
            try:
                log_file = open(config.log_file, 'a+')
                log_file.write(logmessage + "\n")
                log_file.close
            except IOError:
                pass

            if config.log_console > 0:
                print logmessage

    def truncate(self):
        log = open(config.log_file, 'w+')
        log.close


log = Log()


if __name__=="__main__":
    config.log_level = 3
    config.log_sql = 1
    config.log_console = 1
    log(1, 'level 1')
    log(2, 'level 2')
    log(3, 'level 3')

