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
$password	= $L->Param('password');
$notes		= $L->Param('notes');

$L->StartPage("Saving Account Information");
$L->SaveUser($user_id, $username, $first_name, $middle_name, $surname, $email, $admin, $password, $notes);
print "The changes have been saved.\n";
$L->EndPage();

