#!/usr/bin/perl

$editcols = 80;
$editrows = 25;

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;
$section_max	= 25;

# Read parameters
$doc_id		= param('doc_id');
$notes          = param('notes');
$revision	= param('revision');

$logfile = '/tmp/ldp.log';
open (LOG, "> $logfile");
print LOG "document_wiki opened by $username.\n";


$section = 0;
while ($section <= $section_max) {
	$section++;
	$wiki_section = param("wiki$section");
	if ($wiki_section) {
#		if ($wiki) {
#			$wiki .= "\n";
#		}
		$wiki .= $wiki_section;
	}
}
$section = 0;

$save		= param('Save');
$preview	= param('Preview');
$docbook	= param('DocBook');
$splitup	= param('SplitUp');

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
if ($username ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		$maintainer_id = $row[2];
		$result=$conn->exec("SELECT count(*) FROM document_maintainer WHERE maintainer_id=$maintainer_id AND doc_id=$doc_id AND active='t'");
		@row = $result->fetchrow;
		unless ($row[0]) {
			print $query->redirect("../wrongpermission.html");
			exit;
		}
	}
}

print LOG "Opening document_wiki by $username.\n";

if ($save) {
	print LOG "Saving document_wiki by $username.\n";
	while ($wiki =~ /\\/) {
		$wiki =~ s/\\/a1s2d3f4/;
	}
	while ($wiki =~ /a1s2d3f4/) {
	        $wiki =~ s/a1s2d3f4/\\\\/;
	}
	while ($wiki =~ /&/) {
		$wiki =~ s/&/a1s2d3f4/;
	}
	while ($wiki =~ /a1s2d3f4/) {
	        $wiki =~ s/a1s2d3f4/&amp;/;
	}
	while ($wiki =~ /\'/) {
		$wiki =~ s/\'/a1s2d3f4/;
	}
	while ($wiki =~ /a1s2d3f4/) {
	        $wiki =~ s/a1s2d3f4/\'\'/;
	}
	while ($notes =~ /\'/) {
	        $notes =~ s/\'/a1s2d3f4/;
	}
	while ($notes =~ /a1s2d3f4/) {
	        $notes =~ s/a1s2d3f4/\'\'/;
	}

	#find out how many prior revisions there were
	$result = $conn->exec("SELECT count(*) FROM document_wiki WHERE doc_id = $doc_id");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
	@row = $result->fetchrow;
	$revisions = $row[0];

#	&printheader;
#	print $wiki;
#	print end_html;
#	exit;

	if ($revisions >= $revision ) {
		&printheader;
		print "<p>Edit conflict!\n";
		print "<p>You were editing version $revisions, but trying to save to version $revision\n";
		print end_html;
	} elsif ($wiki eq '') {
		&printheader;
		print "<p>No content to save!\n";
		print end_html;
	} else {
		$revision = $revisions + 1;
		$sql = "INSERT INTO document_wiki(doc_id, revision, date_entered, wiki, notes, username) VALUES ($doc_id, $revision, now(), '$wiki', '$notes', '$username')";
		$result=$conn->exec($sql);
		print $query->redirect("document_edit.pl?doc_id=$doc_id");
	}
	exit;
}

