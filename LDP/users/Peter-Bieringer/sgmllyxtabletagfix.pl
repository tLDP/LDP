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
#  -> This bug is fixed in LyX 1.1.6fix4
#
# Example:
#  - <colspec colname="col0" align="center"/>
#  + <colspec colname="col0" align="center">
#
# Changes:
#  20020119/PB: Initial release
#  20020125/PB: Minor review
#  20020130/PB: add comment
#

print STDERR "INF : Fix 'colspec' lines\n";

while (<STDIN>) {
	my $line = $_;
	chomp $line;

	#print "$line";
	#print "\n";

	if ($line =~ /^<colspec/) {
		if ($line =~ /\/>$/) {
			print STDERR "C";

			# Substitute '/>' with '>'
			$line =~ s/\/>$/>/g;
		};
	};

       	print $line . "\n";
};
print STDERR "\n";
