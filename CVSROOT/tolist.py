#!/usr/bin/python
#
# CVSROOT/users ---> ezmlm list extra allow subscribers
# (c) sergiusz paw³owicz 2001 <ser@pld.org.pl> - BSD License
#   [- forgive me, it`s almost my first python program]
# 
# $Id$

# config: full path to users file
users="/home/cvsroot/CVSROOT/users"

# now we can open the users file
users_in = open(users)

# take the first line
users_line = users_in.readline()

# test for the last line in users file (last line is always empty string)
while users_line != '' :

	# let`s split the line into three strings in the list:
	# 	[0] - login name
	# 	[1] - e-mail address
	# 	[2] - full name
	import string
	users_splitted = string.split(users_line, ':')

	# to create a subscription
	import os
	os.popen('/usr/local/bin/ezmlm-sub /home/linuxdoc/cvs-commits/allow ' + 
		users_splitted[0]+'@tldp.org')
	os.popen('/usr/local/bin/ezmlm-sub /home/linuxdoc/cvs-commits/allow ' +
		users_splitted[0]+'@gabber.metalab.unc.edu')
	os.popen('/usr/local/bin/ezmlm-sub /home/linuxdoc/staff/allow ' +
		users_splitted[0]+'@tldp.org')
	os.popen('/usr/local/bin/ezmlm-sub /home/linuxdoc/lampadas-commits/allow ' +
		users_splitted[0]+'@tldp.org')

	# take next line from users file
	users_line = users_in.readline()

else:
	# to close the users file
	users_in.close()

# happy end.
