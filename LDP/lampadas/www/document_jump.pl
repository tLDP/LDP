#!/usr/bin/perl
# 
# Used to jump immediately to editing a document by doc_id.
# Only available for Administrators and Maintainers.
# 
use Lampadas;
$L = new Lampadas;

unless ($L->Maintainer()) or $L->Admin()) {
	$L->Redirect("wrongpermission.pl");
}

# Read parameters
$doc_id	= $L->Param(doc_id);
$L->Redirect("document_edit.pl?doc_id=$doc_id");


# Holding onto this just in case I discover something was using it.
# But I don't think so. :-)
# 
#$conn=Pg::connectdb("dbname=$dbmain");
#die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;
#
#$result = $conn->exec("SELECT url FROM document WHERE doc_id=$doc_id");
#die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
#
#@row = $result->fetchrow;
#
## Load from db
#$url = $row[0] =~ s/\s+$//;
#
#print $query->redirect("$url");
