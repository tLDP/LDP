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
$doc_id       = param('doc_id');
$topic_num    = param('topic_num');
$subtopic_num = param('subtopic_num');
$caller       = param('caller');

$conn=Pg::connectdb("dbname=$dbmain");

$sql = "DELETE FROM document_topic WHERE doc_id=$doc_id AND topic_num=$topic_num AND subtopic_num=$subtopic_num";
$result=$conn->exec($sql);

print $query->redirect($caller)

