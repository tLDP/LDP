#! /usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->CurrentUserID()) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("My Lampadas");
print $L->UserDocsTable($L->CurrentUserID());
$L->EndPage();

