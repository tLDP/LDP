#!/usr/bin/perl
#
# $Id$
#
# SGML LyX table tag fix tool
#
# (P) & (C) 2002 by Peter Bieringer <pb@bieringer.de>
#
# Published under the GNU GPL licence
#
# Takes SGML output exported by LyX and fix a bug in the table tag.
# Don't know the reason what causes this, but it is wrong.
#
# Example:
#  - <colspec colname="col0" align="center"/>
#  + <colspec colname="col0" align="center">
#
# Changes:
#  20020119: Initial release
#

while (<STDIN>) {
	my $line = $_;
	chomp $line;

	#print "$line";
	#print "\n";

	if ($line =~ /^<colspec/) {
		print STDERR "INF: Find a 'colspec' line \n";

		# Substitute '/>' with '>'
		$line =~ s/\/>$/>/g;
	};

       	print $line . "\n";
};
