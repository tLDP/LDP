#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$name = param('name');
$name = uc($name);

$conn=Pg::connectdb("dbname=$dbmain");
die $conn->errorMessage unless PGRES_CONNECTION_OK eq $conn->status;

$result = $conn->exec("SELECT url FROM document WHERE UPPER(filename)='$name' AND pub_status='N'");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;
$url           = $row[0];

print "Content-Type: text/plain; charset=ISO-8859-1\n\n";
if ($url eq '') {
	print "ERROR: did not find $name";
} else {
	print $url;
}

exit;

print header(-expires=>'now');
print "<html><head><title>$title</title>";
print "<body>";
if ($url eq '') {
	print "ERROR: did not find $name";
} else {
	print $url;
}
print "</body></html>";



