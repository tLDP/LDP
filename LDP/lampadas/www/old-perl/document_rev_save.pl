#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

# Read $L->Parameters
$caller		= $L->Param('caller');
$rev_id		= $L->Param('rev_id');
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
$chkDel        = $L->Param('chkDel');

$conn=Pg::connectdb("dbname=$dbmain");

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		print $query->redirect("wrongpermission.pl");
		exit;
	}
}

if ( $chkDel eq 'on' ) {
	$temp = $L->DelDocVersion($doc_id, $rev_id);
}
else {
	$temp = $L->SaveDocVersion($doc_id, $rev_id, $version, $pub_date, $initials, $notes);
}

$L->StartPage("Saved");
print $temp;
$L->EndPage();
