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
$caller        = param('caller');
$doc_id        = param('doc_id');
$maintainer_id = param('maintainer_id');
$active        = param('active');
$role          = param('role');
$email         = param('email');
$chkDel        = param('chkDel');

$conn=Pg::connectdb("dbname=$dbmain");

#print header;
#print start_html;
if ( $chkDel eq 'on' ) {
  $sql = "DELETE FROM document_maintainer WHERE doc_id = $doc_id and maintainer_id = $maintainer_id";
  $result=$conn->exec($sql);
}
else {
  $sql = "UPDATE document_maintainer SET active = '$active' WHERE doc_id = $doc_id and maintainer_id = $maintainer_id";
  $result=$conn->exec($sql);
  $sql = "UPDATE document_maintainer SET role   = '$role'   WHERE doc_id = $doc_id and maintainer_id = $maintainer_id";
  $result=$conn->exec($sql);
  $sql = "UPDATE document_maintainer SET email  = '$email'  WHERE doc_id = $doc_id and maintainer_id = $maintainer_id";
  $result=$conn->exec($sql);

#  print "$sql<br>\n";
#  print "active_maintainers: $active_maintainers\n";
}

#update the maintained field in the document record
$sql = "SELECT COUNT(*) as active_maintainers FROM document_maintainer WHERE doc_id=$doc_id AND (role='Author' OR role='Co-Author' OR role='Maintainer') AND active='t'";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$active_maintainers = $row[0];
if ( $active_maintainers > 0 ) { $maintained = "t" } else { $maintained = "f" }
$sql = "UPDATE document SET maintained='$maintained' WHERE doc_id=$doc_id";
$result=$conn->exec($sql);

print $query->redirect($caller)

