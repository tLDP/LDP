#!/usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# print the page
$L->StartPage('Document List');
print $L->DocsTable(\%wheres, \%optionals);
$L->EndPage();
