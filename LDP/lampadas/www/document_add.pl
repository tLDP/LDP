#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$dbmain = "ldp";
$conn=Pg::connectdb("dbname=$dbmain");
@row;

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin FROM username WHERE username='$username'");
@row = $result->fetchrow;
if ($username ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	$admin = $row[1];
	if ($admin ne 't') {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}

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

$sql = "INSERT INTO document(doc_id,   title,   filename, class,    format,    dtd,    dtd_version, version, last_update, url,  isbn, pub_status,    author_status,    review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained)";
$sql =         "$sql VALUES ($doc_id, '$title', NULL,     '$class', '$format', '$dtd', NULL,        NULL,    NULL,        NULL, NULL, '$pub_status', '$author_status', 'U',           NULL,        NULL,     NULL,    'U',                't')";

$conn->exec($sql);

print $query->redirect("document_edit.pl?doc_id=$doc_id");

