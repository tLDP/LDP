#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;
$L->StartPage("Running Lintadas...");
$L->Lintadas();
print "<p>Ran Lampadas on all documents.";
$L->EndPage();

