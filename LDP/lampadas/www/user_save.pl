#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$username	= param('username');
$username	=~ s/^\s+//;
$username	=~ s/\s+$//;
$first_name	= param('first_name');
$first_name	=~ s/^\s+//;
$firstname	=~ s/\s+$//;
$surname	= param('surname');
$surname	=~ s/^\s+//;
$surname	=~ s/\s+$//;
$maintainer_id	= param('maintainer_id');
$maintainer_id = 0 unless ($maintainer_id);
$email		= param('email');
$email		=~ s/^\s+//;
$email		=~ s/\s+$//;
$admin		= param('admin');
$admin = 'f' unless ($admin eq 't');
$editor_id	= param('editor_id');
$editor_id = 0 unless ($editor_id);
$password	= param('password');
$password	=~ s/^\s+//;
$password	=~ s/\s+$//;


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

$sql = "UPDATE username SET first_name = '$first_name', surname='$surname', maintainer_id=$maintainer_id, email='$email', admin='$admin', editor_id=$editor_id WHERE username='$username'";
$result=$conn->exec($sql);

if ($password) {
	$cmd = "htpasswd -b /var/www/htpasswd-gldp $username $password >> /var/www/htpasswd.log";
	system($cmd);
}

#print header;
#print start_html;
#print $sql;
#print end_html;
#exit;

print $query->redirect("user_edit.pl?username=$username");
