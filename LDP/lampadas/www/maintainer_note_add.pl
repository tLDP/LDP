#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller = param('caller');
$maintainer_id   = param('maintainer_id');
$note     = param('note');
$note     =~ s/\'/\'\'/;

$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
$founduser = $row[0];
$founduser =~ s/\s+$//;
if ($username ne $founduser) {
	print $query->redirect("../newaccount.html");
	exit;
}

$sql = "INSERT INTO maintainer_notes (maintainer_id, date_entered, username, notes) values ($maintainer_id, now(), '$username', '$note')";
$result=$conn->exec($sql);

if ( $caller) {
	print $query->redirect($caller);
}
else {
	print $query->redirect("maintainer_edit.pl?maintainer_id=$maintainer_id");
}
