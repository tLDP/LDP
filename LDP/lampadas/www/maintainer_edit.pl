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

system("./navbar.pl");

print "<p>ID: $maintainer_id";
print "<form name=edit method=POST action='maintainer_save.pl'>";
print "<input type=hidden name=maintainer_id value=$maintainer_id></input>";
printf "<p><table><tr><th>Name</th><th>Email</th></tr>";
print "</tr>\n";
print "<tr><td>\n";
print 'Name: <input type=text name="maintainer_name" size=30 value="' . $maintainer_name . '"></input><br>';
printf "</td><td>\n";
print 'Email: <input type=text name="email" size=30 value="' . $email . '"></input><br>';
print "</td><td>\n";
print "<input type=submit value=Save>";
print "</td></tr></table>\n";
print "</form>";

$docs_result = $conn->exec("SELECT document.doc_id, document.title, class, pub_status.pub_status_name, document_maintainer.role, document_maintainer.active, document_maintainer.email, document.url FROM document_maintainer, document, pub_status WHERE document_maintainer.maintainer_id = $maintainer_id AND document.pub_status = pub_status.pub_status AND document_maintainer.doc_id = document.doc_id ORDER BY document.title");
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
  $url = $row[7];

  print "<tr>";
  print "<form method=POST action='document_maintainer_save.pl'>\n";
  print "<td valign=top><a href='document_edit.pl?doc_id=$doc_id'>$title</a>\n";
  if ( $url ) { print " <a href=$url>Go!</a>" }
  print "</td>\n";
  print "<td valign=top>$class</td>\n";
  print "<td valign=top>$pub_status_name</td>\n";
  print "<td valign=top>$role</td>\n";
  print "<td valign=top>$active</td>\n";
  print "<td valign=top>$feedback_email</td>\n";
  print "</form>";
  print "</tr>\n";
}
printf "</table>\n";




print "<p><hr>";





$notes_result = $conn->exec("SELECT date_entered, notes, username FROM maintainer_notes WHERE maintainer_id = $maintainer_id ORDER BY date_entered");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $notes_result->resultStatus;

print "<h2>Notes</h2>\n";

print "<form name=notes method=POST action='maintainer_note_add.pl'>";
print "<p><table>\n";
print "<tr><th>Date and Time</th><th>User</th><th>Note</th></tr>";
while (@row = $notes_result->fetchrow) {
  $date_entered = $row[0];
  $notes        = $row[1];
  $notes        =~ s/</&lt;/;
  $notes        =~ s/>/&gt;/;
  $username     = $row[2];
  print "<tr><td valign=top>$date_entered</td><td valign=top>$username</td><td valign=top>$notes</td></tr>\n";
}
print "<tr><td colspan=2 align=right>To add a note, type the note, then click Save.</td>\n";
print "<td><textarea name=note rows=10 cols=40 wrap></textarea>\n";
print "<input type=hidden name=maintainer_id value=$maintainer_id>\n";
print "<input type=submit value='Save'></td>\n";
print "</tr>";
print "</table>\n";
print "</form>";

print end_html;

