#! /usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$user_id = $L->Param('user_id');
unless ($L->Admin() or ($L->CurrentUserID() == $user_id)) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("Edit User");
print $L->UserTable($user_id);
print $L->UserNotesTable($user_id);
$L->EndPage();

