#!/usr/bin/perl

use CGI qw(:standard);
use Pg;

$dbmain='ldp';
@row;
$count = 0;

$query = new CGI;

# Connect to the database
$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
$admin = $row[1];

$result=$conn->exec("SELECT maintainer_id, maintainer_name, email FROM maintainer ORDER BY maintainer_name");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

# print the page
print header(-expires=>'now');
print "<html><head><title>LDP Maintainers</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
print "</head>";
print "<body>";

print "<h1>LDP Maintainers</h1>\n";

system("./navbar.pl");

print "<p><table border=0>\n";
print "<tr><th>Name</th><th>Email</th></tr>\n";
while (@row = $result->fetchrow) {
  $maintainer_id = $row[0];
  $maintainer_name = $row[1];
  if ( $maintainer_name eq "" ) { $maintainer_name = 'J. Doe' }
  $email = $row[2];
  print "<tr><td>";
  print a({href=>"maintainer_edit.pl?maintainer_id=$maintainer_id"},"$maintainer_name");
  print "</td><td>\n";
  if ( $email ) { print a({href=>"mailto:$email"}, "$email") }
  print "</td>";
  print "</tr>";
  $count++;
}
print "</table>\n";

print "<p>Count: $count";

if ($admin eq 't') {
	print "<p><hr>\n";

	print "<h1>New Maintainer</h1>\n";

	print "<p><form method=POST action='maintainer_add.pl'>\n";
	print "<input type=hidden name=caller value='maintainer_list.pl'>\n";
	print "<table>\n";
	print "<tr><td align=right>Name:</td><td><input type=text name=maintainer_name width=20 size=20></td></tr>\n";
	print "<tr><td align=right>Email:</td><td><input type=text name=email width=20 size=20></td></tr>\n";
	print "<tr><td></td><td><input type=submit value=Save></td></tr>\n";
	print "</table></form>\n";
}

print end_html;

