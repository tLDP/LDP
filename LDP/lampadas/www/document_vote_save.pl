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

$doc_id = param('doc_id');
$vote   = param('vote');
$username = $query->remote_user();

$sql = "DELETE FROM doc_vote WHERE doc_id=$doc_id AND username='$username'";
$result=$conn->exec($sql);

$sql = "INSERT INTO doc_vote(doc_id, username, vote) values ($doc_id, '$username', $vote)";
$result=$conn->exec($sql);

$conn->exec($sql);

print $query->redirect("document_edit.pl?doc_id=$doc_id");

