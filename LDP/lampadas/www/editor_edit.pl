#! /usr/bin/perl

use CGI qw(:standard);
use Pg;
$query = new CGI;

$dbmain = "ldp";
@row;

# Read parameters
$editor_id       = param('editor_id');

# Load data from db and call edit form
$conn=Pg::connectdb("dbname=$dbmain");


$result = $conn->exec("SELECT editor_id, editor_name, email, notes from editor where editor_id = $editor_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;

# Load from db
$editor_id   = $row[0];
$editor_name = $row[1];
$editor_name =~  s/\s*$//;
$email       = $row[2];
$email       =~  s/\s*$//;
$notes       = $row[3];
$notes       =~  s/\s*$//;


print header(-expires=>'now');

print "<html><head><title>$editor_name</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'></head>";
print "<body>";

print "<h1>$editor_name</h1>\n";

print "<p><a href='../index.html'>Index</a> \n";
print "<a href='topic_list.pl'>Topics</a> \n";
print "<a href='document_list.pl'>Documents</a> \n";
print "<a href='maintainer_list.pl'>Maintainers</a> ";
print "<a href='editor_list.pl'>Editors</a>";

print "<p>ID: $editor_id";
print "<form name=edit method=POST action='editor_save.pl'>";
print "<input type=hidden name=editor_id value=$editor_id></input>";
printf "<p><table>\n";
print '<tr><td>Name:</td><td><input type=text name="editor_name" size=30 value="' . $editor_name . '"></input></td></tr>';
print '<tr><td>Email:</td><td><input type=text name="email" size=30 value="' . $email . '"></input></td></tr>';
print "<tr><td valign=top>Notes:</td><td><textarea name=notes rows=10 cols=40>$notes</textarea></td></tr>\n";
print "<tr><td></td><td><input type=submit value=Save></td></tr>";
print "</table>";
print "</form>";

$docs_result = $conn->exec("SELECT document.doc_id, document.title, class, pub_status.pub_status_name, document_editor.editor_role, document_editor.active FROM document_editor, document, pub_status WHERE document_editor.editor_id = $editor_id AND document.pub_status = pub_status.pub_status AND document_editor.doc_id = document.doc_id ORDER BY document.title");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $docs_result->resultStatus;

print "\n<h2>Documents</h2>\n";
printf "<p><table border=1 cellspacing=2\n";
print "<tr><th>Title</th><th>Class</th><th>Doc Status</th><th>Role</th><th>Active</th></tr>";
while (@row = $docs_result->fetchrow) {
  $doc_id = $row[0];
  $title = $row[1];
  $class = $row[2];
  $pub_status_name = $row[3];
  $editor_role = $row[4];
  $active = $row[5];
  if ( $active eq 't' ) { $active = "Active" } else { $active = "Inactive" }
  print "<tr>";
  print "<form method=POST action='document_editor_save.pl'>\n";
  print "<td valign=top><a href='document_edit.pl?doc_id=$doc_id'>$title</a></td>\n";
  print "<td valign=top>$class</td>\n";
  print "<td valign=top>$pub_status_name</td>\n";
  print "<td valign=top>$editor_role</td>\n";
  print "<td valign=top>$active</td>\n";
  print "</form>";
  print "</tr>\n";
}
printf "</table>\n";

print end_html;

