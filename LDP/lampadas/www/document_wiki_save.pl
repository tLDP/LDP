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
$doc_id        = param('doc_id');
$wiki          = param('wiki');
while ($wiki =~ /\'/) {
	$wiki =~ s/\'/a1s2d3f4/;
}
while ($wiki =~ /a1s2d3f4/) {
	$wiki =~ s/a1s2d3f4/\'\'/;
}

$conn=Pg::connectdb("dbname=$dbmain");

$sql = "UPDATE document SET wiki='$wiki' WHERE doc_id=$doc_id";
$result=$conn->exec($sql);

print $query->redirect("document_wiki.pl?doc_id=$doc_id");


print header;
print start_html;
print "<p>$sql";
print end_html;
exit;

