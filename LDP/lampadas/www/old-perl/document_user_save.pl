#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read $L->Parameters
$caller		= $L->Param('caller');
$doc_id		= $L->Param('doc_id');
$user_id	= $L->Param('user_id');
$active		= $L->Param('active');
$role		= $L->Param('role');
$email		= $L->Param('email');
$chkDel		= $L->Param('chkDel');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

if ( $chkDel eq 'on' ) {
	$sql = "DELETE FROM document_user WHERE doc_id = $doc_id and user_id = $user_id";
	$DB->Exec($sql);
} else {
	$sql = "UPDATE document_user SET active = '$active' WHERE doc_id = $doc_id and user_id = $user_id";
	$DB->Exec($sql);
	$sql = "UPDATE document_user SET role   = '$role'   WHERE doc_id = $doc_id and user_id = $user_id";
	$DB->Exec($sql);
	$sql = "UPDATE document_user SET email  = '$email'  WHERE doc_id = $doc_id and user_id = $user_id";
	$DB->Exec($sql);
}

#update the maintained field in the document record
$sql = "SELECT COUNT(*) as active_users FROM document_user WHERE doc_id=$doc_id AND (role='Author' OR role='Co-Author' OR role='Maintainer') AND active='t'";
$active_users = $DB->Value($sql);
if ($active_users) {
	$maintained = "t"
} else {
	$maintained = "f"
}
$sql = "UPDATE document SET maintained='$maintained' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$L->Redirect($caller);
