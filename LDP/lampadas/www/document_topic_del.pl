#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read parameters
$doc_id		= $L->Param('doc_id');
$topic_num	= $L->Param('topic_num');
$subtopic_num	= $L->Param('subtopic_num');
$caller		= $L->Param('caller');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
		exit;
	}
}

$DB->Exec("DELETE FROM document_topic WHERE doc_id=$doc_id AND topic_num=$topic_num AND subtopic_num=$subtopic_num");

$L->Redirect($caller);


