#! /usr/bin/perl

use CGI qw(:standard);
use Pg;
use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$username	= param('username');
$username	=~ s/\s+$//;
$first_name	= param('first_name');
$first_name	=~ s/\s+$//;
$middle_name	= param('middle_name');
$middle_name	=~ s/\s+$//;
$surname	= param('surname');
$surname	=~ s/\s+$//;
$email		= param('email');
$email		=~ s/\s+$//;

$conn=Pg::connectdb("dbname=$dbmain");

if ($username and $email) {
	@row = $DB->Row("SELECT COUNT(*) FROM username WHERE username='$username'");
	$count = $row[0];
	if ($count) {
		$L->StartPage('Duplicate Username');
		print "<p>The username you requested, '$username', is already taken.\n";
	} else {
		$sql = "SELECT COUNT(*) FROM username WHERE email='$email'";
		@row = $DB->Row($sql);
		$count = $row[0];
		if ($count) {
			$L->StartPage('Duplicate Email');
			print "<p>There is already an account using your email address.\n";
		} else {
			my %newuser = $L->NewUser($username, $first_name, $middle_name, $surname, $email, 'f', $password);
			if ($newuser{username} eq $username) {
				$L->StartPage('New Account Created');
				print "<p>Your account has been created.\n";
				print "<p>Your password has been mailed to your email address,\n";
				print "and you can use it to log in.\n";
				print "Once you log in for the first time,\n";
				print "you can change your password.\n";
			} else {
				$L->StartPage('Error Creating Account');
				print "<p>There was an error creating your account.\n";
				print "Please try again, and if the problem persists, notify the webmaster.\n";
			}
		}
	}
} else {
	$L->StartPage('Missing Information');
	print "<p>You didn't fill out all of the fields in the form.\n";
}

$L->EndPage();
