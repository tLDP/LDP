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
$chkDel      = param('chkDel');

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

if ( $chkDel eq 'on' ) {
  $sql = "DELETE FROM document_editor WHERE doc_id = $doc_id and editor_id = $editor_id";
  $result=$conn->exec($sql);
}
else {
  $sql = "UPDATE document_editor SET active = '$active' WHERE doc_id = $doc_id and editor_id = $editor_id";
  $result=$conn->exec($sql);
  $sql = "UPDATE document_editor SET editor_role = '$editor_role' WHERE doc_id = $doc_id and editor_id = $editor_id";
  $result=$conn->exec($sql);
}
print $query->redirect($caller)

