#!/usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

$project = $L->Config('project');
$L->StartPage("Welcome");
print "Welcome to the $project Lampadas System.";
$L->EndPage();

