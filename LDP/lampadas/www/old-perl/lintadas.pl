#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;
$L->StartPage("Running Lintadas...");
$L->Lintadas();
print $L->ErrorsTable();
$L->EndPage();

