#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller      = param('caller');
$doc_id      = param('doc_id');
$editor_id   = param('editor_id');
$active      = param('active');
$editor_role = param('editor_role');

$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
$founduser = $row[0];
$founduser =~ s/\s+$//;
if ($username ne $founduser) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}

#print header;
#print start_html;
$sql = "INSERT INTO document_editor(doc_id, editor_id, active, editor_role) VALUES ($doc_id, $editor_id, '$active', '$editor_role')";
$result=$conn->exec($sql);


#print header;
#print start_html;
#print $sql;
#print end_html;
#exit;

print $query->redirect($caller)

