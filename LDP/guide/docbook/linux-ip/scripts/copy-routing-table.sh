#! /bin/sh -
#
# copy-routing-table.sh; code fragment to copy a routing table
#
# Copyright (c)2002 SecurePipe, Inc. - http://www.securepipe.com/
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, 
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#

# -- copy_routing_table takes one integer numeric argument which is a valid
#    routing table identifier or a routing table by name which iproute2
#    will find in /etc/iproute2/rt_tables
#
#    this subroutine will remove all entries from the specified routing
#    table (ip route flush table $TABLE)
#
#    it will make an exact copy of the main routing table, but will not
#    add a default route to the new $TABLE
#

# - - - - - - - - - - -
  copy_routing_table () {
# - - - - - - - - - - -
#
# -- accepts one paramater:
#
#    $1:  table identifier for the routing table to create
#
  test "$#" -lt "1"     && return
  DTABLE=$1

  test "$#" -gt "1"     && STABLE="$2"
  test "$STABLE" = ""   && STABLE="main"

  ip route flush table $DTABLE
  ip route show table $STABLE | grep -Ev '^default' \
    | while read ROUTE ; do
      ip route add table $DTABLE $ROUTE
  done

}
