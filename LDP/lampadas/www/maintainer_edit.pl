#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$dbmain = "ldp";
@row;

# Read parameters
$maintainer_id       = param('maintainer_id');

# Load data from db and call edit form
$conn=Pg::connectdb("dbname=$dbmain");


$result = $conn->exec("SELECT maintainer_id, maintainer_name, email from maintainer where maintainer_id = $maintainer_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;

# Load from db
$maintainer_id   = $row[0];
$maintainer_name = $row[1];
$maintainer_name =~  s/\s*$//;
$email           = $row[2];
$email           =~  s/\s*$//;

print header(-expires=>'now');

print "<html><head><title>$maintainer_name</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'></head>";
print "<body>";

print "<h1>$maintainer_name</h1>\n";

print "<p><a href='../index.html'>Index</a> \n";
print "<a href='document_list.pl'>Documents</a> \n";
print "<a href='maintainer_list.pl'>Maintainers</a> \n";
print "<a href='editor_list.pl'>Editors</a> \n";

print "<p>ID: $maintainer_id";
print "<form name=edit method=POST action='maintainer_save.pl'>";
printf "<p>\n";
print "<input type=hidden name=maintainer_id value=$maintainer_id></input>";
printf "<p>\n";
print 'Name: <input type=text name="maintainer_name" size=30 value="' . $maintainer_name . '"></input><br>';
printf "<p>\n";
print 'Email: <input type=text name="email" size=30 value="' . $email . '"></input><br>';
printf "<p>\n";
print "<input type=submit value=Save>";
print "</form>";

$docs_result = $conn->exec("SELECT document.doc_id, document.title, class, pub_status.pub_status_name, document_maintainer.role, document_maintainer.active, document_maintainer.email FROM document_maintainer, document, pub_status WHERE document_maintainer.maintainer_id = $maintainer_id AND document.pub_status = pub_status.pub_status AND document_maintainer.doc_id = document.doc_id ORDER BY document.title");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $docs_result->resultStatus;

print "<h2>Documents</h2>\n";
printf "<p><table border=1 cellspacing=2\n";
print "<tr><th>Title</th><th>Class</th><th>Doc Status</th><th>Role</th><th>Active</th><th>Feedback Email</th></tr>";
while (@row = $docs_result->fetchrow) {
  $doc_id = $row[0];
  $title = $row[1];
  $class = $row[2];
  $pub_status_name = $row[3];
  $role = $row[4];
  $active = $row[5];
  if ( $active eq 't' ) { $active = "Active" } else { $active = "Inactive" }
  $feedback_email = $row[6];
  print "<tr>";
  print "<form method=POST action='document_maintainer_save.pl'>\n";
  print "<td valign=top><a href='document_edit.pl?doc_id=$doc_id'>$title</a></td>\n";
  print "<td valign=top>$class</td>\n";
  print "<td valign=top>$pub_status_name</td>\n";
  print "<td valign=top>$role</td>\n";
  print "<td valign=top>$active</td>\n";
  print "<td valign=top>$feedback_email</td>\n";
  print "</form>";
  print "</tr>\n";
}
printf "</table>\n";




print end_html;

