#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$dbmain = "ldp";
@row;
$query = new CGI;

# Read parameters
$doc_id       = param('doc_id');

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$result = $conn->exec("SELECT url FROM document WHERE doc_id=$doc_id");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;

# Load from db
$url = $row[0] =~ s/\s+$//;

print $query->redirect("$url");
