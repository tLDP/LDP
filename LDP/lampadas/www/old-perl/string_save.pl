#! /usr/bin/perl
# 
use Lampadas;
$L = new Lampadas;

$string_id	= $L->Param('string_id');
$lang		= $L->Param('lang');
$string		= $L->Param('string');
$chkDel		= $L->Param('chkDel');

if ($chkDel eq 'on') {
	$L->DelString($string_id, $lang);
} else {
	$L->SaveString($string_id, $lang, $string);
}
$L->Redirect("string_edit.pl");
