#! /usr/bin/perl

$workpath = "/tmp";
$editcols = 80;
$editrows = 25;

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$doc_id		= param('doc_id');
$wiki           = param('wiki');
$notes          = param('notes');
$revision	= param('revision');

$save		= param('Save');
$preview	= param('Preview');
$docbook	= param('DocBook');

$username       = $query->remote_user();

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
if ($username ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if (($row[1] ne 't') and ($row[2] != $doc_id)) {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}

if ($save) {
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

	if ($revisions >= $revision ) {
		&printheader;
		print "<p>Edit conflict!\n";
		print "<p>You were editing version $revisions, but trying to save to version $revision\n";
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
unless ($preview or $docbook) {
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
	print "<table width='100%'>\n";
	print "<tr><th>Document Text</th></tr>\n";
	print "<tr><td><textarea name=wiki rows=$editrows cols=$editcols style='width:100%' wrap>$wiki</textarea></td></tr>\n";
	print "<tr><td>Comments: <input type=text name=notes size=$editcols></input></td></tr>\n";
	if ($revisions == 0) {
		print "<tr><td>There are no previous versions of this document. Your changes will be saved as version $revision</td></tr>\n";
	} else {
		print "<tr><td>You are editing version $revisions. Your changes will be saved as version $revision</td></tr>\n";
	}
	print "</table>\n";
	print "<input type=submit value=Save name=Save>\n";
	print "<input type=submit value=Preview name=Preview>\n";
	print "<input type=submit value=DocBook name=DocBook>\n";
	print "</form>\n";
	print end_html;
}

if ($preview or $docbook) {
	$txtfile = "$workpath/" . rand . ".txt";
	$sgmlfile = $txtfile;
	$sgmlfile =~ s/\.txt/\.sgml/;
	$htmlfile = $txtfile;
	$htmlfile =~ s/\.txt/\.html/;
	$abstractfile = $txtfile;
	$abstractfile =~ s/\./abs\./;
	$abstractsgmlfile = $sgmlfile;
	$abstractsgmlfile =~ s/\./abs\./;
	system("rm $sgmlfile");

	open(TXT, "> $txtfile");
	print TXT $wiki;
	close(TXT);

	$cmd = "/usr/lib/cgi-bin/gldp.org/txt2db.pl -o $sgmlfile $txtfile";
	system($cmd);

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
		
		$cmd = "/usr/lib/cgi-bin/gldp.org/txt2db.pl -o $abstractsgmlfile $abstractfile";
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
	
	open(SGML, $sgmlfile);
	while (<SGML>) {
		$line = $_;
		$sgml .= $line;
		while ($line =~ /</) {
			$line =~ s/</&lt;/;
		}
		while ($line =~ />/) {
			$line =~ s/>/&gt;/;
		}
		$buf .= "<br>$line";
	}
	close(SGML);

	$sgml .= "</article>\n";

	open(SGML, "> $sgmlfile");
	print SGML $sgml;
	close(SGML);
}

if ($docbook) {
	&printheader;
	print "<p><hr>\n";
	print "<pre>\n";
	while ($sgml =~ /\</) {
		$sgml =~ s/\</&lt;/;
	}
	while ($sgml =~ /\>/) {
		$sgml =~ s/\>/&gt;/;
	}
	print $sgml;
	print "</pre>\n";
	print "</html>\n";
}

if ($preview) {
	$cmd = "xsltproc --docbook /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl $sgmlfile > $htmlfile";
	system($cmd);

	print header(-expires=>'now');
	open(HTML, "$htmlfile");
	$i = 0;
	while (<HTML>) {
		$line = $_;
		$i += 1;
#		if ($i > 8) {
	  		print $line;
#		}
	}
	close(HTML);

}

sub printheader {
	print header(-expires=>'now');
	print "<html><head><title>$title Wiki</title>";
	print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
	print "</head>";
	print "<body>";

	print "<h1>$title Wiki</h1>\n";

	print "<p><a href='/index.html'>Index</a>&nbsp;|&nbsp;";
	print "<a href='/cgi-bin/document_list.pl'>Documents</a>&nbsp;|&nbsp;";
	print "<a href='/cgi-bin/topic_list.pl'>Topics</a>&nbsp;|&nbsp;";
	print "<a href='/cgi-bin/maintainer_list.pl'>Maintainers</a>&nbsp;|&nbsp;";
	print "<a href='/cgi-bin/editor_list.pl'>Editors</a>&nbsp;|&nbsp;";
	print "<a href='/cgi-bin/ldp_stats.pl'>Statistics</a>&nbsp;|&nbsp;";
	print "<a href='/help/'>Help</a>&nbsp;|&nbsp;";
	print "<a href='/help/wiki.html'>Page Help</a>";

	print "<p>";
	print "<a href='document_edit.pl?doc_id=$doc_id'>Meta-Data</a>\n";
	print "&nbsp;|&nbsp;";
	print "<a href='document_wiki_list.pl?doc_id=$doc_id'>Version History</a>\n";
}
