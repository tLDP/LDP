#!/usr/bin/perl

use CGI qw(:standard);
use Pg;

$dbmain='ldp';
@row;
$count = 0;

# Connect and load the tuples
$conn=Pg::connectdb("dbname=$dbmain");
$result=$conn->exec("SELECT volunteer_id, name, email, role FROM volunteer ORDER BY name");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

# print the page
print header(-expires=>'now');
print "<html><head><title>LDP Volunteers</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
print "</head>";
print "<body>";

print "<h1>LDP Maintainers</h1>\n";

system("./navbar.pl");

print "<p><table border=0>\n";
while (@row = $result->fetchrow) {
  $volunteer_id = $row[0];
  $name = $row[1];
  $email = $row[2];
  $role = $row[3];
  print "<tr><td>";
  print a({href=>"volunteer_edit.pl?volunteer_id=$volunteer_id"},"$name");
  print "</td><td>\n";
  if ( $email ) { print a({href=>"mailto:$email"}, "$email") }
  print "</td><td>\n";
  print "$role\n";
  print "</td>";
  print "</tr>";
  $count++;
}
print "</table>\n";

print "<p>Count: $count";

print end_html;

