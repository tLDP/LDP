#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read parameters
$doc_id        = $L->Param('doc_id');
$title         = $L->Param('title');
$title         =~ s/\'/\'\'/;
$filename      = $L->Param('filename');
$filename      =~ s/\'/\'\'/;
$class         = $L->Param('class');
$format        = $L->Param('format');
$dtd           = $L->Param('dtd');
$dtd_version   = $L->Param('dtd_version');
$version       = $L->Param('version');
$version       =~ s/\'/\'\'/;
$last_update   = $L->Param('last_update');
$url           = $L->Param('url');
$isbn          = $L->Param('isbn');
$pub_status    = $L->Param('pub_status');
$review_status = $L->Param('review_status');
$tickle_date   = $L->Param('tickle_date');
$ref_url       = $L->Param('ref_url');
$pub_date      = $L->Param('pub_date');
$tech_review_status = $L->Param('tech_review_status');
$license       = $L->Param('license');
$abstract      = $L->Param('abstract');
while ($abstract =~ /\'/) {
	$abstract      =~ s/\'/a1s2d3f4/;
}
while ($abstract =~ /a1s2d3f4/) {
	$abstract      =~ s/a1s2d3f4/\'\'/;
}

$version       =~ s/\'/\'\'/;

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

# This is horribly inefficient, but allows partial saves.
# For our volume, it hardly matters.
#
$sql = "UPDATE document SET title='$title' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET filename='$filename' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET class='$class' WHERE doc_id=$doc_id";
$DB->Exec($sql);
if ($format) {
	$sql = "UPDATE document SET format='$format' WHERE doc_id=$doc_id";
} else {
	$sql = "UPDATE document SET format=null WHERE doc_id=$doc_id";
}
$DB->Exec($sql);
if ($dtd) {
	$sql = "UPDATE document SET dtd='$dtd' WHERE doc_id=$doc_id";
} else {
	$sql = "UPDATE document SET dtd=null WHERE doc_id=$doc_id";
}
$DB->Exec($sql);
$sql = "UPDATE document SET dtd_version='$dtd_version' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET version='$version' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET last_update='$last_update' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET url='$url' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET isbn='$isbn' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET pub_status='$pub_status' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET review_status='$review_status' WHERE doc_id=$doc_id";
$DB->Exec($sql);

if ( $tickle_date eq '' )
{  $sql = "UPDATE document SET tickle_date=NULL WHERE doc_id=$doc_id"; }
else
{  $sql = "UPDATE document SET tickle_date='$tickle_date' WHERE doc_id=$doc_id"; }
$DB->Exec($sql);

$sql = "UPDATE document SET ref_url='$ref_url' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET pub_date='$pub_date' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET tech_review_status='$tech_review_status' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET license='$license' WHERE doc_id=$doc_id";
$DB->Exec($sql);
$sql = "UPDATE document SET abstract='$abstract' WHERE doc_id=$doc_id";
$DB->Exec($sql);

$L->AddError("Document Saved.");
$L->Redirect("document_edit.pl?doc_id=$doc_id");
