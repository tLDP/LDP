#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read parameters
$caller	= $L->Param('caller');
$doc_id	= $L->Param('doc_id');
$topic	= $L->Param('topic');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		print $query->redirect("wrongpermission.pl");
		exit;
	}
}

@topic_subtopic_num = split /\./, $topic;
$topic_num    = $topic_subtopic_num[0];
$subtopic_num = $topic_subtopic_num[1];

$sql = "INSERT INTO document_topic (doc_id, topic_num, subtopic_num) VALUES ($doc_id, $topic_num, $subtopic_num)";
$DB->Exec($sql);
$L->Redirect($caller);

