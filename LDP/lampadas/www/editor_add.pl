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
} else {
	if (($row[1] ne 't') and ($row[2] != $doc_id)) {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}

# Read parameters
$caller          = param('caller');
$editor_name = param('editor_name');
$editor_name =~ s/\'/\'\'/;
$email           = param('email');

$sql = "SELECT max(editor_id) from editor";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$editor_id = $row[0] + 1;

$sql = "INSERT INTO editor(editor_id, editor_name, email) VALUES ($editor_id, '$editor_name', '$email')";

#print header;
#print start_html;
#print "<p>$editor_name";
#print "<p>$email";
#print "<p>$editor_id";
#print "<p>$sql";
#print end_html;
#exit;

$conn->exec($sql);

print $query->redirect($caller)

