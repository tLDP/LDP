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
$editor_id   = param('editor_id');
$editor_name = param('editor_name');
$editor_name =~ s/\'/\'\'/;
$email       = param('email');
$notes       = param('notes');
$notes       =~ s/\'/\'\'/;

$conn=Pg::connectdb("dbname=$dbmain");
$sql = "UPDATE editor SET editor_name='$editor_name', email='$email', notes='$notes' WHERE editor_id = $editor_id";
$result=$conn->exec($sql);
print $query->redirect("editor_edit.pl?editor_id=$editor_id");

