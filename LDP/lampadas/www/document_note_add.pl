#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$doc_id   = param('doc_id');

$note     = param('note');
while ($note =~ /\'/) {
	$note =~ s/\'/a1s2d3f4/;
}
while ($note =~ /a1s2d3f4/) {
	$note     =~ s/a1s2d3f4/\'\'/;
}

$username = $query->remote_user();

$conn=Pg::connectdb("dbname=$dbmain");
$sql = "INSERT INTO notes (doc_id, date_entered, username, notes) values ($doc_id, now(), '$username', '$note')";
$result=$conn->exec($sql);

print $query->redirect("document_edit.pl?doc_id=$doc_id");
