#! /usr/bin/perl
# 
# Create a new user account
#
use Lampadas;

$L = new Lampadas;

$L->StartPage('Create New User Account');

print "<p>Welcome to the " . $L->Config('owner') . " Lampadas system.\n";

print "<p>To create a new user account, fill out this form.\n";

print "<p><form name='newuser' action='createuser.pl' method='POST'>\n";
print "<table>\n";
print "<tr>\n";
print "<td align=right>*Username</td>\n";
print "<td><input type=text name=username size=20></input></td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td align=right>*Enter your email address.<br>Your password will be mailed to this address, so it must be valid.</td>\n";
print "<td><input type=text name=email size=20></input></td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td align=right>First Name</td>\n";
print "<td><input type=text name=first_name size=20></input></td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td align=right>Middle Name</td>\n";
print "<td><input type=text name=middle_name size=20></input></td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td align=right>Surname</td>\n";
print "<td><input type=text name=surname size=20></input></td>\n";
print "</tr>\n";
print "<tr>\n";
print "<td></td><td><input type=submit value='Create Account!'></td>\n";
print "</tr>\n";
print "</table\n";
print "</form>\n";

print "<p>*Required Fields\n";

$L->EndPage()
