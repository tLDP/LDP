#! /usr/bin/perl

use Lampadas;
$L = new Lampadas;

$username	= $L->Param('username');
$first_name	= $L->Param('first_name');
$middle_name	= $L->Param('middle_name');
$surname	= $L->Param('surname');
$email		= $L->Param('email');
$admin		= $L->Param('admin');
$sysadmin	= $L->Param('sysadmin');

$message = $L->AddUser($username, $first_name, $middle_name, $surname, $email, $admin, $sysadmin, '');
$L->StartPage("Creating New Account");
print $message;
$L->EndPage();
