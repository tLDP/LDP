#! /usr/bin/perl
# 
use CGI qw(:standard);
$CGI = new CGI;

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

# Read parameters
$user_id	= param('user_id');
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
$admin		= param('admin');
$admin = 'f' unless ($admin eq 't');
$password	= param('password');
$password	=~ s/\s+$//;


$DB->Exec("UPDATE username SET username='$username', first_name='$first_name', middle_name='$middle_name', surname='$surname', email='$email', admin='$admin' WHERE user_id='$user_id'");
if ($password) {
	$DB->Exec("UPDATE username SET password='$password' WHERE user_id='$user_id'");
}

$url = "user_edit.pl?user_id=$user_id";
$L->StartPage("User Saved");
print "The changes have been saved.\n";
$L->EndPage();

