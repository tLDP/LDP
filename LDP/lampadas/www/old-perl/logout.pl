#! /usr/bin/perl

use Lampadas;

$L = new Lampadas;

$L->Logout('Logged Out');	# Logout() calls Start_Page to clear the cookie.
print "<p>Logged out.\n";
$L->EndPage();
