#! /usr/bin/perl
#
use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read parameters
$caller		= $L->Param('caller');
$doc_id		= $L->Param('doc_id');
$user_id	= $L->Param('user_id');
$active		= $L->Param('active');
$role		= $L->Param('role');
$email		= $L->Param('email');

unless ($L->Admin()){
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

$sql = "INSERT INTO document_user(doc_id, user_id, active, role, email) VALUES ($doc_id, $user_id, '$active', '$role', '$email' )";
$DB->Exec($sql);

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

