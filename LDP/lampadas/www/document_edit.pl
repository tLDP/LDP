#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

$dbmain = "ldp";
@row;

# Read parameters
$doc_id       = param('doc_id');

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$result = $conn->exec("SELECT doc_id, title, filename, class, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, ref_url, pub_date, tech_review_status, maintained, license, abstract FROM document WHERE doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;



# Load from db
$doc_id        = $row[0];
$title         = $row[1];
$title         =~  s/\s+$//;
$title         =~  s/\'//;
$filename      = $row[2];
$filename      =~  s/\s+$//;
$class         = $row[3];
$class         =~  s/\s+$//;
$format        = $row[4];
$format        =~  s/\s+$//;
$dtd           = $row[5];
$dtd           =~  s/\s+$//;
$dtd_version   = $row[6];
$dtd_version   =~  s/\s+$//;
$version       = $row[7];
$version       =~  s/\s+$//;
$last_update   = $row[8];
$url           = $row[9];
$isbn          = $row[10];
$pub_status    = $row[11];
$review_status = $row[12];
$tickle_date   = $row[13];
$ref_url       = $row[14];
$pub_date      = $row[15];
$tech_review_status = $row[16];
$maintained    = $row[17];
$license       = $row[18];
$license       =~  s/\s+$//;
$abstract      = $row[19];
$abstract      =~  s/\s+$//;

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

$votes_result = $conn->exec("select vote from doc_vote where doc_id = $doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $votes_result->resultStatus;
@row = $votes_result->fetchrow;
$vote = $row[0];



print header(-expires=>'now');

print "<html><head><title>$title</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
print "</head>";
print "<body>";

print "<h1>$title</h1>\n";

print "<p><a href='../index.html'>Index</a> ";
print "<a href='topic_list.pl'>Topics</a> ";
print "<a href='document_list.pl'>Documents</a> ";
print "<a href='maintainer_list.pl'>Maintainers</a> ";
print "<a href='editor_list.pl'>Editors</a> ";

print "<p>ID: $doc_id";

print "<form method=POST action='document_save.pl' name='edit'>\n";
print "<input type=hidden name=doc_id value='$doc_id'>\n";

print "<table>\n";
print "<tr><th colspan=8>Document Details</th></tr>\n";
print "<tr><td align=right>Title:</td><td colspan=5><input type=text name=title size=60 value='$title'></td></tr>\n";
print "<tr><td align=right>Filename:</td><td colspan=5><input type=text name=filename size=60 value='$filename'></td></tr>\n";

print "<tr>";

print "<td align=right>Status:</td><td>";
print "<select name=pub_status>";
if ( $pub_status eq "N" ) { print '<option selected value="N">Active</option>'; } else { print '<option value="N">Active</option>' }
if ( $pub_status eq "?" ) { print '<option selected value="?">Unknown</option>'; } else { print '<option value="?">Unknown</option>' }
if ( $pub_status eq "A" ) { print '<option selected value="A">Archived</option>'; } else { print '<option value="A">Archived</option>' }
if ( $pub_status eq "D" ) { print '<option selected value="D">Deleted</option>'; } else { print '<option value="D">Deleted</option>' }
if ( $pub_status eq "O" ) { print '<option selected value="O">Offsite</option>'; } else { print '<option value="O">Offsite</option>' }
if ( $pub_status eq "P" ) { print '<option selected value="P">Pending</option>'; } else { print '<option value="P">Pending</option>' }
if ( $pub_status eq "R" ) { print '<option selected value="R">Replaced</option>'; } else { print '<option value="R">Replaced</option>' }
if ( $pub_status eq "W" ) { print '<option selected value="W">Wishlist</option>'; } else { print '<option value="W">Wishlist</option>' }
print "</select></td>";

print "<td align=right>Class:</td><td>\n";
print "<select name=class>";
if ( $class eq "BACKGROUNDER" ) { print '<option selected>BACKGROUNDER</option>'; } else { print '<option>BACKGROUNDER</option>' }
if ( $class eq "HOWTO" ) { print '<option selected>HOWTO</option>'; } else { print '<option>HOWTO</option>' }
if ( $class eq "MINI" ) { print '<option selected>MINI</option>'; } else { print '<option>MINI</option>' }
if ( $class eq "FAQ" ) { print '<option selected>FAQ</option>'; } else { print '<option>FAQ</option>' }
if ( $class eq "QUICK" ) { print '<option selected>QUICK</option>'; } else { print '<option>QUICK</option>' }
if ( $class eq "GUIDE" ) { print '<option selected>GUIDE</option>'; } else { print '<option>GUIDE</option>' }
if ( $class eq "TEMPLATE" ) { print '<option selected>TEMPLATE</option>'; } else { print '<option>TEMPLATE</option>' }
print "</select></td>";

print "<td align=right>Maintained:</td><td>\n";
if ( $maintained eq "t" ) { print 'Yes'; } else { print 'No' }
#print "<select name=maintained>";
#if ( $maintained eq "t" ) { print '<option selected value="t">Yes</option>'; } else { print '<option value="t">Yes</option>' }
#if ( $maintained eq "f" ) { print '<option selected value="f">No</option>'; } else { print '<option value="f">No</option>' }
#print "</select>";
print "</td>";

print "</tr>\n<tr>\n";

print "<td align=right>Review Status:</td><td>";
print "<select name=review_status>";
if ( $review_status eq "U" ) { print '<option selected value="U">Unreviewed</option>'; } else { print '<option value="U">Unreviewed</option>' }
if ( $review_status eq "N" ) { print '<option selected value="N">Need Identified</option>'; } else { print '<option value="N">Need Identified</option>' }
if ( $review_status eq "P" ) { print '<option selected value="P">Pending</option>'; } else { print '<option value="P">Pending</option>' }
if ( $review_status eq "R" ) { print '<option selected value="R">Completed</option>'; } else { print '<option value="R">Completed</option>' }
print "</select></td>";

print "<td align=right>Tech Review:</td><td>";
print "<select name=tech_review_status>";
if ( $tech_review_status eq "U" ) { print '<option selected value="U">Unreviewed</option>'; } else { print '<option value="U">Unreviewed</option>' }
if ( $tech_review_status eq "N" ) { print '<option selected value="N">Need Identified</option>'; } else { print '<option value="N">Need Identified</option>' }
if ( $tech_review_status eq "P" ) { print '<option selected value="P">Pending</option>'; } else { print '<option value="P">Pending</option>' }
if ( $tech_review_status eq "R" ) { print '<option selected value="R">Completed</option>'; } else { print '<option value="R">Completed</option>' }
print "</select></td>";

print "<td align=right>License:</td><td>";
print "<select name=license>";
if ( $license eq "" )  { print '<option selected></option>'; } else { print '<option></option>' }
if ( $license eq "GFDL" )  { print '<option selected>GFDL</option>'; } else { print '<option>GFDL</option>' }
if ( $license eq "LDPL" ) { print '<option selected>LDPL</option>'; } else { print '<option>LDPL</option>' }
if ( $license eq "OPL" )  { print '<option selected>OPL</option>'; } else { print '<option>OPL</option>' }
if ( $license eq "GPL" )  { print '<option selected>GPL</option>'; } else { print '<option>GPL</option>' }
if ( $license eq "NONE" )  { print '<option selected>NONE</option>'; } else { print '<option>NONE</option>' }
if ( $license eq "PD" )  { print '<option selected>PD</option>'; } else { print '<option>PD</option>' }
if ( $license eq "OTHER" )  { print '<option selected>OTHER</option>'; } else { print '<option>OTHER</option>' }
print "</select></td>";

print "</tr>\n<tr>\n";

print "<td align=right>Published:</td><td><input type=text name=pub_date size=10 value='$pub_date'></td>";
print "<td align=right>Updated:</td><td><input type=text name=last_update size=10 value='$last_update'></td>";
print "<td align=right>Version:</td><td><input type=text name=version size=10 value='$version'></td>";

print "</tr>\n<tr>\n";

print "<td align=right>Format:</td><td>";
print "<select name=format>";
if ( $format eq "" ) { print '<option selected></option>'; } else { print '<option></option>' }
if ( $format eq "SGML" ) { print '<option selected>SGML</option>'; } else { print '<option>SGML</option>' }
if ( $format eq "XML" ) { print '<option selected>XML</option>'; } else { print '<option>XML</option>' }
if ( $format eq "TEXT" ) { print '<option selected>TEXT</option>'; } else { print '<option>TEXT</option>' }
if ( $format eq "LaTeX" ) { print '<option selected>LaTeX</option>'; } else { print '<option>LaTeX</option>' }
if ( $format eq "PDF" ) { print '<option selected>PDF</option>'; } else { print '<option>PDF</option>' }
print "</select></td>";

print "<td align=right>DTD:</td><td>";
print "<select name=dtd>";
if ( $dtd eq "" ) { print '<option selected></option>'; } else { print '<option></option>' }
if ( $dtd eq "N/A" ) { print '<option selected>N/A</option>'; } else { print '<option>N/A</option>' }
if ( $dtd eq "HTML" ) { print '<option selected>HTML</option>'; } else { print '<option>HTML</option>' }
if ( $dtd eq "DocBook" ) { print '<option selected>DocBook</option>'; } else { print '<option>DocBook</option>' }
if ( $dtd eq "LinuxDoc" ) { print '<option selected>LinuxDoc</option>'; } else { print '<option>LinuxDoc</option>' }
print "</select></td>";

print "<td align=right>DTD Version:</td><td>";
print "<input type=text name=dtd_version size=10 value='$dtd_version'>";
print "</td>";

print "</tr>\n<tr>\n";

print "<td align=right><a href='$url'>URL</a>:</td><td colspan=7><input type=text name=url size=60 value='$url'></td>";

print "</tr>\n<tr>\n";

print "<td align=right><a href='$ref_url'>Home</a>:</td><td colspan=7><input type=text name=ref_url size=60 value='$ref_url'></td>";

print "</tr>\n<tr>\n";

print "<td align=right>Tickle Date</td><td><input type=text name=tickle_date size=10 value='$tickle_date'></td>";

print "<td align=right>ISBN:</td><td><input type=text name=isbn size=14 value='$isbn'></td>";

print "<td></td><td><input type=submit value=Save></td>";

print "</tr>\n<tr>\n";

print "<td align=right>Abstract</td><td colspan=10><textarea name=abstract rows=10 cols=60 wrap></textarea>\n";

print "</tr>\n<tr>\n";

print "<td align=right>Rating</td><td>";

if ( $vote > 0 ) {
  print "<table border=0 bgcolor=black cellspacing=0 cellpadding=0>\n";
  for ( $i = 1; $i <= 10; $i++ ) {
    print "<td bgcolor=";
    if ( $vote >= $i ) { print "green" } else { print "black" }
    print ">&nbsp;&nbsp;</td>\n";
  }
  print "</tr></table>\n";
}
else {
  print "Not rated";
}

print "</td>";


print "</tr></table>\n";
print "</form>";









print "<p><hr>";




print "<h2>Contributors</h2>";

$authors_result = $conn->exec("SELECT maintainer.maintainer_id, role, active, document_maintainer.email, maintainer.email as author_email, maintainer_name FROM document_maintainer, maintainer WHERE doc_id = $doc_id and document_maintainer.maintainer_id = maintainer.maintainer_id ORDER BY active desc, maintainer_name");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $authors_result->resultStatus;

print "<p><table>\n";
print "<tr><th>Status</th><th>Role</th><th>Name</th><th>Feedback Email</th><th colspan=2>Action</th></tr>";
while (@row = $authors_result->fetchrow) {
  $maintainer_id = $row[0];
  $role          = $row[1];
  $role          =~  s/\s*$//;
  if ( $row[2] eq 't' ) { $active = "Active" } else { $active = "Inactive" }
  $feedback_email = $row[3];
  $email          = $row[4];
  if ( $row[5] eq '' ) { $maintainer_name = 'J. Doe' } else { $maintainer_name = "$row[5]" }
  print "<tr>";
  print "<form method=POST action='document_maintainer_save.pl'>";
  print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
  print "<input type=hidden name=doc_id value=$doc_id>";
  print "<input type=hidden name=maintainer_id value=$maintainer_id>";

  print '<td valign=top><select name="active">';
  if ( $active eq "Active" ) { print '<option selected value="t">Active</option>' } else { print '<option value="t">Active</option>' }
  if ( $active eq "Inactive" ) { print '<option selected value="f">Inactive</option>' } else { print '<option value="f">Inactive</option>' }
  print "</select></td>";

  print "<td valign=top><select name='role'>";
  if ( $role eq "Author" ) { print '<option selected>Author</option>' } else { print '<option>Author</option>' }
  if ( $role eq "Co-Author" ) { print '<option selected>Co-Author</option>' } else { print '<option>Co-Author</option>' }
  if ( $role eq "Maintainer" ) { print '<option selected>Maintainer</option>' } else { print '<option>Maintainer</option>' }
  if ( $role eq "Converter" ) { print '<option selected>Converter</option>' } else { print '<option>Converter</option>' }
  print "</select></td>\n";

  print "<td valign=top><a href='maintainer_edit.pl?maintainer_id=$maintainer_id'>$maintainer_name</a></td>\n";
  print "<td valign=top><input type=text name=email width=20 size=20 value='$feedback_email'></input></td>\n";
  print "<td valign=top><input type=checkbox name=chkDel>Del</td>";
  print "<td valign=top><input type=submit value=Save></td>\n";
  print "</form>";
  print "</tr>\n";
}

# For assigning a new contributor
#print "<tr><th colspan=6>New Contributor</th></tr>";
print "<tr>";
print "<form method=POST action='document_maintainer_add.pl'>";
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
print "</select></td>\n";

print "<td valign=top>";

$sql = "SELECT maintainer_id, maintainer_name FROM maintainer ORDER BY maintainer_name";
$authors_result = $conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $authors_result->resultStatus;

print "<select name=maintainer_id\n";
print "<option>\n";
while (@row = $authors_result->fetchrow) {
  $maintainer_id = $row[0];
  if ( $row[1] eq '' ) { $maintainer_name = 'J. Doe' } else { $maintainer_name = "$row[1]" }
  print "<option value=$maintainer_id>$maintainer_name\n"
}
print "</select>\n";
print "</td>\n";

print "<td valign=top><input type=text name=email width=20 size=20></td>\n";
print "<td valign=top></td>\n";
print "<td valign=top><input type=submit value=Add></td>\n";
print "</form>";
print "</tr>\n";

print "</table>\n";
print "<br><small>Note: Deleting a record here doesn't delete the maintainer. It only deletes the association between the maintainer and this document.</small>\n";









print "<p><hr>";





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
#  print "<p>found: " . $topics[$rownum] . " = " . $topic_names[$rownum];
}

print "<p><table>\n";
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
print '<td valign=top><select name="topic">';
print "<option value=></option>\n";
for ($topic = 0; $topic < @topics; $topic++) {
  $topic_num = $topics[$topic];
  $topic_name = $topic_names[$topic];
  print "<option value=" . $topic_num . ">" . $topic_num . " " . $topic_name . "</option>\n";
}
print "</select></td>\n";
print "<td valign=top><input type=submit value=Add></td>\n";
print "</form>\n";
print "</tr></table>\n";



print "<p><hr>";

print "<h2>Audience Assignments</h2>\n";
print "<p>under construction. move along...";

#print "<p><table>\n";
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





print "<p><hr>";





print "<h2>Editors</h2>";

$authors_result = $conn->exec("SELECT editor.editor_id, editor_role, active, editor.email, editor.editor_name FROM document_editor, editor WHERE doc_id = $doc_id and document_editor.editor_id = editor.editor_id ORDER BY active desc, editor_name");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $authors_result->resultStatus;

print "<p><table>\n";
print "<tr><th>Status</th><th>Role</th><th>Name</th><th>Email</th><th colspan=2>Action</th></tr>";
while (@row = $authors_result->fetchrow) {
  $editor_id   = $row[0];
  $editor_role = $row[1];
  $editor_role =~  s/\s*$//;
  if ( $row[2] eq 't' ) { $active = "Active" } else { $active = "Inactive" }
  if ( $row[4] eq '' ) { $editor_name = 'J. Doe' } else { $editor_name = $row[4] }
  print "<tr>";
  print "<form method=GET action='document_editor_save.pl'>";
  print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
  print "<input type=hidden name=doc_id value=$doc_id>";
  print "<input type=hidden name=editor_id value=$editor_id>";

  print '<td valign=top><select name="active">';
  if ( $active eq "Active" ) { print '<option selected value="t">Active</option>' } else { print '<option value="t">Active</option>' }
  if ( $active eq "Inactive" ) { print '<option selected value="f">Inactive</option>' } else { print '<option value="f">Inactive</option>' }
  print "</select></td>";

  print "<td valign=top><select name='editor_role'>";
  if ( $editor_role eq "LANG" ) { print '<option selected value="LANG">Language Editor</option>' } else { print '<option value="LANG">Language Editor</option>' }
  if ( $editor_role eq "TECH" ) { print '<option selected value="TECH">Technical Editor</option>' } else { print '<option value="TECH">Technical Editor</option>' }
  print "</select></td>\n";

  print "<td valign=top><a href='editor_edit.pl?editor_id=$editor_id'>$editor_name</a></td>\n";
  print "<td valign=top>" . $row[3] . "</td>\n";
  print "<td valign=top><input type=checkbox name=chkDel>Del</td>";
  print "<td valign=top><input type=submit value=Save></td>\n";
  print "</form>";
  print "</tr>\n";
}


# For assigning a new editor
print "<tr>";
print "<form method=POST action='document_editor_add.pl'>";
print "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
print "<input type=hidden name=doc_id value=$doc_id>";

print '<td valign=top><select name="active">';
print '<option value="t">Active</option>';
print '<option value="f">Inactive</option>';
print "</select></td>";

print "<td valign=top><select name='editor_role'>";
print '<option value="LANG">Language Editor</option>';
print '<option value="TECH">Technical Editor</option>';
print "</select></td>\n";

print "<td valign=top>";

$sql = "SELECT editor_id, editor_name FROM editor ORDER BY editor_name";
$editors_result = $conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $editors_result->resultStatus;

print "<select name=editor_id\n";
print "<option>\n";
while (@row = $editors_result->fetchrow) {
  $editor_id = $row[0];
  if ( $row[1] eq '' ) { $editor_name = 'J. Doe' } else { $editor_name = "$row[1]" }
  print "<option value=$editor_id>$editor_name</option>\n"
}
print "</select>\n";
print "</td>\n";

print "<td valign=top>&nbsp;</td>\n";
print "<td valign=top>&nbsp;</td>\n";
print "<td valign=top><input type=submit value=Add></td>\n";
print "</form>";
print "</tr>\n";

print "</table>\n";
print "<br><small>Note: Deleting a record here doesn't delete the editor. It only deletes the association between the editor and this document.</small>\n";



print "<p><hr>";

print "<h2>Rating</h2>\n";

print "<p><table border=0 cellspacing=0 cellpadding=0>\n";
for ( $i = 1; $i <= 10; $i++ ) {
  print "<td bgcolor=";
  if ( $vote >= $i ) { print "green" } else { print "black" }
  print ">&nbsp;&nbsp;&nbsp;</td>\n";
}
print "</tr></table>\n";

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






print "<p><hr>";





$notes_result = $conn->exec("SELECT date_entered, notes, username FROM notes WHERE doc_id = $doc_id ORDER BY date_entered");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $notes_result->resultStatus;

print "<h2>Notes</h2>\n";

print "<form name=notes method=POST action='document_note_add.pl'>";
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
print "<input type=hidden name=doc_id value=$doc_id>\n";
print "<input type=submit value='Save'></td>\n";
print "</tr>";
print "</table>\n";
print "</form>";

print end_html;

