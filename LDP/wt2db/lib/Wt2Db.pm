#!/usr/bin/perl
#
# Converts WikiText files into docbook.
#
package Wt2Db;

use File::Basename;
use HTML::Entities;
use FileHandle;
use Exporter;

@ISA = qw(Exporter);
@EXPORT = qw(
	new
	ProcessFile
	ProcessLine
	ProcessEnd
	Buffer
	Reset
	);

&Reset;

# Call this before rerunning ProcessLine to clear state.
# 
sub Reset {
	$level1 = 0;
	$level2 = 0;
	$level3 = 0;
	$orderedlist = 0;
	$listitem = 0;
	$itemizedlist = 0;
	$para = 0;
	$qandaset = 0;
	$qandaentry = 0;
	$answer = 0;

	# These are passed in by the caller
	#
	$txtfile = '';
	$dbfile = '';
	$verbose = 0;
	$doctype = 0;
	$nonet = 0;

	# These maintain state
	#
	$line = '';
	$linenumber = 0;
	$id = '';
	$title = '';
	$buf = '';

	$noparatag = 0;
	$noparadepth = 0;
	$noparaline = 0;
}


# -----------------------------------------------------------

sub new {
	my $that = shift;
	my $class = ref($that) || $that;
	my $self = {};
	bless $self, $class;
	return $self;
}

sub ProcessFile {
	($self, $txtfile, $dbfile, $verbose, $doctype, $nonet, $encoding) = @_;

	# Read from STDIN if no input file given
	# 
	if ($txtfile) {
		if( !(-r $txtfile) ) {
			print "wt2db: ERROR cannot read $f ($!)\n\n";
			exit(1);
		} else {
			$fh = new FileHandle;
			open $fh, "<$txtfile" or die "Cannot open $txtfile ($!)\n";
		}
	} else {
		$fh = STDIN;
	}

	if ($dbfile) {
		$outfh = new FileHandle;
		open $outfh, ">$dbfile" or die "Cannot write to $dbfile\n\n";
	} else {
		$outfh = STDOUT;
	}

	# wrap article if requested
	#
    $encoding = 'ISO-8859-1' unless ($encoding);
	if ($doctype eq 'XML') {
		print "Adding XML DOCTYPE and article tags." if ($verbose);
		$buf = '<?xml version="1.0" encoding="' . $encoding . '" standalone="no"?>' . "\n";
		$buf .= '<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN"' . "\n";
     		$buf .= '    "http://docbook.org/xml/4.1.2/docbookx.dtd"';
		$buf .= "\[\]\>\n";
		$buf .= "\n";
		$buf .= '<article>' . "\n";
	} elsif ($doctype eq 'SGML') {
		print "Adding SGML DOCTYPE and article tags." if ($verbose);
		$buf = '<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook V4.1//EN">' . "\n";
		$buf .= '<article>' . "\n";
	}

	# read in the text file
	#
	while ($originalline = <$fh>) {
		ProcessLine($foo, $originalline);
		print $outfh "$buf";
		$buf = '';
	}

	ProcessEnd();

	# wrap article if requested
	#
	if ($doctype) {
		$buf .= '</article>' . "\n";
	}
	
	print $outfh "$buf";
	$buf = '';
	close $fh;
	close $outfh;
}

