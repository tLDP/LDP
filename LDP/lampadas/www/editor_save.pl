#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$editor_id   = param('editor_id');
$editor_name = param('editor_name');
$editor_name =~ s/\'/\'\'/;
$email       = param('email');
$notes       = param('notes');
$notes       =~ s/\'/\'\'/;

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

$sql = "UPDATE editor SET editor_name='$editor_name', email='$email', notes='$notes' WHERE editor_id = $editor_id";
$result=$conn->exec($sql);
print $query->redirect("editor_edit.pl?editor_id=$editor_id");

