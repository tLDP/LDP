#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$doc_id       = param('doc_id');
$topic_num    = param('topic_num');
$subtopic_num = param('subtopic_num');
$caller       = param('caller');

$conn=Pg::connectdb("dbname=$dbmain");

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

$sql = "DELETE FROM document_topic WHERE doc_id=$doc_id AND topic_num=$topic_num AND subtopic_num=$subtopic_num";
$result=$conn->exec($sql);

print $query->redirect($caller)

