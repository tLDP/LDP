#! /usr/bin/perl

use Lampadas;

$L = new Lampadas;

if ($L->Login('Logged In')) {	# Login() calls Start_Page to set the cookie.
	print "<p>Login unsuccessful.";
} else {
	print "<p>Login successful.";
}
$L->EndPage();
