#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, user_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
$founduser = $row[0];
$founduser =~ s/\s+$//;
if ($username ne $founduser) {
	print $query->redirect("../newaccount.html");
	exit;
}
$user_id	= $row[2];

$doc_id	= param('doc_id');
$vote	= param('vote');

$sql = "DELETE FROM doc_vote WHERE doc_id=$doc_id AND user_id='$user_id'";
$result=$conn->exec($sql);

# Only allow votes 1 - 10. Zero votes mean remove my vote.
# 
if ($vote) {
	$sql = "INSERT INTO doc_vote(doc_id, user_id, vote) values ($doc_id, $user_id, $vote)";
	$result=$conn->exec($sql);
}

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

$sql = "UPDATE document SET rating=$vote_avg WHERE doc_id=$doc_id";
$conn->exec("$sql");

print $query->redirect("document_edit.pl?doc_id=$doc_id");

