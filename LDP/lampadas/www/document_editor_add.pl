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
$caller      = param('caller');
$doc_id      = param('doc_id');
$editor_id   = param('editor_id');
$active      = param('active');
$editor_role = param('editor_role');

$conn=Pg::connectdb("dbname=$dbmain");

#print header;
#print start_html;
$sql = "INSERT INTO document_editor(doc_id, editor_id, active, editor_role) VALUES ($doc_id, $editor_id, '$active', '$editor_role')";
$result=$conn->exec($sql);


#print header;
#print start_html;
#print $sql;
#print end_html;
#exit;

print $query->redirect($caller)

