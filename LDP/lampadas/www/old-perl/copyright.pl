#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$L->StartPage("Coypright");
print $L->String(copyright);
$L->EndPage();

