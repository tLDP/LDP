#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$topic_num		= $L->Param('topic_num');
$topic_name		= $L->Param('topic_name');
$topic_description	= $L->Param('topic_description');

$L->SaveTopic($topic_num, $topic_name, $topic_description);
$L->Redirect("topic_edit.pl?topic_num=$topic_num");
