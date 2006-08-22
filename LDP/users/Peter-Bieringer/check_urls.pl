#!/usr/bin/perl -W

# (P) & (C) 2006 by Peter Bieringer <pb at bieringer dot de>

# This program extracts URLs from a Lyx file and checks them

# 20060822/PB: major improvement, add support for persistent XML database

use strict;
use Net::HTTP;
use XML::Dumper;

my $debug = 0xffff & ~(0x20);

my %urls;
my $p_urls = \%urls;

my %hosts;

my $time = time;

my $dbfile = "url_database.xml";


sub quote($) {
	$_[0] =~ s/\`/#60/g; 
	$_[0] =~ s/[\200-\377]/\?/g; 

	return $_[0];
};

sub extract_urls($) {

	print STDERR "DEBUG/extract_urls: open file: $_[0]\n";

	open FILE, "<" . $_[0] || die "ERROR : can't open file: " . $_[0];

	my $linecounter = 0;
	while (<FILE>) {
		$linecounter++;

		chomp $_;

		if ($_ =~ /LatexCommand \\url\[([^]]*)\]{([^}]*)}/) {
			my ($url, $desc);

			$desc = $1;
			$url = $2;

			print STDERR "DEBUG/extract_urls: desc='$desc' URL=$url\n" if ($debug & 0x10);

			if (defined $$p_urls{$url}->{'line'}) {
				print STDERR "DEBUG/extract_urls: URL already found earlier - skip\n" if ($debug & 0x10);

				if ($$p_urls{$url}->{'time'} == $time) {

				} else {
					# from database, update now
					$$p_urls{$url}->{'time'} = $time;	
					$$p_urls{$url}->{'line'} = $linecounter;
					$$p_urls{$url}->{'desc'} = quote($desc);
				};
				next;
			} else {
				$$p_urls{$url}->{'desc'} = quote($desc);
				$$p_urls{$url}->{'time'} = $time;	
				$$p_urls{$url}->{'line'} = $linecounter;
			};
		};
	};

	close(FILE);
};

sub load_urls() {
	if (! -f $dbfile) {
		print STDERR "DEBUG/load_urls: database file doesn't exist, skip load: $dbfile\n" if ($debug & 0x10);
		return 2;
	};

	my $dump = new XML::Dumper;
	print STDERR "DEBUG/load_urls: load database file: $dbfile\n" if ($debug & 0x10);
	$p_urls = $dump->xml2pl($dbfile);
};

sub store_urls() {
	my $dump = new XML::Dumper;
	$dump->pl2xml($p_urls, $dbfile);
};

sub cleanup_old_urls() {
	for my $url (keys %$p_urls) {
		if ($$p_urls{$url}->{'time'} < $time) {
			print STDERR "DEBUG/cleanup_old_urls: remove old URL from database: $url\n" if ($debug & 0x10);
			my $p_h = $$p_urls{$url};
			delete $$p_urls{$url};
		};
	};
};


sub check_urls() {
	print STDERR "DEBUG/check_urls: begin\n" if ($debug & 0x10);

	for my $url (keys %$p_urls) {
		if (defined $$p_urls{$url}->{'checktime'}) {
			if ($$p_urls{$url}->{'checktime'} > $time - 60*60*24*7) {
				# Checked during last 7 days - skip
				print STDERR "DEBUG/check_urls: checked during last 7 days - skip: $url\n" if ($debug & 0x10);
				next;
			};
		};

		print STDERR "DEBUG/check_urls: check now: $url\n" if ($debug & 0x10);

		my ($host, $port);

		my $desc = $$p_urls{$url}->{'desc'};

		my $status = "undef";
		# Extract host
		my ($proto, $hostport, $uri) = $url =~ /^([^:]+):\/\/([^\/]+)(.*)$/;

		if ($hostport =~ /^([^:]):([0-9]+)$/) {
			$host = $1;
			$port = $2;
		} else {
			$host = $hostport;
			if ($proto eq "http") {
				$port = 80;
			} elsif ($proto eq "ftp") {
				$port = 21;
				$status = "skipped (ftp)";
				goto ("LABEL_END");
			} elsif ($proto eq "nntp") {
				$port = 119;
				$status = "skipped (nntp)";
				goto ("LABEL_END");
			} elsif ($proto eq "https") {
				$port = 443;
				$status = "skipped (https)";
				goto ("LABEL_END");
			};
		};

		# Strip trailing #
		$uri =~ s/#.*//;

		if (length($uri) == 0) {
			$status = "URI is empty";
			goto ("LABEL_PRINT");
		};

		# Check
		print STDERR "DEBUG/check_urls: open connection: $host:$port\n" if ($debug & 0x20);
		my $s = Net::HTTP->new(Host => $host, PeerPort => $port, Timeout => 30);
		if (! defined $s) {
			$status = "Host not found";
			goto ("LABEL_PRINT");
		};

		print STDERR "DEBUG/check_urls: send HEAD request: $uri\n" if ($debug & 0x20);
		if ($s->write_request(HEAD => $uri, 'User-Agent' => "Mozilla/5.0") == 0) {
			$status = "trouble with uri";
			goto ("LABEL_PRINT");
		};

		print STDERR "DEBUG/check_urls: wait for response\n" if ($debug & 0x20);
		my($code, $mess, %h) = $s->read_response_headers;

		print STDERR "DEBUG/check_urls: check response\n" if ($debug & 0x10);
		if ($code !~ /^[23]/) {
			$status = "HTTP reports: $code";
		} else {
			$status = "ok";
		};
LABEL_PRINT:
		if ($status ne "ok") {
			print "desc='$desc' URL=$url proto=$proto host=$host port=$port uri='$uri'";
			print " status=$status\n\n";
		};
LABEL_END:
		$$p_urls{$url}->{'checktime'} = $time;
		$$p_urls{$url}->{'checkresult'} = $status;
		undef $s;
		store_urls();
	};
};


sub report_urls() {
	print STDERR "DEBUG/report_urls: begin\n" if ($debug & 0x10);

	for my $url (sort { $$p_urls{$a}->{'line'} <=> $$p_urls{$b}->{'line'} } ( keys %$p_urls)) {
		if ($$p_urls{$url}->{'checkresult'} eq "ok") {
			next;
		};

		print "NOTICE: URL has a problem: $url\n";
		print "        Description      : " . $$p_urls{$url}->{'desc'} . "\n";
		print "        Line number      : " . $$p_urls{$url}->{'line'} . "\n";
		print "        Result           : " . $$p_urls{$url}->{'checkresult'} . "\n";
		print "\n";
	};
};




##### Main

load_urls();
extract_urls($ARGV[0]);
cleanup_old_urls();
check_urls();
store_urls();
report_urls();
