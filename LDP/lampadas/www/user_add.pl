#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$username	= param('username');
$first_name	= param('first_name');
$surname	= param('surname');
$maintainer_id	= param('maintainer_id');
$email		= param('email');
$admin		= param('admin');
$editor_id	= param('editor_id');
$password	= param('password');

$conn=Pg::connectdb("dbname=$dbmain");

$realusername = $query->remote_user();
$result=$conn->exec("SELECT username, admin FROM username WHERE username='$realusername'");
@row = $result->fetchrow;
if ($realusername ne $row[0]) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		print $query->redirect("../wrongpermission.html");
		exit;
	}
}

$sql = "INSERT INTO username (username, email) VALUES ('$username', '$email')";
$result=$conn->exec($sql);

print $query->redirect("user_edit.pl?username=$username");
