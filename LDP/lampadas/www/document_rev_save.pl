#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller        = param('caller');
$rev_id        = param('rev_id');
$doc_id        = param('doc_id');
$rev_version   = param('rev_version');
$rev_date      = param('rev_date');
$rev_init      = param('rev_init');
$rev_note      = param('rev_note');
while ($rev_note =~ /\'/) {
	$rev_note =~ s/\'/a1s2d3f4/;
}
while ($rev_note =~ /a1s2d3f4/) {
	$rev_note     =~ s/a1s2d3f4/\'\'/;
}
$chkDel        = param('chkDel');

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
		$user_maintainer_id = $row[2];
		$result=$conn->exec("SELECT count(*) FROM document_maintainer WHERE maintainer_id=$user_maintainer_id AND doc_id=$doc_id AND active='t'");
		@row = $result->fetchrow;
		unless ($row[0]) {
			print $query->redirect("../wrongpermission.html");
			exit;
		}
	}
}

if ( $chkDel eq 'on' ) {
  $sql = "DELETE FROM document_rev WHERE rev_id = $rev_id";
  $result=$conn->exec($sql);
}
else {
  $result=$conn->exec("UPDATE document_rev SET version  = '$rev_version' WHERE rev_id = $rev_id");
  $result=$conn->exec("UPDATE document_rev SET pub_date = '$rev_date'    WHERE rev_id = $rev_id");
  $result=$conn->exec("UPDATE document_rev SET initials = '$rev_init'    WHERE rev_id = $rev_id");
  $result=$conn->exec("UPDATE document_rev SET notes    = '$rev_note'    WHERE rev_id = $rev_id");
}

print $query->redirect($caller)



