#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$dbmain = "ldp";
@row;

# Read parameters
$doc_id       = param('doc_id');

print header(-expires=>'now');

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$result = $conn->exec("SELECT title, filename FROM document WHERE doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$title		= $row[0];
$title		=~  s/\s+$//;
$filename	= $row[1];

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

print "<p>";
print "<a href='document_edit.pl?doc_id=$doc_id'>Meta-Data</a>\n";
print "&nbsp;|&nbsp;";
print "<a href='document_wiki.pl?doc_id=$doc_id'>Edit</a>\n";

print "<p><table>\n";
print "<tr><th align=right>Revision</th><th>Saved</th><th>Comment</th><th>User</th></tr>\n";
$result = $conn->exec("SELECT revision, date_entered, wiki, notes, username FROM document_wiki WHERE doc_id = $doc_id ORDER BY revision DESC LIMIT 10, 0");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
while (@row = $result->fetchrow) {
	$revision	= $row[0];
	$date_entered	= $row[1];
	$wiki		= $row[2];
	$wiki		=~  s/\s+$//;
	$notes		= $row[3];
	$username	= $row[4];

	print "<tr><td align=right>$revision</td>\n";
	print "<td>$date_entered</td>\n";
	print "<td>$notes</td>\n";
	print "<td>$username</td></tr>\n";
}
print "</table>\n";

print end_html;

