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

$conn=Pg::connectdb("dbname=$dbmain");

# Read parameters
$caller          = param('caller');
$editor_name = param('editor_name');
$editor_name =~ s/\'/\'\'/;
$email           = param('email');

$sql = "SELECT max(editor_id) from editor";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$editor_id = $row[0] + 1;

$sql = "INSERT INTO editor(editor_id, editor_name, email) VALUES ($editor_id, '$editor_name', '$email')";

#print header;
#print start_html;
#print "<p>$editor_name";
#print "<p>$email";
#print "<p>$editor_id";
#print "<p>$sql";
#print end_html;
#exit;

$conn->exec($sql);

print $query->redirect($caller)

