#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("Error List");
print $L->ErrorsTable();
$L->EndPage();

