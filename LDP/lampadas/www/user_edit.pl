#! /usr/bin/perl
#
use Pg;
use Lampadas;

$L = new Lampadas;

$dbmain = "ldp";
@row;

# Load data from db and call edit form
$conn=Pg::connectdb("dbname=$dbmain");

$user_id = $L->Param('user_id');

unless (($L->Admin) or ($L->CurrentUserID() == $user_id)) {
	$L->Redirect("../newaccount.html");
	exit;
}

$result = $conn->exec("SELECT user_id, username, first_name, middle_name, surname, email, admin FROM username WHERE user_id=$user_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;

# Load from db
# 
$user_id	= $row[0];
$username	= $row[1];
$username	=~ s/\s+$//;
$first_name	= $row[2];
$first_name	=~ s/\s+$//;
$middle_name	= $row[3];
$middle_name	=~ s/\s+$//;
$surname	= $row[4];
$surname	=~ s/\s+$//;
$email		= $row[5];
$admin		= $row[6];

$L->StartPage("User: $username");

print "<form name=edit method=POST action='user_save.pl'>";
print "<input type=hidden name=user_id value=$user_id></input>";
print "<p><table>\n";
print "<tr><th>Username:</th><td><input type=text name='username' size=30 value='$username'></input></td></tr>\n";
print "<tr><th>First Name:</th><td><input type=text name='first_name' size=30 value='$first_name'></input></td></tr>\n";
print "<tr><th>Middle Name:</th><td><input type=text name='middle_name' size=30 value='$middle_name'></input></td></tr>\n";
print "<tr><th>Surname:</th><td><input type=text name='surname' size=30 value='$surname'></input></td></tr>\n";
print "<tr><th>Email:</th><td><input type=text name='email' size=30 value='$email'></input></td></tr>\n";
if ($L->Admin) {
	print "<tr><th>Admin:</th><td><select name='admin'>\n";
	if ($admin eq 't') { print "<option selected value='t'>Yes</option>\n" } else { print "<option value='t'>Yes</option>\n" }
	if ($admin eq 'f') { print "<option selected value='f'>No</option>\n" } else { print "<option value='f'>No</option>\n" }
	print "</select></td></tr>\n";
}
print "<tr><th>New Password:</th><td><input type=text name='password' size=12></input></td></tr>";
print "<tr><td></td><td><input type=submit value=Save></td></tr>";
print "</table>";
print "</form>";




$docs_result = $conn->exec("SELECT document.doc_id, document.title, class, pub_status.pub_status_name, document_user.role, document_user.active, document_user.email, document.url FROM document_user, document, pub_status WHERE document_user.user_id = $user_id AND document.pub_status = pub_status.pub_status AND document_user.doc_id = document.doc_id ORDER BY document.title");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $docs_result->resultStatus;

print "<h2>Documents</h2>\n";
print "<p><table border=1 cellspacing=2\n";
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
print "</table>\n";




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

$L->EndPage();

