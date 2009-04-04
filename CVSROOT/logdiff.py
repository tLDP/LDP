#!/usr/bin/python
#  -*- Python -*-

"""Complicated notification for CVS checkins.

$Id$
-----------------------------------------------------------------------
Taken from
http://cvs.sourceforge.net/cgi-bin/viewcvs.cgi/mailman/CVSROOT/syncmail
by arekm@pld-linux.org and adopted by serek.
-----------------------------------------------------------------------

This script is used to provide email notifications of changes to the CVS
repository.  These email changes will include context diffs of the changes.
Really big diffs will be trimmed.

This script is run from a CVS loginfo file (see $CVSROOT/CVSROOT/loginfo).  To
set this up, create a loginfo entry that looks something like this:

    mymodule /path/to/this/script %%s some-email-addr@your.domain

In this example, whenever a checkin that matches `mymodule' is made, this
script is invoked, which will generate the diff containing email, and send it
to some-email-addr@your.domain.

    Note: This module used to also do repository synchronizations via
    rsync-over-ssh, but since the repository has been moved to SourceForge,
    this is no longer necessary.  The syncing functionality has been ripped
    out in the 3.0, which simplifies it considerably.  Access the 2.x versions
    to refer to this functionality.  Because of this, the script is misnamed.

It no longer makes sense to run this script from the command line.  Doing so
will only print out this usage information.

Usage:

    %(PROGRAM)s [options] <%%S> email-addr [email-addr ...]

Where options is:

    --module
    -m
    	[Required!] Module name as written to "modules" file.

    --cvsroot=<path>
        Use <path> as the environment variable CVSROOT.  Otherwise this
        variable must exist in the environment.

    --help
    -h
        Print this text.

    --context=#
    -C #
        Include # lines of context around lines that differ (default: 2).

    -c
        Produce a context diff (default).

    -u
        Produce a unified diff (smaller, but harder to read).

    <%%S>
        CVS %%s loginfo expansion.  When invoked by CVS, this will be a single
        string containing the directory the checkin is being made in, relative
        to $CVSROOT, followed by the list of files that are changing.  If the
        %%s in the loginfo file is %%{sVv}, context diffs for each of the
        modified files are included in any email messages that are generated.

    email-addrs
        At least one email address.

"""

# -----------------------------------------------------------
# Config start

# Which SMTP server we wanna use?
our_smtp = "152.46.7.36"
addr_suffix = "tldp.org"
passwd_users_file = "/etc/passwd"

# Config end. Do not change anything below.
# -----------------------------------------------------------

import os
import sys
import string
import time
import getopt
import smtplib
import mimify



# Diff trimming stuff
DIFF_HEAD_LINES = 20
DIFF_TAIL_LINES = 20
DIFF_TRUNCATE_IF_LARGER = 1000

PROGRAM = sys.argv[0]



def usage(code, msg=''):
    print __doc__ % globals()
    if msg:
        print msg
    sys.exit(code)



def calculate_diff(filespec, contextlines):
    commit_message = " "
    try:
        file, oldrev, newrev = string.split(filespec, ',')
    except ValueError:
        # No diff to report
        return '***** Bogus filespec: %s' % filespec
    if oldrev == 'NONE':
        try:
            if os.path.exists(file):
                fp = open(file)
            else:
                update_cmd = 'cvs -fn update -r %s -p %s' % (newrev, file)
                fp = os.popen(update_cmd)
            lines = fp.readlines()
            fp.close()
            lines.insert(0, '--- NEW FILE: %s ---\n' % file)
        except IOError, e:
            lines = ['***** Error reading new file: ',
                     str(e), '\n***** file: ', file, ' cwd: ', os.getcwd()]
    elif newrev == 'NONE':
        lines = ['--- %s DELETED ---\n' % file]
    else:
	# get commit message:
	diffcmd = "/usr/bin/cvs log -N -r%s %s"  % (newrev, file)
	fp = os.popen(diffcmd)
	commit_message = fp.readlines()
	sts = fp.close()
	# cut unwanted fields of log file
	commit_message[0] = "Changed "
	commit_message[2:10] = []
	commit_message[-1] = " "
        # This /has/ to happen in the background, otherwise we'll run into CVS
        # lock contention.  What a crock.
        if contextlines > 0:
            difftype = "-C " + str(contextlines)
        else:
            difftype = "-u"
        diffcmd = "/usr/bin/cvs -f diff -kk %s --minimal -r %s -r %s '%s'" % (
            difftype, oldrev, newrev, file)
        fp = os.popen(diffcmd)
        lines = fp.readlines()
        sts = fp.close()
        # ignore the error code, it always seems to be 1 :(
