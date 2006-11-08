#!/usr/bin/perl -W

# (P) & (C) 2006 by Peter Bieringer <pb at bieringer dot de>

# This program extracts URLs from a Lyx file and checks them

# 20060822/PB: major improvement, add support for persistent XML database

use strict;
use Net::HTTP;
use Net::FTP;
use Net::NNTP;
use Crypt::SSLeay;
use LWP::UserAgent;
use XML::Dumper;
use Socket;
use Socket6;

my $debug = 0xffff & ~(0x20);

my %urls;
my $p_urls = \%urls;

my %hosts;

my $time = time;

my $dbfile;

my $dbfile_suffix = ".url-database.xml";


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

sub check_ipv6only($$) {
	print STDERR "DEBUG/check_ipv6only: begin\n" if ($debug & 0x10);
	print STDERR "DEBUG/check_ipv6only: check: " . $_[0] . "\n" if ($debug & 0x10);

	my ($family, $socktype, $proto, $saddr, $canonname, @res);

	@res = getaddrinfo($_[0], $_[1], AF_INET6, SOCK_STREAM);

	if (scalar(@res) < 5) {
		return 1;
	};

	my ($host, $port);
	$family = -1;

	while (scalar(@res) >= 5) {
		($family, $socktype, $proto, $saddr, $canonname, @res) = @res;

		($host, $port) = getnameinfo($saddr, NI_NUMERICHOST | NI_NUMERICSERV);

		print STDERR "Trying to connect to $host port port $port...\n";

		socket(Socket_Handle, $family, $socktype, $proto) || next;
		connect(Socket_Handle, $saddr) && last;

		close(Socket_Handle);
		$family = -1;
	};

	if ($family != -1) {
		print STDERR "connected to $host port $port\n";
		close(Socket_Handle);
		return 0;
	} else {
		warn "connect attempt failed\n";
		return 1;
	};
};

sub check_urls() {
	print STDERR "DEBUG/check_urls: begin\n" if ($debug & 0x10);

	for my $url (sort keys %$p_urls) {
		if (defined $$p_urls{$url}->{'checktime'}) {
			if ($$p_urls{$url}->{'checktime'} > $time - 60*60*24*7) {
				if (defined $$p_urls{$url}->{'checkresult'} && $$p_urls{$url}->{'checkresult'} =~ /^ok/) {
					# Checked during last 7 days - skip
					print STDERR "DEBUG/check_urls: checked during last 7 days - skip: $url\n" if ($debug & 0x10);
					next;
				};
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
			} elsif ($proto eq "nntp") {
				$port = 119;
			} elsif ($proto eq "https") {
				$port = 443;
			};
		};

		# Strip trailing #
		$uri =~ s/#.*//;

		if (length($uri) == 0) {
			$status = "URI is empty";
			goto ("LABEL_PRINT");
		};

		my $s;

		if ($proto eq "ftp") {
			# Check FTP
			print STDERR "DEBUG/check_urls: open FTP connection: $host:$port\n" if ($debug & 0x20);
			$s = Net::FTP->new(Host => $host, Port => $port, Timeout => 30, Passive => 1);

			if (! defined $s) {
				$status = "Host not found";
				if (! check_ipv6only($host,$port)) {
					$status = "ok (IPv6 only)";
				};
				goto ("LABEL_PRINT");
			};

			if (!$s->login("anonymous",'-anonymous@')) {
				$status = "FTP anonymous login failed";
				goto ("LABEL_PRINT");
			};

			if (!$s->cwd($uri)) {
				$status = "FTP can't change to directory $uri";
				goto ("LABEL_PRINT");
			};

			$status = "ok";
			$s->quit;

		} elsif ($proto eq "nntp") {
			my $s = Net::NNTP->new(Host => $host, Timeout => 30);

			if (! defined $s) {
				$status = "Host not found";
				if (! check_ipv6only($host,$port)) {
					$status = "ok (IPv6 only)";
				};
				goto ("LABEL_PRINT");
			};
			$status = "ok";

			$s->quit;

		} elsif ($proto eq "https") {
			my $ua = new LWP::UserAgent;
			my $req = new HTTP::Request('HEAD', $url);
			my $res = $ua->request($req);

			my $code =  $res->code;

			if ($code !~ /^[23]/) {
				$status = "HTTPS reports: $code";
			} else {
				$status = "ok";
			};
		} elsif ($proto eq "http") {
			# Check HTTP
			print STDERR "DEBUG/check_urls: open HTTP connection: $host:$port\n" if ($debug & 0x20);
			$s = Net::HTTP->new(Host => $host, PeerPort => $port, Timeout => 30);
			if (! defined $s) {
				$status = "Host not found";
				if (! check_ipv6only($host,$port)) {
					$status = "ok (IPv6 only)";
				};
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
		if ($$p_urls{$url}->{'checkresult'} =~ /^ok/) {
			next;
		};

		print "NOTICE: URL has a problem: $url\n";
		print "        Description      : " . $$p_urls{$url}->{'desc'} . "\n";
		print "        Line number      : " . $$p_urls{$url}->{'line'} . "\n";
		print "        Result           : " . $$p_urls{$url}->{'checkresult'} . "\n";
		print "\n";
	};
};


sub check_rfc_urls() {
	print STDERR "DEBUG/check_rfc_urls: begin\n" if ($debug & 0x10);

	for my $url (sort { $$p_urls{$a}->{'line'} <=> $$p_urls{$b}->{'line'} } ( keys %$p_urls)) {
		if ($url =~ /rfc[0-9]{1,4}/) {
			print "NOTICE: URL points to RFC: $url\n";
			print "        Description      : " . $$p_urls{$url}->{'desc'} . "\n";
			print "        Line number      : " . $$p_urls{$url}->{'line'} . "\n";
			print "\n";
		};
	};
};


##### Main

if (! defined $ARGV[0] || $ARGV[0] eq "") {
	die "Missing file name (arg1)";
};

if (! -f $ARGV[0]) {
	die "Argument 1 is not an existing file: " . $ARGV[0];
};

$dbfile = $ARGV[0] . $dbfile_suffix;

load_urls();
extract_urls($ARGV[0]);
cleanup_old_urls();
check_urls();
store_urls();
check_rfc_urls();
report_urls();
