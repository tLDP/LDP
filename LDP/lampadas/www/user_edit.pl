#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$username = param('username');

# Load data from db and call edit form
$conn=Pg::connectdb("dbname=$dbmain");

$realusername = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$realusername'");
@row = $result->fetchrow;
$founduser = $row[0];
$founduser =~ s/\s+$//;
if ($realusername ne $founduser) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}


$result = $conn->exec("SELECT username, first_name, surname, maintainer_id, email, admin, editor_id FROM username WHERE username='$username'");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

@row = $result->fetchrow;

# Load from db
$first_name = $row[1];
$first_name =~ s/^\s+//;
$first_name =~ s/\s+$//;
$surname = $row[2];
$surname =~ s/^\s+//;
$surname =~ s/\s+$//;
$maintainer_id = $row[3];
$email = $row[4];
$admin = $row[5];
$editor_id = $row[6];

print header(-expires=>'now');

print "<html><head><title>$first_name $surname</title>";
print "<link rel=stylesheet href='../ldp.css' type='text/css'></head>";
print "<body>";

print "<h1>$first_name $surname</h1>\n";

system("./navbar.pl");

print "<p>Username: $username";
print "<form name=edit method=POST action='user_save.pl'>";
print "<input type=hidden name=username value=$username></input>";
printf "<p><table>\n";
print '<tr><th>Name:</th><td><input type=text name="first_name" size=30 value="' . $first_name . '"></input><input type=text name="surname" size=30 value="' . $surname . '"></input></td></tr>';
print '<tr><th>Email:</th><td><input type=text name="email" size=30 value="' . $email . '"></input></td></tr>';
print '<tr><th>Admin (t/f):</th><td><input type=text name="admin" size=1 value="' . $admin . '"></input></td></tr>';
print '<tr><th>Maintainer ID:</th><td><input type=text name="maintainer_id" size=4 value="' . $maintainer_id . '"></input></td></tr>';
print '<tr><th>Editor ID:</th><td><input type=text name="editor_id" size=4 value="' . $editor_id . '"></input></td></tr>';
print '<tr><th>New Password:</th><td><input type=text name="password" size=12></input></td></tr>';
print "<tr><td></td><td><input type=submit value=Save></td></tr>";
print "</table>";
print "</form>";

print end_html;

