#! /usr/bin/perl
# 
use Lampadas;
$L = new Lampadas;

$original_code	= $L->Param('original_code');
$string_code	= $L->Param('string_code');
$lang		= $L->Param('lang');
$string		= $L->Param('string');
$chkDel		= $L->Param('chkDel');

if ($chkDel eq 'on') {
	$L->DelString($string_code, $lang);
} else {
	$L->SaveString($original_code, $string_code, $lang, $string);
}
$L->Redirect("string_edit.pl");
