#!/usr/bin/perl
#
# $Id$
#
# LyX codeline wrapper tool
#
# (P) & (C) 2002-2009 by Peter Bieringer <pb@bieringer.de>
#
# Published under the GNU GPL licence
#
# Takes LyX code from stdin and pipes a modified to stdout.
#  Wraps length of code lines to a given limit.
#  Marks second and next lines with a given character.
#
# Attention: no warranty that the new LyX code is very well!
#            Use diff to check proper work
#
# Changes:
#  20020118: Initial try
#  20020119: Improve tool, do not touch code lines including LyX tags
#  20090214/PB: adjustments for LyX format 345
#
# Known bugs:
#  * Sure some
#
# Known limitations:
#  * Code lines containing LyX tags are currently not supported and skipped

my $lyx_format_supported = "345";

sub print_long_line ($);

my $TAG_CODE = 0;
my $line_carry = "";
my $lines_original = "";
my $line_limit = 79;
#my $linebreakchar = chr(172);
my $linebreakchar = "¬"; # UTF-8 support

#my $debug = 1;
my $debug = 0;

while (<STDIN>) {
	my $line = $_;
	chomp $line;

	#print "$line";
	#print "\n";
	#
	if ($line =~ /^\\lyxformat ([0-9]+)$/) {
		if ($1 ne $lyx_format_supported) {
			die "Lyx format not supported: $1";
		};
	} elsif ($line =~ /^\\begin_layout Code$/ && $TAG_CODE != 1) {
		print STDERR "INF: Code tag starts\n";
		$TAG_CODE = 1;
		$line_carry = "";
		$lines_original = "";
		next;
	} elsif ($line =~ /^\\end_layout$/ && $TAG_CODE == 1) {
		print STDERR "INF: Code tag ends\n";

		if ($lines_original =~ /\\/) {
			# Ooops, lines contain a LyX tag, currently not supported, so let it be
	               	#print STDERR "WARN: Lines contain LyX code tag, let it like it is\n: '$lines_original'";
                	print STDERR "WARN: Lines contain LyX code tag, let it like it is\n";
			if ($debug & 0x01) { print "G"; };
			print "\\begin_layout Code" . "\n" . $lines_original . "\\end_layout" . "\n";
		} elsif ($lines_original =~ /$linebreakchar/) {
			# Code line already wrapped
                	print STDERR "INF: Code line already wrapped, let it like it is\n";
			if ($debug & 0x01) { print "F"; };
			print "\\begin_layout Code" . "\n" . $lines_original . "\\end_layout" . "\n";
		} else {
			print_long_line $line_carry;
		};

		$TAG_CODE = 0;
		$line_carry = "";
		$lines_original = "";
		next;
	} elsif ($line =~ /^\\layout/ && $TAG_CODE == 1) {
		die "unsupported";
                print STDERR "INF: Code tag ends\n";

		if ($lines_original =~ /\\/) {
			# Ooops, lines contain a LyX tag, currently not supported, so let it be
                	#print STDERR "WARN: Lines contain LyX code tag, let it like it is\n: '$lines_original'";
                	print STDERR "WARN: Lines contain LyX code tag, let it like it is\n";
			if ($debug & 0x01) { print "A"; };
			print "\\begin_layout Code" . "\n" . $lines_original;
		} elsif ($lines_original =~ /$linebreakchar/) {
			# Code line already wrapped
                	print STDERR "INF: Code line already wrapped, let it like it is\n";
			if ($debug & 0x01) { print "B"; };
			print "\\begin_layout Code" . "\n" . $lines_original;
		} else {
			print_long_line $line_carry;
		};

		$line_carry = "";
		$lines_original = "";
                $TAG_CODE = 0;
		print $line . "\n";
		next;
	};

	if ($TAG_CODE != 1) {	
		print $line . "\n";
	} else {
		$lines_original .= $line . "\n";

		if ($line eq "") {
			# empty lines are skipped here
			next;
		};

                print STDERR "INF: Found code line: '" . $line . "'\n";
		$line_carry .= $line;
	};
};

sub print_long_line ($){
	my $line = shift;
	print STDERR "INF: Print code line: '" . $line . "'\n";

	my $l = 0;
	my $c = "";
	
	if (length($line) == 0) {
		if ($debug & 0x01) { print "C"; };
		my $s = "\\begin_layout Code" . "\n" . "\n" . "\\end_layout" . "\n"; 
		print $s;
		return;
	};

	while ($l < length($line)) {
		my $t = 0;
               	print STDERR "INF:  Step: $l\n";

		if ($l == 0) {
			$c = "";
		} else {
			$c =$linebreakchar;
		}

		if (length($line) - $l <= $line_limit) {
			if ($debug & 0x01) { print "D"; };
			my $s = "\\begin_layout Code" . "\n" . $c . substr($line, $l) . "\n" . "\\end_layout" . "\n";
               		print STDERR "INF:  Step end\n";
			print $s;
			print STDERR $s;
			last;
		};

		for ($t = $line_limit; $t > 0; $t--) {
			if (substr($line, $l + $t, 1) eq " ") {
               			print STDERR "INF:  Found <space> at pos: $t\n";
				last;
			};
		};

		if ($t == 0) { $t = $line_limit };
 		print STDERR "INF:  Start printing l=$l t=$t\n";
		if ($debug & 0x01) { print "E"; };
		my $s = "\\begin_layout Code" . "\n" . $c . substr($line, $l, $t) . "\n" . "\\end_layout" . "\n\n";
		print $s;
		print STDERR $s;
		$l = $l + $t;
	};
};

print STDERR "\n\nWARNING: check code using utility 'diff' for proper LyX output!\n";
