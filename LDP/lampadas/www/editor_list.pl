#!/usr/bin/perl

use CGI qw(:standard);
use Pg;

$dbmain='ldp';
@row;
$count = 0;

$query = new CGI;

# Connect to database
$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
$admin = $row[1];

$result=$conn->exec("SELECT editor_id, editor_name, email FROM editor ORDER BY editor_name");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

# print the page
print header(-expires=>'now');
print "<html><head><title>LDP Editors</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
print "</head>";
print "<body>";

print "<h1>LDP Editors</h1>\n";

system("./navbar.pl");

print "<p><table border=0>\n";
while (@row = $result->fetchrow) {
  $editor_id = $row[0];
  $editor_name = $row[1];
  if ( $editor_name eq "" ) { $editor_name = 'J. Doe' }
  $email = $row[2];
  print "<tr><td>";
  print a({href=>"editor_edit.pl?editor_id=$editor_id"},"$editor_name");
  print "</td>";
  print "</tr>";
  $count++;
}
print "</table>\n";

print "<p>Count: $count";

if ($admin eq 't') {
	print "<p><hr>\n";

	print "<h1>New Editor</h1>\n";

	print "<p><form method=POST action='editor_add.pl'>\n";
	print "<input type=hidden name=caller value='editor_list.pl'>\n";
	print "<table>\n";
	print "<tr><td align=right>Name:</td><td><input type=text name=editor_name width=20 size=20></td></tr>\n";
	print "<tr><td align=right>Email:</td><td><input type=text name=email width=20 size=20></td></tr>\n";
	print "<tr><td></td><td><input type=submit value=Save></td></tr>\n";
	print "</table></form>\n";
}

print end_html;

