#! /usr/bin/perl

use CGI qw(:standard);
use Pg;
use Lampadas;

$L = new Lampadas;

$query = new CGI;
$dbmain = "ldp";
@row;
$message = '';

$doc_id       = $L->Param('doc_id');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		print $query->redirect("wrongpermission.pl");
		exit;
	}
}

%doc = $L->Doc($doc_id);

$L->StartPage("$doc{title} ($doc_id)");
print $L->DocTable($doc_id);
print $L->DocVersionsTable($doc_id);
print $L->DocUsersTable($doc_id);
print $L->DocTopicsTable($doc_id);




$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;


print "<h2>Rating</h2>\n";

print "<p><table class='bargraph'>\n";
for ( $i = 1; $i <= 10; $i++ ) {
	print "<td class='";
	if ($doc{rating} >= $i) { print "baron" } else { print "baroff" }
	print "'>&nbsp;&nbsp;</td>\n";
}
print "</tr></table>\n";

$votes_result = $conn->exec("select vote from doc_vote where doc_id = $doc_id and user_id='$currentuser_id'");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $votes_result->resultStatus;
@row = $votes_result->fetchrow;
$vote = $row[0];

print "<p>You can rate each document on a scale from 1 to 10, where 1 is very poor and 10 is excellent.\n";
print "Your vote is averaged with the votes of others to obtain a rating for the document.\n";

print "<form name=vote method=POST action='document_vote_save.pl'>";
print "<p><table>\n";
print "<tr><td align=right>Votes:</td><td>$vote_count</td></tr>\n";
print "<tr><td align=right>Average:</td><td>$vote_avg</td></tr>\n";
print "<tr><td align=right>Your Vote:</td><td>\n";
print "<input name=vote type=text size=2 width=2 value=$vote></input>\n";
print "<input type=hidden name=doc_id value=$doc_id>\n";
print "<input type=submit value='Rate'></td>\n";
print "</table>";

print "</form>";












print "<h2>Notes</h2>\n";

$notes_result = $conn->exec("SELECT n.date_entered, n.notes, u.username FROM notes n, username u WHERE n.creator_id=u.user_id AND n.doc_id=$doc_id ORDER BY date_entered");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $notes_result->resultStatus;

print "<form name=notes method=POST action='document_note_add.pl'>";
print "<p><table class='box'>\n";
print "<tr><th>Date and Time</th><th>User</th><th>Note</th></tr>";
while (@row = $notes_result->fetchrow) {
  $date_entered	= $row[0];
  $notes        = $row[1];
  $notes        =~ s/</&lt;/;
  $notes        =~ s/>/&gt;/;
  $username     = $row[2];
  print "<tr><td valign=top>$date_entered</td><td valign=top>$username</td><td valign=top>$notes</td></tr>\n";
}
print "<tr><td colspan=2 align=right>To add a note, type the note, then click Save.</td>\n";
print "<td><textarea name=note rows=10 cols=40 wrap></textarea>\n";
print "<input type=hidden name=doc_id value=$doc_id>\n";
print "<input type=submit value='Save'></td>\n";
print "</tr>";
print "</table>\n";
print "</form>";




print "<h2>Contributor Notes</h2>\n";

print "<p><table class='box'>\n";
print "<tr><th>Date and Time</th><th>User</th><th>Contributor</th><th>Note</th></tr>";

if ($user_list) {
	$sql = "SELECT n.date_entered, n.notes, u.username, u.first_name, u.middle_name, u.surname FROM username_notes n, username u  WHERE u.user_id=n.user_id AND $user_list ORDER BY date_entered";
	$notes_result = $conn->exec($sql);
	die $conn->errorMessage unless PGRES_TUPLES_OK eq $notes_result->resultStatus;

	while (@row = $notes_result->fetchrow) {
		$date_entered = $row[0];
		$notes        = $row[1];
		$notes        =~ s/</&lt;/;
		$notes        =~ s/>/&gt;/;
		$username     = $row[2];
		$first_name	= $row[3];
		$middle_name	= $row[4];
		$surname	= $row[5];
		$name = $surname . ', ' . $first_name . ' ' . $middle_name;
		print "<tr>\n";
		print "<td valign=top>$date_entered</td>\n";
		print "<td valign=top>$username</td>\n";
		print "<td valign=top>$name</td>\n";
		print "<td valign=top>$notes</td>\n";
		print "</tr>\n";
	}
}

print "</table>\n";

$L->EndPage();

