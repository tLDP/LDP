#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$caller = param('caller');

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
$maintainer_id   = param('maintainer_id');

$username = $query->remote_user();

$note     = param('note');
$note     =~ s/\'/\'\'/;

$conn=Pg::connectdb("dbname=$dbmain");
$sql = "INSERT INTO maintainer_notes (maintainer_id, date_entered, username, notes) values ($maintainer_id, now(), '$username', '$note')";
$result=$conn->exec($sql);

if ( $caller) {
	print $query->redirect($caller);
}
else {
	print $query->redirect("maintainer_edit.pl?maintainer_id=$maintainer_id");
}
