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

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

# Read the votes
$votes_result = $conn->exec("select vote from doc_vote where doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $votes_result->resultStatus;
$vote_count = 0;
$vote_total = 0;
$vote_avg   = 0;
while (@row = $votes_result->fetchrow) {
  $vote = $row[0];
  $vote_count++;
  $vote_total = $vote_total + $vote;
}
if ($vote_count > 0) {
	$vote_avg = $vote_total / $vote_count;
}

%doc = $L->Doc($doc_id);

$L->StartPage("$doc{title} ($doc_id)");
print $L->DocTable($doc_id);
print $L->DocVersionsTable($doc_id);






print "<h2>Contributors</h2>";

$authors_result = $conn->exec("SELECT du.user_id, role, active, du.email, u.first_name, u.middle_name, u.surname FROM document_user du, username u WHERE du.doc_id = $doc_id and du.user_id = u.user_id ORDER BY active desc, first_name, middle_name, surname");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $authors_result->resultStatus;

print "<p><table class='box'>\n";
print "<tr><th>Status</th><th>Role</th><th>Name</th><th>Feedback Email</th><th colspan=2>Action</th></tr>";
while (@row = $authors_result->fetchrow) {
	$user_id = $row[0];
	if ( $user_list ) { $user_list =+ " OR " }
	$user_list =+ "n.user_id = $user_id";
	$role          = $row[1];
	$role          =~ s/\s*$//;
	if ( $row[2] eq 't' ) { $active = "Active" } else { $active = "Inactive" }
	$email	= $row[3];
	$first_name	= $row[4];
	$middle_name	= $row[5];
	$surname	= $row[6];
	$name = "$first_name $middle_name $surname";
	print "<tr>";
	print "<form method=POST action='document_user_save.pl'>";
	print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
	print "<input type=hidden name=doc_id value=$doc_id>";
	print "<input type=hidden name=user_id value=$user_id>";

	print '<td valign=top><select name="active">';
	if ($active eq "Active") { print '<option selected value="t">Active</option>' } else { print '<option value="t">Active</option>' }
	if ($active eq "Inactive") { print '<option selected value="f">Inactive</option>' } else { print '<option value="f">Inactive</option>' }
	print "</select></td>";

	print "<td valign=top><select name='role'>";
	if ( $role eq "Author" ) { print '<option selected>Author</option>' } else { print '<option>Author</option>' }
	if ( $role eq "Co-Author" ) { print '<option selected>Co-Author</option>' } else { print '<option>Co-Author</option>' }
	if ( $role eq "Maintainer" ) { print '<option selected>Maintainer</option>' } else { print '<option>Maintainer</option>' }
	if ( $role eq "Converter" ) { print '<option selected>Converter</option>' } else { print '<option>Converter</option>' }
	if ( $role eq "Translator" ) { print '<option selected>Translator</option>' } else { print '<option>Translator</option>' }
	if ( $role eq "TECH" ) { print '<option selected>TECH</option>' } else { print '<option>TECH</option>' }
	if ( $role eq "LANG" ) { print '<option selected>LANG</option>' } else { print '<option>LANG</option>' }
	print "</select></td>\n";

	print "<td valign=top><a href='user_edit.pl?user_id=$user_id'>$name</a></td>\n";
	print "<td valign=top><input type=text name=email width=20 size=20 value='$email'></input></td>\n";
	print "<td valign=top><input type=checkbox name=chkDel>Del</td>";
	print "<td valign=top><input type=submit value=Save></td>\n";
	print "</form>";
	print "</tr>\n";
}

# For assigning a new contributor
print "<tr>";
print "<form method=POST action='document_user_add.pl'>";
print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
print "<input type=hidden name=doc_id value=$doc_id>";

print '<td valign=top><select name="active">';
print '<option value="t">Active</option>';
print '<option value="f">Inactive</option>';
print "</select></td>";

print "<td valign=top><select name='role'>";
print '<option>Author</option>';
print '<option>Co-Author</option>';
print '<option>Maintainer</option>';
print '<option>Converter</option>';
print '<option>Translator</option>';
print '<option>TECH</option>';
print '<option>LANG</option>';
print "</select></td>\n";

print "<td valign=top>";

$sql = "SELECT user_id, first_name, middle_name, surname FROM username ORDER BY first_name, middle_name, surname";
$authors_result = $conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $authors_result->resultStatus;

print "<select name=user_id\n";
print "<option>\n";
while (@row = $authors_result->fetchrow) {
	$user_id = $row[0];
	$first_name	= $row[1];
	$middle_name	= $row[2];
	$surname	= $row[3];
	$name = "$first_name $middle_name $surname";
	print "<option value=$user_id>$name\n"
}
print "</select>\n";
print "</td>\n";

print "<td valign=top><input type=text name=email width=20 size=20></td>\n";
print "<td valign=top></td>\n";
print "<td valign=top><input type=submit value=Add></td>\n";
print "</form>";
print "</tr>\n";

print "</table>\n";
print "<br><small>Note: Deleting a record here doesn't delete the user. It only deletes the association between the user and this document.</small>\n";














print "<h2>Topic Assignments</h2>\n";

@topics;
@topic_names;

$topic_count = 0;
$topic_result = $conn->exec("SELECT topic.topic_num, subtopic.subtopic_num, topic.topic_name, subtopic.subtopic_name FROM topic, subtopic WHERE subtopic.topic_num = topic.topic_num ORDER BY topic_num, subtopic_num");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $topic_result->resultStatus;
while (@row = $topic_result->fetchrow) {
  $topic_count++;
  $topics[$topic_count] = $row[0] . "." . $row[1];
  $topic_names[$topic_count] = $row[2] . ": " . $row[3];
}

print "<p><table class='box'>\n";
print "<tr><th>Topic</th><th>Action</th></tr>\n";
$document_topic_result = $conn->exec("SELECT topic.topic_num, topic.topic_name, subtopic.subtopic_num, subtopic.subtopic_name FROM document_topic, subtopic, topic WHERE document_topic.topic_num = subtopic.topic_num and document_topic.subtopic_num = subtopic.subtopic_num AND subtopic.topic_num = topic.topic_num AND doc_id=$doc_id ORDER BY topic_num, subtopic_num");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $document_topic_result->resultStatus;

while (@row = $document_topic_result->fetchrow) {
  $topic_num = $row[0];
  $topic_name = $row[1];
  $subtopic_num = $row[2];
  $subtopic_name = $row[3];
  print "<tr>\n";
  print "<form method=POST action='document_topic_del.pl'>\n";
  print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
  print "<input type=hidden name=doc_id value=$doc_id>";
  print "<input type=hidden name=topic_num value=$topic_num>";
  print "<input type=hidden name=subtopic_num value=$subtopic_num>";
  print "<td>$topic_num.$subtopic_num $topic_name: $subtopic_name</td>";
  print "<td valign=top><input type=submit value=Delete></td>\n";
  print "</form>\n";
  print "</tr>\n";
}
print "<tr>";
print "<form method=POST action='document_topic_add.pl'>";
print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
print "<input type=hidden name=doc_id value=$doc_id>";
print "<td valign=top>\n";
#print "<select name='topic'>";
#for ($topic = 0; $topic < @topics; $topic++) {
#  $topic_num = $topics[$topic];
#  $topic_name = $topic_names[$topic];
#  print "<option value=" . $topic_num . ">" . $topic_num . " " . $topic_name . "</option>\n";
#}
#print "</select>\n";
print $L->SubtopicCombo();
print "</td>\n";
print "<td valign=top><input type=submit value=Add></td>\n";
print "</form>\n";
print "</tr></table>\n";




#print "<h2>Audience Assignments</h2>\n";
#print "<p>under construction. move along...";

#print "<p><table class='box'>\n";
#print "<tr><th>Audience</th><th>Description</th></tr>\n";
#$audience_result = $conn->exec("SELECT audience, audience_level, audience_description FROM document_audience, audience WHERE document_audience.doc_id = $doc_id AND document_audience.audience = audience.audience ORDER BY audience_level");
#die $conn->errorMessage unless PGRES_TUPLES_OK eq $audience_result->resultStatus;

#while (@row = $Audience_result->fetchrow) {
#  $audience = $row[0];
#  $audience_level = $row[1];
#  $audience_description = $row[2];
#  print "<tr>\n";
#  print "<form method=POST action='document audience_del.pl'>\n";
#  print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
#  print "<input type=hidden name=doc_id value=$doc_id>";
#  print "<input type=hidden name=topic_num value=$topic_num>";
#  print "<input type=hidden name=subtopic_num value=$subtopic_num>";
#  print "<td>$topic_num.$subtopic_num $topic_name: $subtopic_name</td>";
#  print "<td valign=top><input type=submit value=Delete></td>\n";
#  print "</form>\n";
#  print "</tr>\n";
#}
#print "<tr>";
#print "<form method=POST action='document_topic_add.pl'>";
#print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
#print "<input type=hidden name=doc_id value=$doc_id>";
#print '<td valign=top><select name="topic">';
#print "<option value=></option>\n";
#for ($topic = 0; $topic < @topics; $topic++) {
#  $topic_num = $topics[$topic];
#  $topic_name = $topic_names[$topic];
#  print "<option value=" . $topic_num . ">" . $topic_num . " " . $topic_name . "</option>\n";
#}
#print "</select></td>\n";
#print "<td valign=top><input type=submit value=Add></td>\n";
#print "</form>\n";
#print "</tr></table>\n";











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

