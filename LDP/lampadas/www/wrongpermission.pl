#! /usr/bin/perl
# 
# User does not have enough permission
#
use Lampadas;
$L = new Lampadas;

$L->StartPage('Insufficient Permissions');
print "<p>You do not have permission to do that.";
$L->EndPage;
