#!/usr/bin/perl

use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("New Document");
print $L->NewDocTable();
$L->EndPage();

