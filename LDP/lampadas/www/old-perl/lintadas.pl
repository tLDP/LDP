#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect('wrongpermission.pl');
}

$L->StartPage("Running Lintadas...");
$L->Lintadas();
print $L->ErrorsTable();
$L->EndPage();

