#!/usr/bin/perl

use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage('Users');
print $L->UsersTable();
$L->EndPage();

