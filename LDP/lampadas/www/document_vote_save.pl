#!/usr/bin/perl
#
use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

unless ($L->CurrentUserID()) {
	$L->Redirect("wrongpermission.pl");
}

$user_id	= $L->CurrentUserID();
$doc_id		= $L->Param('doc_id');
$vote		= $L->Param('vote');

$DB->Exec("DELETE FROM doc_vote WHERE doc_id=$doc_id AND user_id='$user_id'");

# Only allow votes 1 - 10. Voting 0 means remove my vote.
# 
if ($vote) {
	if ($vote > 10) {
		$L->StartPage();
		print "Ratings must be between 1 to 10.";
		$L->EndPage()
	} else {
		$sql = "INSERT INTO doc_vote(doc_id, user_id, vote) values ($doc_id, $user_id, $vote)";
		$DB->Exec($sql);
	}
}

# Update the average rating.
#
$vote_avg = $DB->Value("SELECT AVG(vote) FROM doc_vote WHERE doc_id = $doc_id");
$DB->Exec("UPDATE document SET rating=$vote_avg WHERE doc_id=$doc_id");

$L->Redirect("document_edit.pl?doc_id=$doc_id");

