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
print $L->UsersTable();

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

