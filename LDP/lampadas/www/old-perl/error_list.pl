#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("Lintadas Error List");
print $L->ErrorsTable();
$L->EndPage();

