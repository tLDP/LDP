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

$L->StartPage("Edit User");

print $L->UserTable($user_id);
print $L->UserDocsTable($user_id);




$notes_result = $conn->exec("SELECT un.date_entered, un.notes, u.username FROM username u, username_notes un WHERE u.user_id = un.user_id AND u.user_id = $user_id ORDER BY date_entered");
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

