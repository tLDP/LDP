#!/usr/bin/perl
# 
# Used to jump immediately to editing a document by doc_id.
# 
use Lampadas;
$L = new Lampadas;

$doc_id	= $L->Param(doc_id);
$L->Redirect("document_edit.pl?doc_id=$doc_id");
