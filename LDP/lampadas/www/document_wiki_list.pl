#! /usr/bin/perl

use Lampadas;
use Lampadas::Database;

$L = new Lampadas;
$DB = new Lampadas::Database;

$doc_id       = $L->Param('doc_id');
%doc = $L->Doc($doc_id);

$L->StartPage("Editing History of " . $doc{title});

print "<a href='document_edit.pl?doc_id=$doc{id}'>Meta-Data</a>\n";
print "&nbsp;|&nbsp;";
print "<a href='document_wiki.pl?doc_id=$doc{id}'>Edit</a>\n";

print "<p><table class='box'>\n";
print "<tr><th align=right>Revision</th><th>Saved</th><th>Comment</th><th>User</th></tr>\n";
$sql = "SELECT revision, date_entered, wiki, notes, user_id FROM document_wiki WHERE doc_id = $doc_id ORDER BY revision DESC LIMIT 10, 0";
$result = $DB->Recordset($sql);
while (@row = $result->fetchrow) {
	$revision	= $row[0];
	$date_entered	= $row[1];
	$wiki		= $row[2];
	$wiki		=~  s/\s+$//;
	$notes		= $row[3];
	$user_id	= $row[4];

	print "<tr><td align=right>$revision</td>\n";
	print "<td>$date_entered</td>\n";
	print "<td>$notes</td>\n";
	print "<td>$user_id</td></tr>\n";
}
print "</table>\n";

$L->EndPage();
