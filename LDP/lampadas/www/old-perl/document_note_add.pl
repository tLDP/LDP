#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

unless ($L->CurrentUserID()) {
	$L->StartPage("Not logged in");
	print "You must be logged in to add a note.";
	$L->EndPage();
}

# Read parameters
$doc_id	= $L->Param('doc_id');
$notes	= $L->Param('notes');
while ($notes =~ /\'/) {
	$notes =~ s/\'/a1s2d3f4/;
}
while ($notes =~ /a1s2d3f4/) {
	$notes     =~ s/a1s2d3f4/\'\'/;
}

$sql = "INSERT INTO notes (doc_id, date_entered, notes, creator_id) values ($doc_id, now(), '$notes', " . $L->CurrentUserID() . ")";
$DB->Exec($sql);
$L->Redirect("document_edit.pl?doc_id=$doc_id");
