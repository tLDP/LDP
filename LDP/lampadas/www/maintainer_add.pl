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
$conn=Pg::connectdb("dbname=$dbmain");

$dbmain = "ldp";
@row;

# Read parameters
$caller          = param('caller');
$maintainer_name = param('maintainer_name');
$maintainer_name =~ s/\'/\'\'/;
$email           = param('email');

$sql = "SELECT max(maintainer_id) from maintainer";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$maintainer_id = $row[0] + 1;

$sql = "INSERT INTO maintainer(maintainer_id, maintainer_name, email) VALUES ($maintainer_id, '$maintainer_name', '$email')";
$conn->exec($sql);

#print header;
#print start_html;
#print "<p>$maintainer_name";
#print "<p>$email";
#print "<p>$maintainer_id";
#print "<p>$sql";
#print end_html;
#exit;


print $query->redirect($caller)

