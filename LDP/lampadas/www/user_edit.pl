#! /usr/bin/perl
#
use Pg;
use Lampadas;

$L = new Lampadas;

$dbmain = "ldp";
@row;

$user_id = $L->Param('user_id');

unless ($L->Admin() or ($L->CurrentUserID() == $user_id)) {
	$L->Redirect("wrongpermission.pl");
	exit;
}

$L->StartPage("Edit User");
print $L->UserTable($user_id);
print $L->UserDocsTable($user_id);
print $L->UserNotesTable($user_id);

$L->EndPage();

