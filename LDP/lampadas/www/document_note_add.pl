#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$doc_id   = param('doc_id');

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
if ($username ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
}

$note     = param('note');
while ($note =~ /\'/) {
	$note =~ s/\'/a1s2d3f4/;
}
while ($note =~ /a1s2d3f4/) {
	$note     =~ s/a1s2d3f4/\'\'/;
}

$conn=Pg::connectdb("dbname=$dbmain");
$sql = "INSERT INTO notes (doc_id, date_entered, username, notes) values ($doc_id, now(), '$username', '$note')";
$result=$conn->exec($sql);

print $query->redirect("document_edit.pl?doc_id=$doc_id");
