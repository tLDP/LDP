#! /usr/bin/perl
# 
use Lampadas;
$L = new Lampadas;

$user_id	= $L->Param('user_id');
$username	= $L->Param('username');
$first_name	= $L->Param('first_name');
$middle_name	= $L->Param('middle_name');
$surname	= $L->Param('surname');
$email		= $L->Param('email');
$admin		= $L->Param('admin');
$password	= $L->Param('password');
$notes		= $L->Param('notes');

$L->SaveUser($user_id, $username, $first_name, $middle_name, $surname, $email, $admin, $password, $notes);
$L->Redirect("user_edit.pl?user_id=$user_id");
