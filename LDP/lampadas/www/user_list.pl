#!/usr/bin/perl

use Lampadas;
$L = new Lampadas;

$admin = $L->Admin();
$currentuser_id = $L->CurrentUserID();

unless ($L->Admin()) {
	print $query->redirect("wrongpermission.pl");
	exit;
}

$L->StartPage('Lampadas Users');
print $L->UsersTable();
$L->EndPage();

