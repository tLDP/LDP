#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller		= param('caller');
$doc_id		= param('doc_id');
$user_id	= param('user_id');
$active		= param('active');
$role		= param('role');
$email		= param('email');
$chkDel		= param('chkDel');

$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin FROM username WHERE username='$username'");
@row = $result->fetchrow;
$founduser = $row[0];
$founduser =~ s/\s+$//;
if ($username ne $founduser) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		$user_maintainer_id = $row[2];
		$result=$conn->exec("SELECT count(*) FROM document_maintainer WHERE maintainer_id=$user_maintainer_id AND doc_id=$doc_id AND active='t'");
		@row = $result->fetchrow;
		unless ($row[0]) {
			print $query->redirect("../wrongpermission.html");
			exit;
		}
	}
}

#print header;
#print start_html;

if ( $chkDel eq 'on' ) {
	$sql = "DELETE FROM document_user WHERE doc_id = $doc_id and user_id = $user_id";
	$result=$conn->exec($sql);
#	print "<p>$sql\n";
} else {
	$sql = "UPDATE document_user SET active = '$active' WHERE doc_id = $doc_id and user_id = $user_id";
	$result=$conn->exec($sql);
	$sql = "UPDATE document_user SET role   = '$role'   WHERE doc_id = $doc_id and user_id = $user_id";
	$result=$conn->exec($sql);
	$sql = "UPDATE document_user SET email  = '$email'  WHERE doc_id = $doc_id and user_id = $user_id";
	$result=$conn->exec($sql);

#	print "<p>$sql\n";
}

#update the maintained field in the document record
$sql = "SELECT COUNT(*) as active_users FROM document_user WHERE doc_id=$doc_id AND (role='Author' OR role='Co-Author' OR role='Maintainer') AND active='t'";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$active_users = $row[0];

#print "<p>active_users: $active_users\n";

if ($active_users) {
	$maintained = "t"
} else {
	$maintained = "f"
}
$sql = "UPDATE document SET maintained='$maintained' WHERE doc_id=$doc_id";
$result=$conn->exec($sql);

#print "<p>$sql\n";
#print end_html;
#exit;

print $query->redirect($caller)

