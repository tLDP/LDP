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
$caller       = param('caller');
$doc_id       = param('doc_id');
$topic        = param('topic');

@topic_subtopic_num = split /\./, $topic;
$topic_num    = $topic_subtopic_num[0];
$subtopic_num = $topic_subtopic_num[1];

$sql = "INSERT INTO document_topic (doc_id, topic_num, subtopic_num) VALUES ($doc_id, $topic_num, $subtopic_num)";

$conn=Pg::connectdb("dbname=$dbmain");
$result=$conn->exec($sql);

print $query->redirect($caller)

