#!/usr/bin/perl
#
use FileHandle;
use Lampadas;
$L = new Lampadas;

$filename	= $L->Param('filename');
$file		= $L->Param('file');

unless ($L->Admin()) {
	%userfiles = $L->UserFiles($L->CurrentUserID());
	unless ($userfiles{$filename}) {
		$L->Redirect("wrongpermission.pl");
	}
}
%userfile = $userfiles{$filename};
$cvsroot = $L->Config('cvs_root');

# If we're not previewing, load data from database and determine version
# 
$fh = new FileHandle;
open $fh, ">$cvsroot$filename";
print $fh $file;
close $fh;

$L->StartPage("Saving $filename");
print "Saved.";
$L->EndPage();
