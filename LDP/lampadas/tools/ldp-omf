#!/usr/bin/perl

use CGI qw(:standard);
use Pg;
use Time::localtime;

$dbmain='ldp';
@row;
$count = 0;
$query = new CGI;

# Connect and load the tuples
$conn=Pg::connectdb("dbname=$dbmain");
$sql = "SELECT doc_id, title, pub_status_name, class, format, tickle_date, dtd, lr.review_status_name, tr.review_status_name as tech_review_status_name, url, pub_date, last_update, maintained, license, version, abstract FROM document, pub_status, review_status lr, review_status tr WHERE document.pub_status=pub_status.pub_status AND document.review_status = lr.review_status and document.tech_review_status = tr.review_status and document.pub_status='N' ORDER BY doc_id";

$doc=$conn->exec("$sql");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $doc->resultStatus;

print '<?xml version="1.0" encoding="iso-8859-1"?>' . "\n";
print '<omf>' . "\n";
while (@row = $doc->fetchrow) {
	$doc_id                  = $row[0];
	$title                   = $row[1];
	$title                   =~ s/\&/\&amp;/;
	$pub_status_name         = $row[2];
	$class                   = $row[3];
	$class                   =~ s/\s+$//;
	$format                  = $row[4];
	$tickle_date             = $row[5];
	$dtd                     = $row[6];
	$dtd                     =~ s/\s+$//;
	$review_status_name      = $row[7];
	$tech_review_status_name = $row[8];
	$url                     = $row[9];
	$pub_date                = $row[10];
	$last_update             = $row[11];
	$maintained              = $row[12];
	$maintained              =~ s/f/No/;
	$maintained              =~ s/t/Yes/;
	$license                 = $row[13];
	$license                 =~ s/\s+$//;
	$version                 = $row[14];
	$version                 =~ s/\s+$//;
	$abstract                = $row[15];
	$abstract                =~ s/\s+$//;
	$abstract                =~ s/\&/\&amp;/;

	print "<resource id='$doc_id'>\n";

	#CREATOR
	$sql = "SELECT maintainer_name, document_maintainer.email FROM document, document_maintainer, maintainer WHERE document.doc_id = document_maintainer.doc_id AND document_maintainer.maintainer_id = maintainer.maintainer_id AND role='Author' AND document.doc_id = $doc_id";
	$maintainer=$conn->exec("$sql");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $maintainer->resultStatus;
	while (@maintainer_row = $maintainer->fetchrow) {
		$maintainer_name = $maintainer_row[0];
		$maintainer_name =~ s/\&/\&amp;/;
		$maintainer_email = $maintainer_row[1];
		print "  <creator>$maintainer_email ($maintainer_name)</creator>\n";
	}
  
	#MAINTAINER
	$sql = "SELECT maintainer_name, document_maintainer.email FROM document, document_maintainer, maintainer WHERE document.doc_id = document_maintainer.doc_id AND document_maintainer.maintainer_id = maintainer.maintainer_id AND role='Maintainer' AND document.doc_id = $doc_id";
	$maintainer=$conn->exec("$sql");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $maintainer->resultStatus;
	while (@maintainer_row = $maintainer->fetchrow) {
		$maintainer_name = $maintainer_row[0];
		$maintainer_name =~ s/\&/\&amp;/;
		$maintainer_email = $maintainer_row[1];
		print "  <maintainer>$maintainer_email ($maintainer_name)</maintainer>\n";
	}
  
	#CONTRIBUTOR
	$sql = "SELECT maintainer_name, document_maintainer.email FROM document, document_maintainer, maintainer WHERE document.doc_id = document_maintainer.doc_id AND document_maintainer.maintainer_id = maintainer.maintainer_id AND role<>'Author' AND role<>'Maintainer' AND document.doc_id = $doc_id";
	$maintainer=$conn->exec("$sql");
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $maintainer->resultStatus;
	while (@maintainer_row = $maintainer->fetchrow) {
		$maintainer_name = $maintainer_row[0];
		$maintainer_name =~ s/\&/\&amp;/;
		$maintainer_email = $maintainer_row[1];
		print "  <contributor>$maintainer_email ($maintainer_name)</contributor>\n";
	}
  
	#TITLE
	print "  <title>$title</title>\n";

	#DATE
	print "  <date>$last_update</date>\n";

	#VERSION
	print "  <versionGroup>\n";
	print "    <version>\n";
	print "      <id>$version</id>\n";
	print "      <date>$last_update</date>\n";
	print "    </version>\n";
	print "  </versionGroup>\n";

	#TYPE
	print "  <type>$class</type>\n";

	#FORMAT
	if ( $format eq 'XML' ) {
		print "  <format dtd='$dtd' mime='text/xml'/>\n";
	}
	if ( $format eq 'SGML' ) {
		if ( $dtd eq 'HTML' ) {
			print "  <format dtd='$dtd' mime='text/html'/>\n";
		}
		else {
			print "  <format dtd='$dtd' mime='text/sgml'/>\n";
		}
	}
	if ( $format eq 'TEXT' ) {
		print "  <format mime='text/plain'/>\n";
	}
	if ( $format eq 'PDF' ) {
		print "  <format mime='application/pdf'/>\n";
	}
	if ( $format eq 'LaTeX' ) {
		print "  <format mime='application/x-latex'/>\n";
	}

	#IDENTIFIER
	print "  <identifier>$url</identifier>\n";

	#DESCRIPTION
	print "  <description>$abstract</description>\n";

	#SOURCE
	print "  <source>http://www.linuxdoc.org (Linux Documentation Project)</source>\n";

	#LANGUAGE
	print "  <language>en</language>\n";

	#RELATION

	#COVERAGE

	#RIGHTS
	print "  <rights>\n";
	print "    <type>$license</type>\n";
	if ( $license eq "GFDL" ) {
		print "    <license>http://www.fsf.org/licenses/fdl.html</license>\n";
	}
	if ( $license eq "GPL" ) {
		print "    <license>http://www.fsf.org/licenses/gpl.html</license>\n";
	}
	print "  </rights>\n";

	print "</resource>\n";
}
print "</omf>\n";

