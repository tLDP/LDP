#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

# Read $L->Parameters
$caller		= $L->Param('caller');
$doc_id		= $L->Param('doc_id');
$version	= $L->Param('version');
$pub_date	= $L->Param('pub_date');
$initials	= $L->Param('initials');
$notes		= $L->Param('notes');

while ($notes =~ /\'/) {
	$notes =~ s/\'/a1s2d3f4/;
}
while ($notes =~ /a1s2d3f4/) {
	$notes =~ s/a1s2d3f4/\'\'/;
}

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		print $query->redirect("wrongpermission.pl");
		exit;
	}
}

$temp = $L->AddDocVersion($doc_id, $version, $pub_date, $initials, $notes);

$L->StartPage("Saved");
print "Saved.";
print "<p>$temp";
$L->EndPage();



