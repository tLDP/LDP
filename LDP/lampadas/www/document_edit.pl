#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$doc_id       = $L->Param('doc_id');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

%doc = $L->Doc($doc_id);

$L->StartPage("$doc{title} ($doc_id)");
print $L->DocTable($doc_id);
print $L->DocFilesTable($doc_id);
print $L->DocVersionsTable($doc_id);
print $L->DocUsersTable($doc_id);
print $L->DocTopicsTable($doc_id);
print $L->DocRatingTable($doc_id);
print $L->DocNotesTable($doc_id);
$L->EndPage();

