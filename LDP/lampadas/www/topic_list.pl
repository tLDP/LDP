#!/usr/bin/perl

use CGI qw(:standard);
use Pg;

$dbmain='ldp';
@row;
$last_topic_num = 0;
$last_subtopic_num = 0;

# Connect and load the tuples
$conn=Pg::connectdb("dbname=$dbmain");
$sql = "SELECT topic.topic_num, topic.topic_name, subtopic.subtopic_num, subtopic.subtopic_name, document.doc_id, document.title, topic_description, subtopic_description FROM topic, subtopic, document_topic, document WHERE topic.topic_num = subtopic.topic_num and topic.topic_num = document_topic.topic_num and subtopic.subtopic_num = document_topic.subtopic_num and document_topic.doc_id = document.doc_id ORDER BY topic_num, subtopic_num, title";

$result=$conn->exec("$sql");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

# print the page
#print header(-expires=>'now');
print header;
print "<html><head>\n";
print "<title>LDP Document Database</title>\n";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>\n";
print "</head>\n";
print "<body>\n";

print "<h1>Topic Listing</h1>\n";

print "<p><a href='../index.html'>Index</a> \n";
print "<a href='document_list.pl'>Documents</a> \n";
print "<a href='maintainer_list.pl'>Maintainers</a>\n";
print "<a href='editor_list.pl'>Editors</a>\n";

while (@row = $result->fetchrow) {
  $topic_num            = $row[0];
  $topic_name           = $row[1];
  $subtopic_num         = $row[2];
  $subtopic_name        = $row[3];
  $doc_id               = $row[4];
  $title                = $row[5];
  $topic_description    = $row[6];
  $subtopic_description = $row[7];

  if ( $topic_num != $last_topic_num ) {
    print "<p><hr>";
    print "<h1>$topic_num $topic_name</h1>\n";
    print "<blockquote>$topic_description</blockquote>\n";
  }
  if ( $subtopic_num != $last_subtopic_num ) {
    print "<h2>$topic_num.$subtopic_num $subtopic_name</h2>\n";
    print "<blockquote>$subtopic_description</blockquote>\n";
  }
  print a({href=>"document_edit.pl?doc_id=$doc_id"},"$title");
  print "<br>\n";

  $last_topic_num = $topic_num;
  $last_subtopic_num = $subtopic_num;
}

print end_html;

