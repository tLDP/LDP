#! /usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

# Read $L->Parameters
$doc_id		= $L->Param('doc_id');
$oldfilename	= $L->Param('oldfilename');
$filename	= $L->Param('filename');
$chkDel		= $L->Param('chkDel');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

if ( $chkDel eq 'on' ) {
	$L->DelDocFile($doc_id, $oldfilename);
} else {
	$L->SaveDocFile($doc_id, $oldfilename, $filename);
}
$L->Redirect("document_edit.pl?doc_id=$doc_id");

