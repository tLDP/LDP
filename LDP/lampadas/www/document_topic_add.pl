#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller       = param('caller');
$doc_id       = param('doc_id');
$topic        = param('topic');

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

@topic_subtopic_num = split /\./, $topic;
$topic_num    = $topic_subtopic_num[0];
$subtopic_num = $topic_subtopic_num[1];

$sql = "INSERT INTO document_topic (doc_id, topic_num, subtopic_num) VALUES ($doc_id, $topic_num, $subtopic_num)";

$result=$conn->exec($sql);

print $query->redirect($caller)

