#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read parameters
$doc_id        = $L->Param('doc_id');
$title         = $L->Param('title');
$class         = $L->Param('class');
$format        = $L->Param('format');
$dtd           = $L->Param('dtd');
$dtd_version   = $L->Param('dtd_version');
$version       = $L->Param('version');
$last_update   = $L->Param('last_update');
$url           = $L->Param('url');
$isbn          = $L->Param('isbn');
$pub_status    = $L->Param('pub_status');
$review_status = $L->Param('review_status');
$tickle_date   = $L->Param('tickle_date');
$pub_date      = $L->Param('pub_date');
$ref_url       = $L->Param('ref_url');
$tech_review_status = $L->Param('tech_review_status');
$license       = $L->Param('license');
$abstract      = $L->Param('abstract');

unless ($L->Admin()) {
	%userdocs = $L->UserDocs($L->CurrentUserID());
	unless ($userdocs{$doc_id}) {
		$L->Redirect("wrongpermission.pl");
	}
}

$L->SaveDoc($doc_id, $title, $class, $format, $dtd, $dtd_version, $version, $last_update, $url, $isbn, $pub_status, $review_status, $tickle_date, $pub_date, $ref_url, $tech_review_status, $license, $abstract);
$L->Redirect("document_edit.pl?doc_id=$doc_id");
