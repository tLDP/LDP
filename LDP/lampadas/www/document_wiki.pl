#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$dbmain = "ldp";
@row;

# Read parameters
$doc_id       = param('doc_id');

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$result = $conn->exec("SELECT title, wiki, filename FROM document WHERE doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;



# Load from db
$title = $row[0];
$title =~  s/\s+$//;

$wiki	= $row[1];
$wiki   =~  s/\s+$//;

$txtname = "/var/www/txt2db/foo.txt";

$sgmlname = $txtname;
$sgmlname =~ s/\.txt/\.sgml/;

open(TXT, "> $txtname");
print TXT $wiki;
close(TXT);

$cmd = "/usr/lib/cgi-bin/gldp.org/txt2db.pl -o $sgmlname $txtname";
system($cmd);

open(SGML, $sgmlname);
while (<SGML>) {
	$line = $_;
	while ($line =~ /</) {
		$line =~ s/</&lt;/;
	}
	while ($line =~ />/) {
		$line =~ s/>/&gt;/;
	}
	$buf .= "<br>$line";
}
close(SGML);

print header(-expires=>'now');

print "<html><head><title>$title Wiki</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
print "</head>";
print "<body>";

print "<h1>$title Wiki</h1>\n";

print "<p><a href='/index.html'>Index</a> ";
print "<a href='/cgi-bin/document_list.pl'>Documents</a> ";
print "<a href='/cgi-bin/topic_list.pl'>Topics</a> ";
print "<a href='/cgi-bin/maintainer_list.pl'>Maintainers</a> ";
print "<a href='/cgi-bin/editor_list.pl'>Editors</a> ";
print "<a href='/cgi-bin/ldp_stats.pl'>Statistics</a> ";
print "<a href='/help/'>Help</a> ";

print "<p>ID: $doc_id";

print "<form method=POST action='document_wiki_save.pl' name='edit'>\n";
print "<input type=hidden name=doc_id value='$doc_id'>\n";

print "<table>\n";
print "<tr><th>Document Text</th></tr>\n";
print "<tr><td><textarea name=wiki rows=10 cols=60 wrap>$wiki</textarea></td></tr>\n";
print "</table>\n";

print "<input type=submit value=Save>\n";
print "</form>\n";

print "<p>$buf\n";

print end_html;

