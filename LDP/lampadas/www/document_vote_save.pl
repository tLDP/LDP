#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
if ($username ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
}

$doc_id = param('doc_id');
$vote   = param('vote');
$username = $query->remote_user();

$sql = "DELETE FROM doc_vote WHERE doc_id=$doc_id AND username='$username'";
$result=$conn->exec($sql);

$sql = "INSERT INTO doc_vote(doc_id, username, vote) values ($doc_id, '$username', $vote)";
$result=$conn->exec($sql);

$conn->exec($sql);

print $query->redirect("document_edit.pl?doc_id=$doc_id");

