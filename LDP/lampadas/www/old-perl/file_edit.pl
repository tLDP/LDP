#!/usr/bin/perl

$editrows = 25;

use FileHandle;
use Lampadas;
$L = new Lampadas;

$doc_id		= $L->Param('doc_id');
$filename	= $L->Param('filename');

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
open $fh, "<$cvsroot$filename";
while ($line = <$fh>) {
	$file .= $line;
}
close $fh;

$L->StartPage("Editing $filename");
print "<table class='box' width='100%'>\n";
print "<form method=POST action='file_save.pl' name='file'>\n";
print "<input type='hidden' name='doc_id' value=$doc_id>\n";
print "<input type='hidden' name='filename' value='$filename'>\n";
print "<tr><th>Document Text</th></tr>\n";
print "<tr><td><textarea name=file rows=$editrows cols=20 style='width:100%' wrap>$file</textarea></td></tr>\n";
print "<tr><td><input type=submit value=Save name=Save></td></tr>\n";
print "</table>\n";
print "</form>\n";
$L->EndPage();
