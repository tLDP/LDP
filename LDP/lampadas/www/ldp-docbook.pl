#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

# Read parameters
$doc_id = param('doc_id');

print "Content-Type: text/plain; charset=ISO-8859-1\n\n";

$cmd = "/home/david/ldp/cvs/LDP/database/ldp-docbook.pl $doc_id";
system("$cmd");

