#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller        = param('caller');
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

$sql = "SELECT max(rev_id) FROM document_rev WHERE doc_id = $doc_id";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$rev_id = $row[0] + 1;

$sql = "INSERT INTO document_rev(rev_id, doc_id, version, pub_date, initials, notes) VALUES ($rev_id, $doc_id, '$rev_version', '$rev_date', '$rev_init', '$rev_note')";
$result=$conn->exec($sql);

#print "Content-Type: text/plain\n\n";
#print "$sql\n";

print $query->redirect($caller)



