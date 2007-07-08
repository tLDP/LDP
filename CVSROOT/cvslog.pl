#!/usr/bin/perl -w
#
# cvslog -- Mail the CVS log message to a given address.
#
# Loosely based on cvslog by Russ Allbery <rra@stanford.edu>
# Copyright 1998  Board of Trustees, Leland Stanford Jr. University
#
# Copyright 2001, 2003, 2004  Petr Baudis <pasky@ucw.cz>
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
use vars qw ($x_mailer $project $repository $from_email $dest_email $reply_email
		$CVS $diffstat $cvsweb_url $help_msg $sync_delay $max_diff_lines
		$show_diffstat $show_diff $login $subj_files $subj_maxlength
		$withthreading_email $messageid_email $mail_contenttype $mail_contenttransen);




### Configuration

# Project name.
$project = 'LDP';

# The path to the repository.  If your platform or CVS implementation doesn't
# pass the full path to the cvslog script in $0 (or if your cvslog script
# isn't in the CVSROOT directory of your repository for some reason), you will
# need to explicitly set $REPOSITORY to the root directory of your repository
# (the same thing that you would set CVSROOT to).
$repository = '/cvsroot'; # ($0 =~ m#^(.*)/CVSROOT/cvslog$#);

# The from address in the generated mails.

$login = $ENV{'CVS_USER'} || $ENV{'CVS_USERNAME'} || $ENV{'CVSUSER'} ||
	getlogin || (getpwuid($<))[0] || "nobody";
$from_email = "$login <$login\@tldp.org>";

# Mail all reports to this address.
#$dest_email = 'elinks-cvs@v.or.cz, pasky@pasky.ji.cz, fonseca@diku.dk, zas@norz.org';
$dest_email = 'cvs-commits@en.tldp.org';
#for testing, sometimes useful:
#$dest_email = 'ser@metalab.unc.edu';

# Email address all the replies should go at.
$reply_email = 'discuss@en.tldp.org';

# X-mailer for better identification
$x_mailer = '$Id$';

# suffix of Message-ID in email header
$messageid_email = '@tldp.org';

# with threading?
$withthreading_email = 1;

# mail content-type
$mail_contenttype="text/plain; charset=iso-8859-1";

# mail content-transfer-encoding
$mail_contenttransen="8bit";

# The cvs binary location + name (full path to the executable). If in doubt,
# try just 'cvs' and hope. Otherwise, /usr/bin/cvs or /usr/local/bin/cvs could
# do.
$CVS = '/usr/bin/cvs';

# The diffstat binary location + name (full path to the executable) plus the
# additional arguments you want to pass to it. If in doubt, keep the default
# arguments and try just 'diffstat' and hope. Otherwise, /usr/bin/diffstat or
# /usr/local/bin/diffstat could do. Just comment it out if you don't have
# diffstat enabled.
$diffstat = '/usr/bin/diffstat -p0 -w 72';

# URL of cvsweb. Just comment out if you don't have any.
$cvsweb_url = 'http://cvs.tldp.org/go.to/LDP';

# The leading message of the mail:
$help_msg = "This is an automated notification of a change to the $project CVS tree.";

# Number of seconds to wait for possible concurrent instances. CVS calls up
# this script for each involved directory separately and this is the sync
# delay. 5s looks as a safe value, but feel free to increase if you are running
# this on a slower (or overloaded) machine or if you have really a lot of
# directories.
$sync_delay = 5;

# Maximal number of lines the diff can contain. If it will be longer, it is
# going to be trimmed to this length.
# Assuming that each line is avg. 60 lines long and we don't want to have mails
# bigger than 35kb, the maximal number of lines would be 597.
$max_diff_lines = 597;

# Whether you want the diffstat of changes to be sent in the message.
$show_diffstat = 0;

# Whether you want the diff of changes to be sent in the message.
$show_diff = 1;

# Whether you want the affected files list in subject
$subj_files=1;

# How long the subject can be
$subj_maxlength=78;

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

$htag = $tag ? $tag : "HEAD";

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

    print FF join("\t", $dirs[0]->{name}, $dirs[0]->{type}, @t) . "\n";
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

    my ($zdir, $ztype, @zfiles) = split ("\t");
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

open (MAIL, '| /var/qmail/bin/sendmail -t -oi -oem')
    or die "$0: cannot fork sendmail: $!\n";


# Fill in date

my ($date);
$date = scalar gmtime;




# Compose the mail

# TODO: Use CVSROOT/users to determine the committer's realname and email and
# add it to the reply-to / mail-followup-to list. --pasky

my ($VERSION) = '$Revision$' =~ / (\d+\.\d+) /;


# Subject files, references and 
# future "files affected part" (List the files being changed, plus the cvsweb URLs)


