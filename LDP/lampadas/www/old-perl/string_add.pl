#! /usr/bin/perl
# 
use Lampadas;
$L = new Lampadas;

$string_code	= $L->Param('string_code');
$lang		= $L->Param('lang');
$string		= $L->Param('string');

$L->AddString($string_code, $lang, $string);
$L->Redirect("string_edit.pl");
