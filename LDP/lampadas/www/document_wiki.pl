#!/usr/bin/perl

$editrows = 25;

use Lampadas;
use Lampadas::Database;
use Wt2Db;

$L = new Lampadas;
$DB = new Lampadas::Database;
$WT = new Wt2Db;

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
		exit;
	}
}

# Read $L->Parameters
$doc_id		= $L->Param('doc_id');
$notes          = $L->Param('notes');
$revision	= $L->Param('revision');
$wiki		= $L->Param('wiki');

$save		= $L->Param('Save');
$preview	= $L->Param('Preview');
$docbook	= $L->Param('DocBook');

if ($save) {
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
	$revisions = $DB->Value("SELECT COUNT(*) FROM document_wiki WHERE doc_id=$doc_id");

	if ($revisions >= $revision ) {
		&printheader;
		print "<p>Edit conflict!\n";
		print "<p>You were editing version $revisions, but trying to save to version $revision\n";
		$L->EndPage();
	} elsif ($wiki eq '') {
		&printheader;
		print "<p>No content to save!\n";
		$L->EndPage();
	} else {
		$revision = $revisions + 1;
		$sql = "INSERT INTO document_wiki(doc_id, revision, date_entered, wiki, notes, user_id) VALUES ($doc_id, $revision, now(), '$wiki', '$notes', " . $L->CurrentUserID() . ")";
		$DB->Exec($sql);
		$L->Redirect("document_edit.pl?doc_id=$doc_id");
	}
	exit;
}

#load document meta-data
$result = $DB->Recordset("SELECT title, filename, class FROM document WHERE doc_id=$doc_id");
@row = $result->fetchrow;
$title		= $row[0];
$title		=~  s/\s+$//;
$filename	= $row[1];
$class		= $row[2];
$class		=~  s/\s+$//;

#find out how many prior revisions there were
$revisions = $DB->Value("SELECT count(*) FROM document_wiki WHERE doc_id = $doc_id");

if ($preview or $docbook) {
	$sgml  = '<!DOCTYPE ARTICLE PUBLIC "-//OASIS//DTD DocBook V4.1//EN">' . "\n";
	if ($class eq 'FAQ') {
		$sgml .= "<article class='FAQ'>\n";
	} else {
		$sgml .= "<article>\n";
	}
	$sgml .= "<articleinfo>\n";

	%doc = $L->Doc($doc_id);
	%docusers = $L->DocUsers($doc_id);
	
	$WT->Reset();
	foreach $line (split /\n/, $doc{abstract}) {
		$WT->ProcessLine($line);
	}
	$WT->ProcessEnd();
	$abstract .= $WT->Buffer();
	$WT->Reset();

	#build the document header.
	$sgml .= "<title>$doc{title}</title>\n";
	$sgml .= "<date>$doc{pub_date}</date>\n";
	$sgml .= "<pubdate>$doc{pub_date}</pubdate>\n";
	$sgml .= "<abstract>$abstract</abstract>\n";
	
	foreach $key (keys %docusers) {
		$sgml .= "<author>\n";
		$sgml .= "<affiliation>\n";
		$sgml .= "<address>\n";
		$sgml .= "<firstname>$docusers{$key}{first_name}</firstname>\n";
		$sgml .= "<othername>$docusers{$key}{middle_name}</othername>\n";
		$sgml .= "<surname>$docusers{$key}{surname}</surname>\n";
		$sgml .= "<email>$docusers{$key}{email}</email>\n";
		$sgml .= "</address>\n";
		$sgml .= "</affiliation>\n";
		$sgml .= "</author>\n";
	}	
	
	$sgml .= "</articleinfo>\n";

	$WT->Reset();
	foreach $line (split /\n/, $wiki) {
		$WT->ProcessLine($line);
	}
	$WT->ProcessEnd();
	$sgml .= $WT->Buffer();
	$WT->Reset();

	$sgml .= "</article>\n";

} else {
	# If we're not previewing, load data from database and determine version
	# 
	$result = $DB->Recordset("SELECT wiki FROM document_wiki WHERE doc_id = $doc_id ORDER BY revision DESC LIMIT 1, 0");
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
	print "<input type=submit value=Save name=Save>\n";
	print "<input type=submit value=Preview name=Preview>\n";
	print "<input type=submit value=DocBook name=DocBook>\n";
	print "<table width='100%'>\n";
	print "<tr><th>Document Text</th></tr>\n";

	&printwiki;
	print "<tr><td>Comments: <input type=text name=notes style='width:100%' wrap></input></td></tr>\n";
	if ($revisions == 0) {
		print "<tr><td>There are no previous versions of this document. Your changes will be saved as version $revision</td></tr>\n";
	} else {
		print "<tr><td>You are editing version $revisions. Your changes will be saved as version $revision</td></tr>\n";
	}
	print "</table>\n";
	print "</form>\n";
	$L->EndPage();
}

if ($docbook) {
	print "Content-Type: text/plain; charset=ISO-8859-1\n\n";
	print $sgml;
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
		print $line;
	}
	close(HTML);
}

sub printheader {
	$L->StartPage("$title Wiki");

	print "<p>";
	print "<a href='document_edit.pl?doc_id=$doc_id'>Meta-Data</a>\n";
	print "&nbsp;|&nbsp;";
	print "<a href='document_wiki_list.pl?doc_id=$doc_id'>Version History</a>\n";
}

sub printwiki {
	if ($wiki) {
		print "<tr><td><textarea name=wiki rows=$editrows style='width:100%' wrap>$wiki</textarea></td></tr>\n";
	}
}


