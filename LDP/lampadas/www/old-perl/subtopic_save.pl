#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$topic_num		= $L->Param('topic_num');
$subtopic_num		= $L->Param('subtopic_num');
$subtopic_name		= $L->Param('subtopic_name');
$subtopic_description	= $L->Param('subtopic_description');

$L->SaveSubtopic($topic_num, $subtopic_num, $subtopic_name, $subtopic_description);
$L->Redirect("subtopic_edit.pl?subtopic_id=$topic_num" . '.' . $subtopic_num);
