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
$chkDel      = param('chkDel');

$conn=Pg::connectdb("dbname=$dbmain");

if ( $chkDel eq 'on' ) {
  $sql = "DELETE FROM document_editor WHERE doc_id = $doc_id and editor_id = $editor_id";
  $result=$conn->exec($sql);
}
else {
  $sql = "UPDATE document_editor SET active = '$active' WHERE doc_id = $doc_id and editor_id = $editor_id";
  $result=$conn->exec($sql);
  $sql = "UPDATE document_editor SET editor_role = '$editor_role' WHERE doc_id = $doc_id and editor_id = $editor_id";
  $result=$conn->exec($sql);
}
print $query->redirect($caller)

