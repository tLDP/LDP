#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

# Read $L->Parameters
$doc_id		= $L->Param('doc_id');
$filename	= $L->Param('filename');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

$L->AddDocFile($doc_id, $filename);
$L->Redirect("document_edit.pl?doc_id=$doc_id");