#load document meta-data
$result = $conn->exec("SELECT title, filename, class FROM document WHERE doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$title		= $row[0];
$title		=~  s/\s+$//;
$filename	= $row[1];
$class		= $row[2];
$class		=~  s/\s+$//;

#find out how many prior revisions there were
$result = $conn->exec("SELECT count(*) FROM document_wiki WHERE doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$revisions = $row[0];

#if we're not previewing, load data from database and determine version
unless (($preview) or ($docbook)) {
	$result = $conn->exec("SELECT wiki FROM document_wiki WHERE doc_id = $doc_id ORDER BY revision DESC LIMIT 1, 0");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
	@row = $result->fetchrow;
	$revision	= $revisions + 1;
	$wiki		= $row[0];
	$wiki		=~  s/\s+$//;
	while ($wiki =~ /</) {
		$wiki =~ s/</&lt;/;
	}
	while ($wiki =~ />/) {
		$wiki =~ s/>/&gt;/;
	}

	&printheader;

	print "<form method=POST action='document_wiki.pl' name='edit'>\n";
	print "<input type=hidden name=doc_id value='$doc_id'>\n";
	print "<input type=hidden name=revision value=$revision>\n";
	print "<input type=submit value='Separate Sections' name=SplitUp>\n";
	print "<input type=submit value='One Section' name=Combine>\n";
	print "<input type=submit value=Save name=Save>\n";
	print "<input type=submit value=Preview name=Preview>\n";
	print "<input type=submit value=DocBook name=DocBook>\n";
	print "<table width='100%'>\n";
	print "<tr><th>Document Text</th></tr>\n";


	$tempfile = "/tmp/document_wiki" . rand();
	open (TMP, "> $tempfile");
	print TMP $wiki;
	close(TMP);

	open (TMP, $tempfile);
	$wiki = "";
	$section = 0;
	while ($line = <TMP>) {
		if ($splitup) {
			if ($line =~ /^===/) {
			} elsif ($line =~ /^==/) {
			} elsif ($line =~ /^=/) {
				&printwiki;
			}
		}
		$wiki .= $line;
	}
	close TMP;
	unlink $tempfile;
	&printwiki;
	print "<tr><td>Comments: <input type=text name=notes size=$editcols style='width:100%' wrap></input></td></tr>\n";
	if ($revisions == 0) {
		print "<tr><td>There are no previous versions of this document. Your changes will be saved as version $revision</td></tr>\n";
	} else {
		print "<tr><td>You are editing version $revisions. Your changes will be saved as version $revision</td></tr>\n";
	}
	print "</table>\n";
	print "</form>\n";
	print end_html;
}

if ($preview or $docbook) {
	$txtfile = "/tmp/" . rand() . ".txt";
	$sgmlfile = $txtfile;
	$sgmlfile =~ s/\.txt/\.sgml/;
	$htmlfile = $txtfile;
	$htmlfile =~ s/\.txt/\.html/;
	$abstractfile = $txtfile;
	$abstractfile =~ s/\./abs\./;
	$abstractsgmlfile = $sgmlfile;
	$abstractsgmlfile =~ s/\./abs\./;

	open(TXT, "> $txtfile");
	print TXT $wiki;
	close(TXT);

	$cmd = "/usr/local/bin/wt2db -o $sgmlfile $txtfile";
	system($cmd);
	
	print LOG "Wrote wt file to $txtfile for document $doc_id by $username.\n";
	
	$sgml  = '<!DOCTYPE ARTICLE PUBLIC "-//OASIS//DTD DocBook V4.1//EN">' . "\n";
	if ($class eq 'FAQ') {
		$sgml .= "<article class='FAQ'>\n";
	} else {
		$sgml .= "<article>\n";
	}
	$sgml .= "<articleinfo>\n";
	
	$result = $conn->exec("SELECT title, last_update, abstract FROM document WHERE doc_id = $doc_id");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
	while (@row = $result->fetchrow) {
		$title = $row[0];
		$date  = $row[1];

		#insert paragraphs in the abstract where appropriate.
		$abstract = $row[2];
		open(ABSTRACT, "> $abstractfile");
		print ABSTRACT $abstract;
		close(ABSTRACT);
		
		$cmd = "/usr/local/bin/wt2db -o $abstractsgmlfile $abstractfile";
		system($cmd);

		$abstract = "";
		open(ABSTRACTSGML, $abstractsgmlfile);
		while (<ABSTRACTSGML>) {
			$abstract .= $_;
		}

		#build the document header.
		$sgml .= "<title>$title</title>\n";
		$sgml .= "<date>$date</date>\n";
		$sgml .= "<pubdate>$date</pubdate>\n";
		$sgml .= "<abstract>$abstract</abstract>\n";
	}
	
	$result = $conn->exec("SELECT m.maintainer_name, dm.email FROM document_maintainer dm, maintainer m WHERE doc_id = $doc_id AND dm.maintainer_id = m.maintainer_id AND active='t'");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
	while (@row = $result->fetchrow) {
		$name  = $row[0];
		$email = $row[1];
		$sgml .= "<author>\n";
		$sgml .= "<affiliation>\n";
		$sgml .= "<address>\n";
		$sgml .= "<firstname>$name</firstname>\n";
		$sgml .= "</address>\n";
		$sgml .= "</affiliation>\n";
		$sgml .= "</author>\n";
	}	
	
	$sgml .= "</articleinfo>\n";
	
	print LOG "Opening sgml file $sgmlfile for document $doc_id by $username.\n";
	
	$sgmlfileline = 0;
	open(SGML, $sgmlfile);
	while (<SGML>) {
		print LOG ".";
		$line = $_;
		$sgml .= $line;
		$sgmlfileline++;
		while ($line =~ /</) {
			$line =~ s/</&lt;/;
		}
		while ($line =~ />/) {
			$line =~ s/>/&gt;/;
		}
		$buf .= "<br>$line";
	}
	close(SGML);
	print LOG "\n";

	print LOG "Read $sgmlfileline lines from $sgmlfile for document $doc_id by $username.\n";
	
	$sgml .= "</article>\n";

	open(SGML, "> $sgmlfile");
	print SGML $sgml;
	close(SGML);
	
	print LOG "Wrote composite sgml file $sgmlfile for document $doc_id by $username.\n";
	
}

if ($docbook) {
#	&printheader;
#	print "<p><hr>\n";
#	print "<pre>\n";

	print "Content-Type: text/plain; charset=ISO-8859-1\n\n";

#	while ($sgml =~ /</) {
#		$sgml =~ s/</&lt;/;
#	}
#	while ($sgml =~ />/) {
#		$sgml =~ s/>/&gt;/;
#	}
	print $sgml;
#	print "</pre>\n";
#	print "</html>\n";
}

if ($preview) {
	
	print LOG "Previewing $sgmlfile for document $doc_id by $username.\n";

	print LOG "Running xsltproc on $sgmlfile, into $htmlfile.\n";
	
	$cmd = "xsltproc --docbook /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl $sgmlfile > $htmlfile";
	system($cmd);

	print header(-expires=>'now');
	open(HTML, "$htmlfile");
	$i = 0;
	while (<HTML>) {
		$line = $_;
		$i += 1;
		print $line;
	}
	close(HTML);
	
	print LOG "HTML display of $htmlfile complete.\n";
	

}

sub printheader {
	print header(-expires=>'now');
	print "<html><head><title>$title Wiki</title>";
	print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
	print "</head>";
	print "<body>";

	print "<h1>$title Wiki</h1>\n";

	system("./navbar.pl");
	print "<a href='/help/wiki.html'>Page Help</a>";

	print "<p>";
	print "<a href='document_edit.pl?doc_id=$doc_id'>Meta-Data</a>\n";
	print "&nbsp;|&nbsp;";
	print "<a href='document_wiki_list.pl?doc_id=$doc_id'>Version History</a>\n";
}

sub printwiki {
	if (($wiki) or ($section == 0)) {
		$section++;
		print "<tr><td align='center'>Section $section</td></tr>\n";
		print "<tr><td><textarea name=wiki$section rows=$editrows cols=$editcols style='width:100%' wrap>$wiki</textarea></td></tr>\n";
		if ($section == $section_max) {
			print "Aborting due to loop control.\n";
			last;
		}
		$wiki = "";
	}
}


