#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller          = param('caller');
$maintainer_name = param('maintainer_name');
$maintainer_name =~ s/\'/\'\'/;
$email           = param('email');

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

$sql = "SELECT max(maintainer_id) from maintainer";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$maintainer_id = $row[0] + 1;

$sql = "INSERT INTO maintainer(maintainer_id, maintainer_name, email) VALUES ($maintainer_id, '$maintainer_name', '$email')";
$conn->exec($sql);

#print header;
#print start_html;
#print "<p>$maintainer_name";
#print "<p>$email";
#print "<p>$maintainer_id";
#print "<p>$sql";
#print end_html;
#exit;


print $query->redirect($caller)

