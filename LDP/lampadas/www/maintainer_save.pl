#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$maintainer_id   = param('maintainer_id');
$maintainer_name = param('maintainer_name');
$maintainer_name =~ s/\'/\'\'/;
$email           = param('email');

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

$sql = "UPDATE maintainer SET maintainer_name='$maintainer_name', email='$email' WHERE maintainer_id = $maintainer_id";
$result=$conn->exec($sql);
print $query->redirect("maintainer_edit.pl?maintainer_id=$maintainer_id");

