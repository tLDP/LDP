#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$username = $query->remote_user();
if ( $username eq "guest") {
  print header;
  print "<html><head><title>No Permission</title>\n";
  print "<link rel=stylesheet href='../ldp.css' type='text/css'></head>\n";
  print "<body>\n";
  print "<h1>No Permission</h1>\n";
  print "You do not have permission to modify the database.\n";
  print "<p>You need to <a href='../'>get an account</a> before you can modify data.\n";
  print end_html;
  exit;
}
$dbmain = "ldp";
@row;

# Read parameters
$doc_id   = param('doc_id');

$username = $query->remote_user();

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
