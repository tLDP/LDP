#!/usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

$L->StartPage('Statistics');
print $L->PubStatusStatsTable();
print $L->LicenseStatsTable();
print $L->FreeNonfreeStatsTable();
print $L->ClassStatsTable();
print $L->FormatStatsTable();
print $L->DTDStatsTable();
print $L->FormatDTDStatsTable();
print $L->DetailedStatsTable();
print $L->MiscStatsTable();
$L->EndPage();
