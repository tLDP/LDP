#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$L->StartPage('Topic Listing');
#print $L->TopicsTable();
print $L->TopicDocsTable();
$L->EndPage();

