#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
if ( $username eq "guest") {
  print header;
  print "<html><head><title>No Permission</title>\n";
  print "<link rel=stylesheet href='../ldp.css' type='text/css'></head>\n";
  print "<body>\n";
  print "<h1>No Permission</h1>\n";
  print "You do not have permission to modify the database.\n";
  print "<p>You need to <a href='../'>get an account</a> before you can modify data.\n";
  print end_html;
  exit;
}

$dbmain = "ldp";
@row;

$caller     = param('caller');

$sql = "SELECT max(doc_id) from document";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$doc_id = $row[0] + 1;
$title      = param('title');
$title      =~ s/\'/\'\'/;
$class      = param('class');
$format     = param('format');
$dtd        = param('dtd');

$pub_status = param('pub_status');

$sql = "INSERT INTO document(doc_id,   title,   filename, class,    format,    dtd,    dtd_version, version, last_update, url,  isbn, pub_status,   author_status,    review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained)";
$sql =         "$sql VALUES ($doc_id, '$title', NULL,     '$class', '$format', '$dtd', NULL,        NULL,    NULL,        NULL, NULL, $pub_status', '$author_status', 'U',           NULL,        NULL,     NULL,    'U',                't')";

#print header;
#print start_html;
#print "<p>doc_id:$doc_id";
#print "<p>title:$title";
#print "<p>pub_status:$pub_status";
#print "<p>class:$class";
#print "<p>format:$format";
#print "<p>dtd:$dtd";
#print "<p>sql:$sql";
#print end_html;
#exit;

$conn->exec($sql);

print $query->redirect("document_edit.pl?doc_id=$doc_id");
#print $query->redirect($caller);

