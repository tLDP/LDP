#!/usr/bin/perl -w
#
# cvslog -- Mail the CVS log message to a given address.
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
# This program is designed to run from CVS's loginfo administrative file and
# takes a log message, massaging it and mailing it away. It's a modified
# version of the log script that comes with CVS, but tries to do less (it
# doesn't do cvs status).
#
# It should be run from loginfo with something like:
#
#       ALL         $CVSROOT/CVSROOT/cvslog %{sVv} $USER
#
# Note that it mails everything to the address configured at the top of this
# file.
#
# TODO: attach diffs (under some length, possibly a diffstat instead),
#	non-agressively reformat log messages
#
# $Id$

use strict;
use vars qw ($project $repository $from_email $dest_email $reply_email
		$CVS $cvsweb_url $help_msg $sync_delay);




### Configuration

# Project name.
$project = 'ELinks';

# The path to the repository.  If your platform or CVS implementation doesn't
# pass the full path to the cvslog script in $0 (or if your cvslog script
# isn't in the CVSROOT directory of your repository for some reason), you will
# need to explicitly set $REPOSITORY to the root directory of your repository
# (the same thing that you would set CVSROOT to).
$repository = '/home/cvs/elinks'; # ($0 =~ m#^(.*)/CVSROOT/cvslog$#);

# The from address in the generated mails.
$from_email = 'cvs@pasky.ji.cz';

# Mail all reports to this address.
#$dest_email = 'elinks-cvs@v.or.cz, pasky@pasky.ji.cz, fonseca@diku.dk, zas@norz.org';
$dest_email = 'elinks-cvs@v.or.cz';

# Email address all the replies should go at.
$reply_email = 'elinks-dev@linuxfromscratch.org';

# The cvs binary location + name (full path to the executable). If in doubt,
# try just 'cvs' and hope. Otherwise, /usr/bin/cvs or /usr/local/bin/cvs could
# do.
$CVS = '/opt/cvs/bin/cvs';

# URL of cvsweb. Just comment out if you don't have any.
$cvsweb_url = 'http://cvsweb.elinks.or.cz/cvsweb.cgi';

# The leading message of the mail:
$help_msg = "This is an automated notification of a change to the $project CVS tree.";

# Number of seconds to wait for possible concurrent instances. CVS calls up
# this script for each involved directory separately and this is the sync
# delay. 5s looks as a safe value, but feel free to increase if you are running
# this on a slower (or overloaded) machine or if you have really a lot of
# directories.
$sync_delay = 5;




### The code itself

use vars qw (@dirs $module $user $tag $htag $logmsg);



### Load input data

my (@files, %files); # two ways of accessing the same records


# The arguments are from %{sVv}; first the relative path in the repository
# and then the list of files modified.

my @input = split (' ', ($ARGV[0] or ''));
$dirs[0]->{name} = shift @input or die "$0: no directory specified\n";

if ("@input" eq '- New directory') {
  $dirs[0]->{type} = 'directory';

} else {
  $dirs[0]->{type} = 'checkin';

  foreach (@input) {
    my ($file);

    ($file->{name}, $file->{oldrev}, $file->{newrev}) = split (',');
    $file->{op} = '?';

    push (@files, $file);
    $files{$file->{name}} = $file;

    push (@{$dirs[0]->{commits}}, $file);
  }
}


# Guess module name.

$module = $dirs[0]->{name}; $module =~ s#/.*##;


# Figure out who is doing the update.

$user = $ARGV[1];


# Parse stdin

my $state = 0;
my @op = ('add', 'modify', 'remove');

while (<STDIN>) {
  $tag = $1 if (/^\s*Tag: ([a-zA-Z0-9_-]+)/);
  $state = 1 if /^Added Files:/;
  $state = 2 if /^Modified Files:/;
  $state = 3 if /^Removed Files:/;
  last if /^Log Message/;
  next unless $state;
  foreach (split) {
    $files{$_}->{op} = $op[$state-1];
  }
}

$htag = $tag ? $tag : "<TRUNK>";

while (<STDIN>) {
  $logmsg .= $_;
}



### Check if we want to waste time at this whole thing at all


# The following is an elinks-specific hack, as we don't want to send
# notifications about this file being changed :).

exit if ($files[0]->{name} and $files[0]->{name} eq "ChangeLog");



### Sync between the multiple instances potentially being ran simultaneously

my $sum; # _VERY_ simple hash of the log message. It is really weak, but I'm
         # lazy and it's really sorta exceptional to even get more commits
         # running simultaneously anyway.
