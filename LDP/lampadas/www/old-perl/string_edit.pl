#! /usr/bin/perl
#
use Lampadas;
$L = new Lampadas;

unless ($L->SysAdmin()) {
	$L->Redirect("wrongpermission.pl");
}

$L->StartPage("Edit System Strings");
print $L->StringsTable();
$L->EndPage();

