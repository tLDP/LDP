#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

unless ($L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}
$title			= $L->Param('title');
$class			= $L->Param('class');
$format			= '';
$version		= $L->Param('version');
$last_update		= $L->Param('last_update');
$url			= $L->Param('url');
$isbn			= $L->Param('isbn');
$pub_status		= $L->Param('pub_status');
$review_status		= $L->Param('review_status');
$tickle_date		= $L->Param('tickle_date');
$pub_date		= $L->Param('pub_date');
$ref_url		= $L->Param('ref_url');
$tech_review_status	= $L->Param('tech_review_status');
$maintained		= 'f';
$license		= $L->Param('license');
$abstract		= $L->Param('abstract');
$rating			= 0;
$lang			= $L->Param('lang');

$doc_id = $L->AddDoc(
	$title, 
	$class, 
	$format, 
	$version, 
	$last_update, 
	$url,
	$isbn,
	$pub_status,
	$review_status,
	$tickle_date,
	$pub_date,
	$ref_url,
	$tech_review_status,
	$maintained,
	$license,
	$abstract,
	$rating,
	$lang
);

$L->Redirect("document_edit.pl?doc_id=$doc_id");

