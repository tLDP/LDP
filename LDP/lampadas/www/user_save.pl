#! /usr/bin/perl
# 
use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

$user_id	= $L->Param('user_id');
$username	= $L->Param('username');
$first_name	= $L->Param('first_name');
$middle_name	= $L->Param('middle_name');
$surname	= $L->Param('surname');
$email		= $L->Param('email');
$admin		= $L->Param('admin');
$admin = 'f' unless ($admin eq 't');
$password	= $L->Param('password');
$notes		= $L->Param('notes');

$DB->Exec("UPDATE username SET username='$username', first_name='$first_name', middle_name='$middle_name', surname='$surname', email='$email', admin='$admin', notes='$notes' WHERE user_id='$user_id'");
if ($password) {
	$DB->Exec("UPDATE username SET password='$password' WHERE user_id='$user_id'");
}

$url = "user_edit.pl?user_id=$user_id";
$L->StartPage("User Saved");
print "The changes have been saved.\n";
$L->EndPage();

