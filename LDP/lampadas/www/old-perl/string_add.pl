#! /usr/bin/perl
# 
use Lampadas;
$L = new Lampadas;

$lang		= $L->Param('lang');
$string		= $L->Param('string');

$L->AddString($lang, $string);
$L->Redirect("string_edit.pl");
