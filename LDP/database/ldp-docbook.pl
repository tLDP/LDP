#! /usr/bin/perl

use Pg;

$dbmain = "ldp";
@row;

# Read parameters
$doc_id = $ARGV[0];

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

#load document meta-data
$result = $conn->exec("SELECT title, filename, class FROM document WHERE doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$title		= $row[0];
$title		=~  s/\s+$//;
$filename	= $row[1];
$class		= $row[2];
$class		=~  s/\s+$//;

$result = $conn->exec("SELECT wiki FROM document_wiki WHERE doc_id = $doc_id ORDER BY revision DESC LIMIT 1, 0");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$revision	= $revisions + 1;
$wiki		= $row[0];
$wiki		=~  s/\s+$//;

$txtfile = "/tmp/" . rand() . ".txt";
$sgmlfile = $txtfile;
$sgmlfile =~ s/\.txt/\.sgml/;
$abstractfile = $txtfile;
$abstractfile =~ s/\./abs\./;
$abstractsgmlfile = $sgmlfile;
$abstractsgmlfile =~ s/\./abs\./;

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

print $sgml;

system("rm $txtfile");
system("rm $sgmlfile");
system("rm $abstractfile");
system("rm $abstractsgmlfile");