##        if sts:
##            return 'Error code %d occurred during diff\n' % (sts >> 8)
    if len(lines) > DIFF_TRUNCATE_IF_LARGER:
        removedlines = len(lines) - DIFF_HEAD_LINES - DIFF_TAIL_LINES
        del lines[DIFF_HEAD_LINES:-DIFF_TAIL_LINES]
        lines.insert(DIFF_HEAD_LINES,
                     '[...%d lines suppressed...]\n' % removedlines)
    joined_info = string.join(commit_message, '') + "\r\n\r\n" + string.join(lines, '')
    return joined_info



def blast_mail(mail_from, PEOPLE, filestodiff, contextlines, module_name):
    # cannot wait for child process or that will cause parent to retain cvs
    # lock for too long.  Urg!
    if not os.fork():
        # in the child
        # give up the lock you cvs thang!
        time.sleep(2)
	# get full name of commit author
	users_in = open(passwd_users_file, 'r')
	users_line = users_in.readline()
	while users_line != '' :
	    users_splitted = string.split(users_line, ':')
	    if users_splitted[0] == mail_from :
		    full_name = users_splitted[4]
	    users_line = users_in.readline()
	# if there is more then one destination e-mail, split them
	dest_addr = string.split(PEOPLE)
	# define our codepage for MIME
	mimify.CHARSET="ISO-8859-2"
	# message body starting with headers
	msgbody = "From: " +  mimify.mime_encode_header(full_name) + " <" + mail_from + "@" + addr_suffix + ">" + "\r\n"
	msgbody = mimify.mime_encode_header(msgbody)
	msgbody = msgbody + "To: " + string.join(dest_addr, ", ") + "\r\n"
	msgbody = msgbody + "Reply-To: \"General Discuss\" <discuss@en.tldp.org>" + "\n"
	msgbody = msgbody + "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) + "\r\n"
	msgbody = msgbody + "Subject: " + module_name + " " + string.join(filestodiff, " , ") + "\r\n"
	msgbody = msgbody + "X-Mailer: $Id$\r\n"
	msgbody = msgbody + "Content-Type: text/plain; charset=iso-8859-2" + "\r\n"
	msgbody = msgbody + "MIME-Version: 1.0" + "\r\n"
	msgbody = msgbody + "Content-Transfer-Encoding: 8bit" + "\r\n"
	msgbody = msgbody + "\r\n"
	# short info about commit
	msgbody = msgbody + "Module name:    " + module_name + "\r\n"
	msgbody = msgbody + "Changes by:     " + mail_from + "\r\n"
	#msgbody = msgbody + "Changes by:     " + mail_from + " " + time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())  + "GMT \r\n"
	#msgbody = msgbody + "Log message:    " + "\r\n"
	msgbody = msgbody + "\r\n"
        # append the diffs if available
        for file in filestodiff:
            msgbody = msgbody + calculate_diff(file, contextlines)
            msgbody = msgbody + "\r\n"
	# due to bug in python i must issue several deliveries for each address
	for one_address in dest_addr :
	    # smtp part
	    sendit = smtplib.SMTP(our_smtp)
	    sendit.sendmail(mail_from+"@"+addr_suffix, one_address, msgbody)
	    sendit.quit()
        # doesn't matter what code we return, it isn't waited on
        os._exit(0)



# scan args for options
def main():
    contextlines = 2
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hC:cu',
                                   ['module=', 'context=', 'cvsroot=', 'help'])
    except getopt.error, msg:
        usage(1, msg)

    # parse the options
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt == '--cvsroot':
            os.environ['CVSROOT'] = arg
        elif opt in ('-C', '--context'):
            contextlines = int(arg)
        elif opt == '-c':
            if contextlines <= 0:
                contextlines = 2
        elif opt == '-u':
            contextlines = 0
    	elif opt in ('-m', '--module'):
	    module_name = arg

    # What follows is the specification containing the files that were
    # modified.  The argument actually must be split, with the first component
    # containing the directory the checkin is being made in, relative to
    # $CVSROOT, followed by the list of files that are changing.
    if not args:
        usage(1, 'No CVS module specified')
    SUBJECT = args[0]
    CVSNAME = os.environ['CVS_USER']
    specs = string.split(args[0])
    del args[0]

    # The remaining args should be the email addresses
    if not args:
        usage(1, 'No recipients specified')

    # Now do the mail command
    PEOPLE = string.join(args)

    print 'Mailing %s...' % PEOPLE
    if specs == ['-', 'Imported', 'sources']:
        return
    if specs[-3:] == ['-', 'New', 'directory']:
        del specs[-3:]
    elif len(specs) > 2:
        L = specs[:2]
        for s in specs[2:]:
            prev = L[-1]
            if string.count(prev, ",") < 2:
                L[-1] = "%s %s" % (prev, s)
            else:
                L.append(s)
        specs = L
    print 'Generating notification message...'
    blast_mail(os.environ['CVS_USER'], PEOPLE, specs[1:], contextlines, module_name)
    print 'Generating notification message... done.'



if __name__ == '__main__':
    main()
    sys.exit(0)