sub ProcessLine {
	($foo, $originalline) = @_;
	
	$line = $originalline;
	$linenumber++;

	&trimline;

	# blank lines
	unless ($line) {
		unless ($noparadepth) {
			&closenonsect;
			return;
		}
	}

	# capitalize hints that can be entered in lowercase
	#
	$line =~ s/^q:/Q:/;
	$line =~ s/^a:/A:/;

	# encode entities
	#
#	while ($line =~ //) {
#	}
#	decode_entities($line);
#	encode_entities($line);
		
	# inline docbook
	#
	# parse all links, internal and external
	#
	while ($line =~ /\[\[/) {
		unless ($line =~ /\]\]/) {
			$buf .= "ERROR unterminated '[[' tag on line $linenumber.\n";
		}

		# separate link url from link name
		#
		$link = $line;
		$link=~ s/\n//g;
		$link =~ s/.*?\[\[//;
		$link =~ s/\]\].*?$//;
		if ($link =~ /\|/) {
			$linkname = $link;
			$link =~ s/\|.+$//;
			$linkname =~ s/^\S+\|//;
		} else {
			$linkname = $link;
		}

		# kill quotes inside links, they mess us up because
		# we have to wrap this string with quotes.
		# perhaps it should be encoding the entire URL?
		# 
		$link =~ s/'/%27/g;

		# namespaces are handled differently
		#
		print "$link\n" if ($verbose);

		if ($link =~ /^http:\/\//) {
			$line =~ s/\[\[.*?\]\]/<ulink url='$link'><citetitle>$linkname<\/citetitle><\/ulink>/;
		} elsif ($link =~ /^link:/) {
			$link =~ s/^link://;
			$linkname =~ s/^link://;
			$line =~ s/\[\[.*?\]\]/<xref linkend='$link' endterm='$link'\>\<\/xref\>/;
		} elsif ($link =~ /^mailto:/) {
			$linkname =~ s/^mailto://;
			$line =~ s/\[\[.*?\]\]/<ulink url='$link'><citetitle>$linkname<\/citetitle><\/ulink>/;
		} elsif ($link =~ /^wiki:/) {
			$linkname =~ s/^wiki://;
			$link =~ s/^wiki:/http:\/\/www\.wikipedia\.com\/wiki\.phtml\?title=/;
			$link =~ s/\ /+/;
			$line =~ s/\[\[.*?\]\]/<ulink url='$link'><citetitle>$linkname<\/citetitle><\/ulink>/;
		} elsif ($link =~ /^ldp:/) {
			$linkname =~ s/^ldp://;
			$link =~ s/^ldp://;
			if ($nonet) {
				$line =~ s/\[\[.*?\]\]/<citetitle>$link<\/citetitle>/;
			} else {
				$tempfile = "/tmp/wt2db-" . $rand;
				$cmd = "wget -q http://db.linuxdoc.org/cgi-pub/ldp-xml.pl?name=$link -O $tempfile";
				print "$cmd\n" if ($verbose > 1);
				$return = system("$cmd");
				unless ($return) {
					open(URL, "$tempfile") || die "wt2db: cannot open temporary file ($!)\n\n";
					$link = '';
					while ($url_line = <URL>) {
						$url_line =~ s/\n//;
						if ($url_line =~ /identifier/) {
							$link .= $url_line;
						}
					}
					close(URL);
					unlink $tempfile;
				}
				$link =~ s/^.*?<identifier>//;
				$link =~ s/<\/identifier>.*?$//;
				if ($link eq '') {
					$linkname = "ERROR: LDP namespace resolution failure on $linkname";
				}
				$line =~ s/\[\[.*?\]\]/<ulink url='$link'><citetitle>$linkname<\/citetitle><\/ulink>/;
			}
		} elsif ($link =~ /^file:/) {
			$linkname =~ s/^file://;
			$line =~ s/\[\[.*?\]\]/<filename>$linkname<\/filename>/;
		} elsif ($link =~ /^dir:/) {

# FIXME: need to check attribute on filename element
# 
			$linkname =~ s/^dir://;
			$line =~ s/\[\[.*?\]\]/<filename type='directory'>$linkname<\/filename>/;
		} else {
			$line =~ s/\[\[.*?\]\]/<filename>$linkname<\/filename>/;
		}
	}

	# emphasis
	#
	while ($line =~ /'''.*'''/) {
		$line =~ s/'''/<emphasis role='bold'>/;
		$line =~ s/'''/<\/emphasis>/;
	}

	# this block defines DocBook structures that won't be broken up with 
	# paragraphs when we hit empty lines:
	#
	#	<para>
	#	<sect1>
	#	<sect2>
	#	<sect3>
	#	<programlisting>
	#	<literallayout>
	
	# forget about being in nopara state if we're no longer in one
	# 
	if ($noparadepth == 0) {
		$noparatag = "";
	}
		
	# start a new nopara section
	#
	if ((($line =~ /^<para>/) or
	     ($line =~ /^<sect/) or
	     ($line =~ /^<screen>/) or
	     ($line =~ /^<screen>/) or
	     ($line =~ /^<blockquote>/) or
	     ($line =~ /^<literallayout>/) or
	     ($line =~ /^<articleinfo>/) or
	     ($line =~ /^<programlisting>/)) and
	    ($noparadepth == 0)) { 
	    	&closepara;
		$noparatag = $line;
		$noparatag =~ s/^.*?<//;
		$noparatag =~ s/>.*?$//;
		$noparaline = $linenumber;

		# screen sections don't embed para tags, but are wrapped in them
		#
		if ($line =~ /^<screen>/) {
			unless ($para) {
				$buf .= "<para>";
				$para = 1;
			}
		}
	}

	# count noparadepth
	#
	if ($noparatag ne '') {
		$temp = $line;
		while ($temp =~ /<$noparatag>/) {
			$temp =~ s/<?$noparatag>//;
			$noparadepth ++;
		}
		while ($temp =~ /<\/$noparatag>/) {
			$temp =~ s/<?\/$noparatag>//;
			$noparadepth --;
			if ($noparadepth == 0) {
				$noparaline = 0;
			}
		}

		# runon protection
		#
		if (($noparaline) and ($linenumber >= ($noparaline + 100))) {
			$buf .= "ERROR: runon block starting on line $noparaline\n";
			return;
		}

		# recover original line -- no whitespace modifiers
		# allow nonencoded text in unparsed lines, when in a literal block
		#
		$line = $originalline;
		chomp($line);
		if ($line =~ /^<$noparatag>/ ) {
			$starttag = "<$noparatag>";
		} else {
			$starttag = '';
		}
		if ($line =~ /<\/$noparatag>/ ) {
			$endtag = "<\/$noparatag>";
		} else {
			$endtag = '';
		}

		$line =~ s/<$noparatag>//;
		$line =~ s/<\/$noparatag>//;
	    if (($noparatag eq 'screen') or
	        ($noparatag eq 'literallayout') or
	        ($noparatag eq 'programlisting')) {
    		encode_entities($line);
        }
		$line = "$starttag$line$endtag";

	# sect3
	#
	} elsif ($line =~ /^===/) {
		&close3;
		&splittitle;
		if ($id eq '') {
			$line = "<sect3><title>$title</title>";
		} else {
			$line = "<sect3 id='$id'><title id='$id-title'>$title</title>";
		}
		$level3 = 1;

	# sect2
	#
	} elsif ($line =~ /^==/) {
		&close2;
		&splittitle;
		if ($id eq '') {
			$line = "<sect2><title>$title</title>";
		} else {
			$line = "<sect2 id='$id'><title id='$id-title'>$title</title>";
		}
		$level2 = 1;

	# sect1
	#
	} elsif ($line =~ /^=/) {
		&close1;
		&splittitle;
		if ($id eq '') {
			$line = "<sect1><title>$title</title>";
		} else {
			$line = "<sect1 id='$id'><title id='$id-title'>$title</title>";
		}
		$level1 = 1;

	# orderedlist
	#
	} elsif ($line =~ /^#/) {
		&closeitemizedlist;
		if ($orderedlist == 0) {
			$buf .= "<orderedlist>\n";
			$orderedlist = 1;
		}
		&closelistitem;
		$line =~ s/^#//;
		&trimline;
		$line =~ s/^/<listitem><para>/;
		$listitem = 1;
		$para = 1;
	} elsif ($line =~ /^\/#/) {
		$line =~ s/^\/#//;
		&trimline;
		&closeorderedlist;

	# itemizedlist
	#
	} elsif ($line =~ /^\*/) {
		&closeorderedlist;
		if ($itemizedlist == 0) {
			$buf .= "<itemizedlist>\n";
			$itemizedlist = 1;
		}
		&closelistitem;
		$line =~ s/^\*//;
		&trimline;
		$line =~ s/^/<listitem><para>/;
		$listitem = 1;
		$para = 1;
	} elsif ($line =~ /\/\*/) {
		$line =~ s/^\/\*//;
		&trimline;
		&closeitemizedlist;

	# question
	#
	} elsif ($line =~ /^Q:/) {
		&closelists;
		&closeqandaentry;
		$line =~ s/^Q://;
		&trimline;
		&splittitle;
		if ($id eq '') {
			$line = "<question><para>$title</para></question>";
		} else {
			$line = "<question id='$id'><para>$title</para></question>";
		}
		unless ($qandaentry) {
			$line = "<qandaentry>\n" . $line;
			$qandaentry = 1;
		}
		if ($qandaset == 0) {
			$line = "<qandaset defaultlabel='qanda'>\n". $line;
			$qandaset = 1;
		}

	# answer
	#
	} elsif ($line =~ /^A:/) {
		$line =~ s/^A://;
		&trimline;
		&closeanswer;
		$line = "<answer><para>" . $line;
		$answer = 1;
		$para = 1;

	} elsif ($line =~ /^\s*----\s*$/) {
		$line = '';

	# para
	#
	} else {
		if (($para == 0) and ($noparatag eq '')) {
			$line = "<para>" . $line;
			$para = 1;
		} else {
			$line .= " ";
		}
	}

	$buf .= "$line\n";
}