my $files_affected_part="";
my $subj_file_list="";
my $references="";
my $messageid="";
my $cvsweb_part="";
for (my $i = 0; $i < @dirs; $i++) {
  my $dirs = $dirs[$i];
  my $dir = $dirs->{name};
  my $subdir = $dir;
  $subdir =~ s!^[^/]*/?!!;
  $subdir .= '/' if $subdir ne '';

  $files_affected_part .= "\n$dir:\n   ";

  if ($dirs[$i]->{type} eq 'directory') {
    $files_affected_part .= "New directory\n";

  } else {
    my $commits = $dirs->{commits};

    for (my $j = 0; $j < @$commits; $j++) {
      my $ref;
      my $commit = $commits->[$j];
      my ($name, $oldrev, $newrev, $op) = ("NAME","NONE","NONE",-1);
      ($name, $oldrev, $newrev, $op) = ($commit->{name}, $commit->{oldrev}, $commit->{newrev}, $commit->{op});
      $subj_file_list .= "$subdir$name";
      $subj_file_list .= " (NEW)" if ($op eq 'add');
      $subj_file_list .= " (REMOVED)" if ($op eq 'remove');
      $subj_file_list .= ", ";
      $files_affected_part .= "$name ($oldrev -> $newrev) ";
      $files_affected_part .= " (NEW)" if ($op eq 'add');
      $files_affected_part .= " (REMOVED)" if ($op eq 'remove');
      $files_affected_part .= " (?! contact devils)" if ($op eq '?');
      $files_affected_part .= ", " if $j < @$commits-1;
#      $files_affected_part .= "\n";
      $cvsweb_part .= "    $cvsweb_url/$dir/$name?r1=$oldrev&r2=$newrev\n"
        if defined $cvsweb_url and $op ne 'add' and $op ne 'remove';
      $ref=$dir."_".$name.".".$newrev;
      $ref =~ s/[^a-zA-Z0-9.]/_/g;
      $messageid="<".$ref.$messageid_email.">";
      $ref=$dir."_".$name.".".$oldrev;
      $ref =~ s/[^a-zA-Z0-9.]/_/g;
      $references.=" <". $ref. $messageid_email .">";
    }
  }
}

# Fill in subj and possibly cut it

my ($subj);
$subj_file_list =~ s/, $/ /;
$subj = "Subject: $module".($tag?" ($tag)":"").": ".($subj_files?$subj_file_list:"").$logmsg;
$subj =~ s/\n/ /g; $subj =~ s/ *$//;
$subj = substr($subj, 0, $subj_maxlength-3) . '...' if (length($subj) > $subj_maxlength);
my $keywords="DEV-$user, MOD-$module, TAG-".($tag?$tag:"HEAD").", ". $subj_file_list;

print MAIL <<EOM;
From: $from_email
To: $dest_email
Reply-To: $reply_email
Mail-Followup-To: $reply_email
X-CVS: $user\@$project:$module
X-CVS-Module: $module
User-Agent: cvslog.pl/$VERSION
$subj
Message-ID: $messageid
X-Mailer: $x_mailer
MIME-Version: 1.0
Content-Transfer-Encoding: $mail_contenttransen
Content-Type: $mail_contenttype
Keywords: $keywords
EOM

if ($withthreading_email) {
  print MAIL <<EOM;
References: $references
In-Reply-To: $references
EOM
}

my $msgheader = sprintf ("%-36s %s\n%-36s %s", "Author: $user", "Date: $date GMT","Module: $module"," Tag: $htag");
$logmsg =~ s/\n+/\n/gm;

print MAIL <<EOM;

$msgheader
EOM

print MAIL <<EOM;
---- Log message:
$logmsg
EOM

print MAIL <<EOM;
---- Files affected:$files_affected_part
EOM


goto end_diff unless $show_diff or $show_diffstat;

print MAIL <<EOM;

---- Diffs:
EOM

# And now the diffs!

my @diff;

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

    push (@diff, "\n" . ("=" x 64) . "\n");
    push (@diff, @difflines);
  }
}

push (@diff, ("=" x 64) . "\n");

# Diffstat

my $dstmp = '/tmp/cvslog.diffstat.'.$$;
if ($diffstat and $show_diffstat and open (DSTMP, '>' . $dstmp)) {
  print DSTMP @diff;
  close DSTMP;
  my $pid = open (DIFFSTAT, '-|');
  if (!defined $pid) {
    die "$0: can't fork diffstat: $!\n";
  } elsif ($pid == 0) {
    open (STDERR, '>&STDOUT') or die "$0: can't reopen stderr: $!\n";
    exec (split(/\s+/, $diffstat), $dstmp)
      	or die "$0: can't fork diffstat: $!\n";
  } else {
    my @diffstat = <DIFFSTAT>;
    close DIFFSTAT;
    print MAIL @diffstat;
    print MAIL "\n";
  }
  unlink ($dstmp);
}

goto end_diff unless $show_diff;

if (@diff > $max_diff_lines) {
  @diff = splice(@diff, 0, $max_diff_lines);
  print MAIL @diff;
  print MAIL "<<Diff was trimmed, longer than $max_diff_lines lines>>\n";
} else {
  print MAIL @diff;
}

end_diff:

if ($cvsweb_part ne ""){
  print MAIL <<EOM;

---- CVS-web:
$cvsweb_part
EOM
}

# Send it to the world

close MAIL;
die "$0: sendmail exit status " . $? >> 8 . "\n" unless ($? == 0);


# vi: set sw=2:
