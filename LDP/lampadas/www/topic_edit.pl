#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$topic_num = $L->Param("topic_num");

$L->StartPage("Edit Topic");
print $L->TopicTable($topic_num);
$L->EndPage();
