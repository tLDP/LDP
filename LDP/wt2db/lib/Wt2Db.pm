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

# These keep track of which constructs we're in the middle of
#
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


# -----------------------------------------------------------

sub new {
	my $that = shift;
	my $class = ref($that) || $that;
	my $self = {};
	bless $self, $class;
	return $self;
}

sub ProcessFile {
	($self, $txtfile, $dbfile, $verbose, $article) = @_;

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
	if ($article) {
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
	if ($article) {
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
	# ulink
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

		# kill quotes, they mess us up
		# 
		$link =~ s/'/%27/g;

		# namespaces are handled differently
		#
		print "$link\n" if ($verbose);
		if ($link =~ /^http:/) {
			$line =~ s/\[\[.*?\]\]/<ulink url='$link'><citetitle>$linkname<\/citetitle><\/ulink>/;
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
			$tempfile = "/tmp/wt2db-" . $rand;
			$cmd = "wget -q http://db.linuxdoc.org/cgi-pub/ldp-xml.pl?name=$link -O $tempfile";
			system("$cmd");
			open(URL, "$tempfile") || die "wt2db: cannot open temporary file ($!)\n\n";
			$link = "";
			while ($url_line = <URL>) {
				$url_line =~ s/\n//;
				if ($url_line =~ /identifier/) {
					$link .= $url_line;
				}
			}
			close(URL);
			unlink $tempfile;
			$link =~ s/^.*?<identifier>//;
			$link =~ s/<\/identifier>.*?$//;
			if ($link eq '') {
				$linkname = "ERROR: LDP namespace resolution failure on $linkname";
			}
			$line =~ s/\[\[.*?\]\]/<ulink url='$link'><citetitle>$linkname<\/citetitle><\/ulink>/;
		} elsif ($link =~ /^file:/) {
			$linkname =~ s/^file://;
			$line =~ s/\[\[.*?\]\]/<filename>$linkname<\/filename>/;
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
	
	# forget about nopara
	if ($noparadepth == 0) {
		$noparatag = "";
	}
		
	# start a new nopara section
	#
	if ((($line =~ /^<para>/) or
	     ($line =~ /^<sect/) or
	     ($line =~ /^<screen>/) or
	     ($line =~ /^<literallayout>/) or
	     ($line =~ /^<articleinfo>/) or
	     ($line =~ /^<programlisting>/)) and
	    ($noparadepth == 0)) { 
	    	&closepara;
		$noparatag = $line;
		$noparatag =~ s/^.*?<//;
		$noparatag =~ s/>.*?$//;
		$noparaline = $linenumber;
		if ($line =~ /^<screen>/) {
			unless ($para) {
				$line = "<para>" . $line;
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
		#
		$line = $originalline;
		chomp($line);

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
			$line = "<question><para>" . $title . "</para></question>";
		} else {
			$line = "<question id='$id'><para>" . $title . "</para></question>";
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

# Basically a cut-and-paste of the original declarations,
# to make sure all variables are completely cleared.
#
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
	$id = "";
	if ($line =~ /\|/) {
		$title =~ s/\|.+//;
		$id = $line;
		$id =~ s/^.+\|//;
	}
	$title =~ s/\s+$//;
	$title =~ s/^\s+//;
	$id =~ s/\s+$//;
	$id =~ s/^\s+//;
}
1;
