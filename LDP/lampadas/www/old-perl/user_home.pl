#! /usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$user_id = $L->Param('user_id');
$user_id = $L->CurrentUserID() unless ($user_id);

unless (($L->CurrentUserID() eq $user_id) or ($L->Admin())) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("My Lampadas");
print $L->String('user-home');
print $L->UserDocsTable($user_id);
$L->EndPage();

