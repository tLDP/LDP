#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$L->StartPage("About Lampadas");
print $L->String(about);
$L->EndPage();

