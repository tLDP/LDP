#!/usr/bin/perl
#
# $Id$
#
# SGML LyX qoute entinity fix tool
#
# (P) & (C) 2002 by Peter Bieringer <pb@bieringer.de>
#
# Published under the GNU GPL licence
#
# Takes SGML output exported by LyX and fix a bug regarding quote entinities
# Don't know the reason what causes this, but it is wrong.
#
# Replaces:
#  &ldquo; -> &quot;
#  &rdquo; -> &quot;
#
# Changes:
#  20020125: Initial release
#
# Known bugs:
#  Entinity must be in one line

print STDERR "INF : Replacing special quotes entinities\n";

while (<STDIN>) {
	my $line = $_;
	chomp $line;

	#print "$line";
	#print "\n";

	if ($line =~ /&ldquo;/) {
		print STDERR "<";
		# Substitute 
		$line =~ s/&ldquo;/&quot;/g;
	};
	if ($line =~ /&rdquo;/) {
		print STDERR ">";
		# Substitute 
		$line =~ s/&rdquo;/&quot;/g;
	};


       	print $line . "\n";
};
print STDERR "finished\n";
