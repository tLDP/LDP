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
$maintainer_id   = param('maintainer_id');
$maintainer_name = param('maintainer_name');
$maintainer_name =~ s/\'/\'\'/;
$email           = param('email');

$conn=Pg::connectdb("dbname=$dbmain");
$sql = "UPDATE maintainer SET maintainer_name='$maintainer_name', email='$email' WHERE maintainer_id = $maintainer_id";
$result=$conn->exec($sql);
print $query->redirect("maintainer_edit.pl?maintainer_id=$maintainer_id");