sub ProcessEnd {
	# close nesting
	#
	&close1;

	if ($noparadepth > 0) {
		$buf .= "ERROR tag $noparatag on line $noparaline unterminated.\n";
	}
}

sub Buffer {
	return $buf;
}

sub close1 {
	&close2;
	if ($level1) {
		$buf .= "</sect1>\n";
		$level1 = 0;
	}
}

sub close2 {
	&close3;
	if ($level2) {
		$buf .= "</sect2>\n";
		$level2 = 0;
	}
}

sub close3 {
	&closeorderedlist;
	&closeitemizedlist;
	&closepara;
	&closeqandaset;
	if ($level3) {
		$buf .= "</sect3>\n";
		$level3 = 0;
	}
}

sub closenonsect {
	&closepara;
#	&closeorderedlist;
#	&closeitemizedlist;
}

sub closelistitem {
	&closepara;
	if ($listitem) {
		$buf .= "</listitem>\n";
		$listitem = 0;
	}
}

sub closeorderedlist {
	&closepara;
	&closelistitem;
	if ($orderedlist) {
		$buf .= "</orderedlist>\n";
		$orderedlist = 0;
	}
}

sub closeitemizedlist {
	&closepara;
	&closelistitem;
	if ($itemizedlist) {
		$buf .= "</itemizedlist>\n";
		$itemizedlist = 0;
	}
}

