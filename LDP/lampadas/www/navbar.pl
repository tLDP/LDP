#!/usr/bin/perl
# 
# Generates a navigation bar suitable for display across the top or bottom of a page.
# 
use CGI qw(:standard);
use Pg;

$dbmain='ldp';
@row;
$query = new CGI;

# connect to the database
$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, first_name, surname FROM username WHERE username='$username'");
@row = $result->fetchrow;
$admin = $row[1];
$firstname = $row[2];
$surname = $row[3];

print "<table class='navbar'><tr>\n";
print "<th><a href='user_edit.pl?username=$username'>$firstname $surname</a></th>\n";
print "<th><a href='/index.html'>Index</a></th>\n";
print "<th><a href='/cgi-bin/document_list.pl'>Documents</a></th>\n ";
print "<th><a href='/cgi-bin/topic_list.pl'>Topics</a></th>\n ";
print "<th><a href='/cgi-bin/maintainer_list.pl'>Maintainers</a></th>\n ";
print "<th><a href='/cgi-bin/editor_list.pl'>Editors</a></th>\n ";
if ($admin) {
	print "<th><a href='/cgi-bin/user_list.pl'>Users</a></th>\n ";
}
print "<th><a href='/cgi-bin/ldp_stats.pl'>Statistics</a></th>\n ";
print "<th><a href='/help/'>Help</a></th>\n ";
print "</tr>\n";
print "</table>\n";
