#! /usr/bin/perl
# 
# Create a new user account
#
use Lampadas;
$L = new Lampadas;

$L->StartPage('Create New User Account');
print $L->NewUserTable();
$L->EndPage()