sub closelists {
	&closeitemizedlist;
	&closeorderedlist;
}

sub closeanswer {
	&closepara;
	if ($answer) {
		$buf .= "</answer>\n";
		$answer = 0;
	}
}

sub closeqandaentry {
	&closeanswer;
	if ($qandaentry) {
		$buf .= "</qandaentry>\n";
		$qandaentry = 0;
	}
}

sub closeqandaset {
	&closeqandaentry;
	if ($qandaset) {
		$buf .= "</qandaset>\n";
		$qandaset = 0;
	}
}

sub closepara {
	if ($para) {
		$buf .= "</para>\n";
		$para = 0;
	}
}

sub trimline {
	$line =~ s/\s+$//;
	$line =~ s/^\s+//;
}

sub splittitle {
	$line =~ s/^=+//;
	$line =~ s/=+$//;
	$title = $line;
	if ($line =~ /\|/) {
		$title =~ s/\|.+//;
		$id = $line;
		$id =~ s/^.+\|//;
	} else {
		$id = &anchorfix($title);
	}
	$title =~ s/\s+$//;
	$title =~ s/^\s+//;
	$id =~ s/\s+$//;
	$id =~ s/^\s+//;
}

sub anchorfix {
	my $anchor = $_[0];
	$anchor = lc(&trim($anchor));
	$anchor = decode_entities($anchor);
	$anchor =~ s/-/-dash-/g;
	$anchor =~ s/&/-and-/g;
	$anchor =~ s/;//g;
	$anchor = encode_entities($anchor);
	$anchor =~ s/&(\w)grave/\1/g;
	$anchor =~ s/&(\w)acute/\1/g;
	$anchor =~ s/&(\w)circ/\1/g;
	$anchor =~ s/&(\w)uml/\1/g;
	$anchor =~ s/&(\w)tilde/\1/g;
	$anchor =~ s/&(\w)cedil/\1/g;
	$anchor =~ s/&/-and-/g;
	$anchor =~ s/;//g;
	$anchor =~ s/\//-slash-/g;
	$anchor =~ s/\\/-bslash-/g;
	$anchor =~ s/\s+/-/g;
	$anchor =~ s/'//g;
	$anchor =~ s/`//g;
	$anchor =~ s/,/-comma-/g;
	$anchor =~ s/\./-dot-/g;
	$anchor =~ s/!/-bang-/g;
	$anchor =~ s/\?/-question-/g;
	$anchor =~ s/\+/-plus-/g;
	$anchor =~ s/\*/-x-/g;
	$anchor =~ s/\(/-op-/g;
	$anchor =~ s/\)/-cp-/g;
	$anchor =~ s/\@/-at-/g;
	$anchor =~ s/dcm_at/-at-/gi;
	$anchor =~ s/\^/-hat-/g;
	$anchor =~ s/=/-eq-/g;
	$anchor =~ s/\$/S/;
	$anchor =~ s/~/-tilde-/g;
	$anchor =~ s/0/-zero-/g;
	$anchor =~ s/1/-one-/g;
	$anchor =~ s/2/-two-/g;
	$anchor =~ s/3/-three-/g;
	$anchor =~ s/4/-four-/g;
	$anchor =~ s/5/-five-/g;
	$anchor =~ s/6/-six-/g;
	$anchor =~ s/7/-seven-/g;
	$anchor =~ s/8/-eight-/g;
	$anchor =~ s/9/-nine-/g;
	$anchor =~ s/\|/-pipe-/g;
	$anchor =~ s/\[/-lsqb-/g;
	$anchor =~ s/\]/-rsqb-/g;
	$anchor =~ s/^-+//;
	$anchor =~ s/-+$//;
	$anchor =~ s/--/-/g;	# get rid of double, initial and trailing hyphens
	return &trim($anchor);
}

sub trim {
	my $temp = $_[0];

	$temp =~ s/^\s+//g;
	$temp =~ s/\s+$//g;
	return $temp;
}
1;
