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
if ($username ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}

$result=$conn->exec("SELECT username, first_name, surname, maintainer_id, email, admin, editor_id FROM username ORDER BY surname, first_name");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

# print the page
print header(-expires=>'now');
print "<html><head><title>LDP Database Users</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>";
print "</head>";
print "<body>";

print "<h1>LDP Database Users</h1>\n";

system("./navbar.pl");

print "<p><table border=0>\n";
print"<tr><th>Username</th>\n";
print "<th>First Name</th>\n";
print "<th>Surname</th>\n";
print "<th>Email</th>\n";
print "<th>Maintainer</th>\n";
print "<th>Editor</th>\n";
print "<th>Admin</th></tr>\n";
while (@row = $result->fetchrow) {
  $username = $row[0];
  $first_name = $row[1];
  $surname = $row[2];
  $maintainer_id = $row[3];
  $email = $row[4];
  $admin = $row[5];
  $editor_id = $row[6];
  print "<tr><td>" . a({href=>"user_edit.pl?username=$username"},"$username") . "</td>";
  print "<td>$first_name</td>\n";
  print "<td>$surname</td>\n";
  print "<td>$email</td>\n";
  print "<td>$maintainer_id</td>\n";
  print "<td>$editor_id</td>\n";
  print "<td>$admin</td>\n";
  print "</tr>";
  $count++;
}
print "</table>\n";

print "<p>Count: $count";

print "<p><hr>\n";

print "<h1>New User</h1>\n";

print "<p><form method=POST action='user_add.pl'>\n";
print "<input type=hidden name=caller value='user_list.pl'>\n";
print "<table>\n";
print "<tr><td align=right>Name:</td><td><input type=text name=username width=20 size=20></td></tr>\n";
print "<tr><td align=right>Email:</td><td><input type=text name=email width=20 size=20></td></tr>\n";
print "<tr><td></td><td><input type=submit value=Save></td></tr>\n";
print "</table></form>\n";

print end_html;

