#!/usr/bin/perl

use CGI qw(:standard);
use Pg;
use Lampadas;

$L = new Lampadas;

$dbmain='ldp';
@row;
$count = 0;

$query = new CGI;

# Connect to database
$conn=Pg::connectdb("dbname=$dbmain");

$admin = $L->Admin();
$currentuser_id = $L->CurrentUserID();

unless ($L->Admin()) {
	print $query->redirect("wrongpermission.pl");
	exit;
}

$result=$conn->exec("SELECT user_id, username, first_name, middle_name, surname, email, admin FROM username ORDER BY username");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

$L->StartPage('Lampadas Users');

print "<p><table border=0>\n";
print"<tr><th>Username</th>\n";
print "<th>First Name</th>\n";
print "<th>Middle Name</th>\n";
print "<th>Surname</th>\n";
print "<th>Email</th>\n";
print "<th>Admin</th></tr>\n";
while (@row = $result->fetchrow) {
	$user_id = $row[0];
	$username = $row[1];
	$username =~ s/\s+$//;
	$first_name = $row[2];
	$middle_name = $row[3];
	$surname = $row[4];
	$email = $row[5];
	$admin = $row[6];
	print "<tr><td>" . a({href=>"user_edit.pl?user_id=$user_id"},"$username") . "</td>";
	print "<td>$first_name</td>\n";
	print "<td>$middle_name</td>\n";
	print "<td>$surname</td>\n";
	print "<td>$email</td>\n";
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
print "<tr><td align=right>Username:</td><td><input type=text name=username width=20 size=20></td></tr>\n";
print "<tr><td align=right>First Name:</td><td><input type=text name=first_name width=20 size=20></td></tr>\n";
print "<tr><td align=right>Middle Name:</td><td><input type=text name=middle_name width=20 size=20></td></tr>\n";
print "<tr><td align=right>Surname:</td><td><input type=text name=surrname width=20 size=20></td></tr>\n";
print "<tr><td align=right>Email:</td><td><input type=text name=email width=20 size=20></td></tr>\n";
print "<tr><td align=right>Admin:</td><td><select name=admin><option value='t'>Yes</option><option selected value='f'>No</option></select></td></tr>\n";
print "<tr><td></td><td><input type=submit value=Save></td></tr>\n";
print "</table></form>\n";

$L->EndPage();

