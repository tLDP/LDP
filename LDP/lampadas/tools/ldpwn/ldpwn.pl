#!/usr/bin/perl

use CGI qw(:standard);
use Pg;

$baseurl = "http://www.linuxdoc.org";
$basesql = "SELECT doc_id, title, class, url, version, format FROM document ";
$dbmain='ldp';
@row;
$pubdate1 = $ARGV[0];
$pubdate2 = $ARGV[1];

$conn=Pg::connectdb("dbname=$dbmain");

#Determine the tuples to load
$sql = $basesql . "WHERE pub_status = 'N' AND pub_date >= '$pubdate1' AND pub_date <= '$pubdate2' ORDER BY title";

# Connect and load the tuples
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

print h2('New Documents');
printf "\n\n";
printf "<ul>\n";

while (@row = $result->fetchrow) {
  read_document(@row);
  print_document();
}
printf "</ul>\n\n";
print h2('Updated Documents');
printf "\n\n";
printf "<ul>\n";


$sql = $basesql . "WHERE pub_status = 'N' AND pub_date < '$pubdate1' AND last_update >= '$pubdate1' AND last_update <= '$pubdate2' ORDER BY title";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

while (@row = $result->fetchrow) {
  read_document (@row);
  print_document();
}
printf "</ul>\n\n";








sub read_document (@row) {
  $doc_id = $row[0];
  $title = $row[1];
  $class = $row[2];
  $class =~ s/\s*$//;
  $refurl = $row[3];
  $version = $row[4];
  $version =~ s/\s*$//;
  $format = $row[5];
  $format =~ s/\s*$//;
  $url = $refurl;
}

sub print_document() {
  print "<p><li><b>";
  print $title;
  printf "</b><br>\n";
  print a({href=>$url},$url);
  print br;
  printf "\n";
  print "Version " . $version;

  $sql = "SELECT maintainer_name, document_maintainer.email FROM document_maintainer, maintainer where document_maintainer.doc_id = " . $doc_id . " AND document_maintainer.maintainer_id = maintainer.maintainer_id AND active AND role = 'Author' ORDER BY maintainer_name";
  $author_result=$conn->exec($sql);
  die $conn->errorMessage unless PGRES_TUPLES_OK eq $author_result->resultStatus;
  while (@author_row = $author_result->fetchrow) {
    read_author ();
    print_author();
  }
  
  printf "\n\n";
}

sub read_author() {
  $author = $author_row[0];
  $email = $author_row[1];
}

sub print_author() {
  print ", " . $author;
  if (not ($email eq "")) {
    print ", ";
    print a({href=>"mailto:" . $email}, $email);
  }
}
