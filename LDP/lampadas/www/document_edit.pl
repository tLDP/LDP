#! /usr/bin/perl

use CGI qw(:standard);
use Pg;
use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

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
print $L->DocRatingTable($doc_id);
print $L->DocNotesTable($doc_id);










$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;




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

