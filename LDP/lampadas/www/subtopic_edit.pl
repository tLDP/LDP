#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$subtopic_id = $L->Param("subtopic_id");

$L->StartPage("Edit Subtopic");
print $L->SubtopicTable($subtopic_id);
$L->EndPage();
