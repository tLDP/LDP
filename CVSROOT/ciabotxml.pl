#!/usr/bin/perl -w
#
# ciabot -- Mail a CVS log message to a given address, for the purposes of CIA
#
# Loosely based on cvslog by Russ Allbery <rra@stanford.edu>
# Copyright 1998  Board of Trustees, Leland Stanford Jr. University
#
# Copyright 2001, 2003  Petr Baudis <pasky@ucw.cz>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2, as published by the
# Free Software Foundation.
#
# The master location of this file is
# http://pasky.or.cz/~pasky/dev/cvs/ciabot.pl.
#
# This program is designed to run from the loginfo CVS administration file. It
# takes a log message, massaging it and mailing it to the address given below.
#
# Its record in the loginfo file should look like:
#
#       ALL        $CVSROOT/CVSROOT/ciabot.pl %s $USER project from_email dest_email
#
# Note that the last three parameters are optional, you can alternatively change
# the defaults below in the configuration section.
#
# $Id$

use strict;
use vars qw ($project $from_email $dest_email @sendmail $sync_delay);




### Configuration

# Project name (as known to CIA).
$project = 'TLDP';

# The from address in generated mails.
$from_email = 'ser@tldp.org';

# Mail all reports to this address.
$dest_email = 'cia@pld-linux.org';

# Path to your sendmail binary. If you have it at a different place (and
# outside of $PATH), add your location at the start of this list. By all means
# keep the trailing empty string in the array.
@sendmail = ('sendmail', '/usr/lib/sendmail', '/usr/sbin/sendmail', '');

# Number of seconds to wait for possible concurrent instances. CVS calls up
# this script for each involved directory separately and this is the sync
# delay. 5s looks as a safe value, but feel free to increase if you are running
# this on a slower (or overloaded) machine or if you have really a lot of
# directories.
$sync_delay = 5;




### The code itself

use vars qw ($user $module $tag @files $logmsg);

my @dir; # This array stores all the affected directories
my @dirfiles;  # This array is mapped to the @dir array and contains files
               # affected in each directory



### Input data loading


# These arguments are from %s; first the relative path in the repository
# and then the list of files modified.

@files = split (' ', ($ARGV[0] or ''));
$dir[0] = shift @files or die "$0: no directory specified\n";
$dirfiles[0] = "@files" or die "$0: no files specified\n";


# Guess module name.

$module = $dir[0]; $module =~ s#/.*##;


# Figure out who is doing the update.

$user = $ARGV[1];


# Use the optional parameters, if supplied.

$project = $ARGV[2] if $ARGV[2];
$from_email = $ARGV[3] if $ARGV[3];
$dest_email = $ARGV[4] if $ARGV[4];


# Parse stdin (what's interesting is the tag and log message)

while (<STDIN>) {
  $tag = $1 if /^\s*Tag: ([a-zA-Z0-9_-]+)/;
  last if /^Log Message/;
}

while (<STDIN>) {
  next unless ($_ and $_ ne "\n" and $_ ne "\r\n");
  $logmsg .= $_;
}



### Sync between the multiple instances potentially being ran simultanously

my $sum; # _VERY_ simple hash of the log message. It is really weak, but I'm
         # lazy and it's really sorta exceptional to even get more commits
         # running simultanously anyway.
map { $sum += ord $_ } split(//, $logmsg);

my $syncfile; # Name of the file used for syncing
$syncfile = "/tmp/cvscia.$project.$module.$sum";


if (-f $syncfile and -w $syncfile) {
  # The synchronization file for this file already exists, so we are not the
  # first ones. So let's just dump what we know and exit.

  open(FF, ">>$syncfile") or die "aieee... can't log, can't log! $syncfile blocked!";
  print FF "$dirfiles[0]!@!$dir[0]\n";
  close(FF);
  exit;

} else {
  # We are the first one! Thus, we'll fork, exit the original instance, and
  # wait a bit with the new one. Then we'll grab what the others collected and
  # go on.

  # We don't need to care about permissions since all the instances of the one
  # commit will obviously live as the same user.

  # system("touch") in a different way
  open(FF, ">>$syncfile") or die "aieee... can't log, can't log! $syncfile blocked!";
  close(FF);

  exit if (fork);
  sleep($sync_delay);

  open(FF, $syncfile);
  my ($dirnum) = 1; # 0 is the one we got triggerred for
  while (<FF>) {
    chomp;
    ($dirfiles[$dirnum], $dir[$dirnum]) = split(/!@!/);
    $dirnum++;
  }
  close(FF);

  unlink($syncfile);
}



### Send out the mail


# Open our mail program

foreach my $sendmail (@sendmail) {
  die "$0: cannot fork sendmail: $!\n" unless ($sendmail);
  open (MAIL, "| $sendmail -t -oi -oem") and last;
}


# The mail header

print MAIL <<EOM;
From: $from_email
To: $dest_email
Content-type: text/xml
Subject: DeliverXML

EOM


# Skip all this nonsense if we're doing XML output.

my ($VERSION) = '$Revision$' =~ / (\d+\.\d+) /;
my $ts = time;

print MAIL <<EM
<message>
   <generator>
       <name>CIA Perl client for CVS</name>
       <version>$VERSION</version>
       <url>http://pasky.or.cz/~pasky/dev/cvs/ciabot.pl</url>
   </generator>
   <source>
       <project>$project</project>
       <module>$module</module>
EM
;
print MAIL "       <branch>$tag</branch>" if ($tag);
print MAIL <<EM
   </source>
   <timestamp>
       $ts
   </timestamp>
   <body>
       <commit>
           <author>$user</author>
           <files>
EM
;

for (my $dirnum = 0; $dirnum < @dir; $dirnum++) {
  map {
    $_ = $dir[$dirnum] . '/' . $_;
    s#^.*?/##; # weed out the module name
    s/ /&nbsp;/g;
    s/</&lt;/g;
    s/>/&gt;/g;
    print MAIL "  <file>$_</file>\n";
  } split(/ /, $dirfiles[$dirnum]);
}

print MAIL <<EM
           </files>
           <log>
$logmsg
           </log>
       </commit>
   </body>
</message>
EM
;


# Close the mail

close MAIL;
die "$0: sendmail exit status " . $? >> 8 . "\n" unless ($? == 0);
