#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$L->StartPage('Topic Listing');
print $L->TopicDocsTable();
$L->EndPage();