map { $sum += ord $_ } split (//, $logmsg);

my $syncfile; # Name of the file used for syncing
$syncfile = "/tmp/cvslog.$project.$module.$sum";


if (-f $syncfile and -w $syncfile) {
  # The synchronization file for this file already exists, so we are not the
  # first ones. So let's just dump what we know and exit.

  open (FF, ">>$syncfile") or die "aieee... can't log, can't log! $syncfile blocked!";

  {
    my @t;
    foreach (@files) {
      push (@t, join(',', $_->{name}, $_->{oldrev}, $_->{newrev}, $_->{op}));
    }

    print FF join(' ', $dirs[0]->{name}, $dirs[0]->{type}, @t) . "\n";
  }

  close (FF);
  exit;

} else {
  # We are the first one! Thus, we'll fork, exit the original instance, and
  # wait a bit with the new one. Then we'll grab what the others collected and
  # go on.

  # We don't need to care about permissions since all the instances of the one
  # commit will obviously live as the same user.

  # system("touch") in a different way
  open (FF, ">>$syncfile") or die "aieee... can't log, can't log! $syncfile blocked!";
  close (FF);

  exit if (fork);
  sleep ($sync_delay);

  open (FF, $syncfile);
  my ($i) = 1;
  while (<FF>) {
    chomp;

    my ($zdir, $ztype, @zfiles) = split (' ');
    $dirs[$i]->{name} = $zdir;
    $dirs[$i]->{type} = $ztype;

    foreach (@zfiles) {
      my ($commit);
      ($commit->{name}, $commit->{oldrev}, $commit->{newrev}, $commit->{op}) = split (',');
      push (@{$dirs[$i]->{commits}}, $commit);
    }

    $i++;
  }
  close (FF);

  unlink ($syncfile);
}



### Send the mail


# Open our mail program

open (MAIL, '| /usr/lib/sendmail -t -oi -oem')
    or die "$0: cannot fork sendmail: $!\n";


# Fill in date

my ($date);
$date = scalar gmtime;


# Fill in subj and possibly cut it

my ($subj);
$subj = "Subject: [$project] $module".($tag?" ($tag)":"")." - $user: $logmsg";
$subj =~ s/\n/ /g; $subj =~ s/ *$//;
$subj = substr($subj, 0, 75) . '...' if (length($subj) > 78);


# Compose the mail

# TODO: Use CVSROOT/users to determine the committer's realname and email and
# add it to the reply-to / mail-followup-to list. --pasky

print MAIL <<EOM;
From: $from_email
To: $dest_email
Reply-To: $reply_email
Mail-Followup-To: $reply_email
X-CVS: $user\@$project:$module
$subj

$help_msg

Author: $user
Module: $module
   Tag: $htag
  Date: $date GMT
EOM

print MAIL <<EOM;

---- Log message:

$logmsg
EOM

print MAIL <<EOM;

---- Files affected:

EOM


# List the files being changed, plus the cvsweb URLs

for (my $i = 0; $i < @dirs; $i++) {
  my $dirs = $dirs[$i];
  my $dir = $dirs->{name};

  print MAIL "$dir:\n";

  if ($dirs[$i]->{type} eq 'directory') {
    print MAIL "   New directory\n";

  } else {
    my $commits = $dirs->{commits};

    for (my $j = 0; $j < @$commits; $j++) {
      my $commit = $commits->[$j];
      my ($name, $oldrev, $newrev, $op) = ($commit->{name}, $commit->{oldrev}, $commit->{newrev}, $commit->{op});
      print MAIL "   $name ($oldrev -> $newrev) ";
      print MAIL " (new)" if ($op eq 'add');
      print MAIL " (removed)" if ($op eq 'remove');
      print MAIL " (?! contact pasky)" if ($op eq '?');
      print MAIL "\n";
      print MAIL "    $cvsweb_url/$dir/$name.diff?r1=$oldrev&r2=$newrev&f=u\n"
        if defined $cvsweb_url and $op ne 'add' and $op ne 'remove';
    }
  }
}


print MAIL <<EOM;


---- Diffs:

EOM


# And now the diffs!

# TODO: Show always diffstat first. --pasky
# TODO: If the diff itself is over N lines, show only the diffstat. --pasky

for (my $i = 0; $i < @dirs; $i++) {
  my $dirs = $dirs[$i];
  my $dir = $dirs->{name};

  next if ($dirs[$i]->{type} ne 'checkin');

  my $commits = $dirs->{commits};

  for (my $j = 0; $j < @$commits; $j++) {
    my $commit = $commits->[$j];

    my $oldrev = $commit->{oldrev}; $oldrev = '0.0' if ($oldrev eq 'NONE');
    my $newrev = $commit->{newrev};
    my $name = $commit->{name};

    # Do not print diffs of removed files. Too boring.
    next if ($newrev eq 'NONE');

    # XXX: Diffs of .po files are too big.
    if ($name =~ /\.po$/) {
      print MAIL "Index: $dir/$name\n";
      print MAIL "<<Some probably quite big and messy diff>>\n";
      next;
    }

    my @difflines;

    my $pid = open (CVS, '-|');
    if (!defined $pid) {
      die "$0: can't fork cvs: $!\n";
    } elsif ($pid == 0) {
      open (STDERR, '>&STDOUT') or die "$0: can't reopen stderr: $!\n";
      exec ($CVS, '-fnQq', '-d', $repository, 'rdiff', '-kk', '-u',
            '-r', $oldrev, '-r', $newrev, $dir.'/'.$name)
		or die "$0: can't fork cvs: $!\n";
    } else {
      @difflines = <CVS>;
      close CVS;
      if (@difflines > 1 and $difflines[1] =~ /failed to read diff file header/) {
        @difflines = ($difflines[0], "<<Binary file>>\n");
      }
    }

    print MAIL @difflines;
  }
}


# Send it to the world

close MAIL;
die "$0: sendmail exit status " . $? >> 8 . "\n" unless ($? == 0);
