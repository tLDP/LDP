#! /usr/bin/perl

use Pg;

$dbmain = "ldp";
@row;

# Read parameters
$doc_id = $ARGV[0];

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$result = $conn->exec("SELECT wiki FROM document_wiki WHERE doc_id = $doc_id ORDER BY revision DESC LIMIT 1, 0");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$wiki		= $row[0];
$wiki		=~  s/\s+$//;

print $wiki;
