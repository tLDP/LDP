#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect('wrongpermission.pl');
}

$L->StartPage("Updating CVS Cache");
@cvsresponse = $L->CVSUpdate();
foreach $cvsresponse (@cvsresponse) {
	print "$cvsresponse<br>\n";
}
print "<p>CVS Updated.";
$L->EndPage();
