#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;

# Read parameters
$name = param('name');

print "Content-Type: text/plain; charset=ISO-8859-1\n\n";

$cmd = "/home/david/ldp/cvs/LDP/database/xml.pl -n $name";
system("$cmd");

