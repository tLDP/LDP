#!/usr/bin/perl

use CGI qw(:standard);
use Pg;
use Date::Calc qw(:all);

$baseurl = "http://www.linuxdoc.org";
$basesql = "SELECT doc_id, title, class, ref_url, version, format FROM document ";
$dbmain='ldp';


$conn=Pg::connectdb("dbname=$dbmain");

print header;

print "<html><head><title>LDP Statistics</title><link rel=stylesheet href='/ldp.css' type='text/css'>";
print "<body>";

print "<h2>Statistics</h2>\n\n";

$sql = "select count(*) from document";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$document_total = $row[0];


$sql = "select count(*) from document where pub_status = 'N'";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
@row = $result->fetchrow;
$document_count = $row[0];


print "<h3>Status</h3>";
print "\n\n";
$sql = "select pub_status_name, count(*) from pub_status, document where pub_status.pub_status = document.pub_status group by pub_status_name";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Status</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<td>" . $row[0] . "</td>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_total * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><td>Total</td><td align=right>$total</td></tr>";
print "</table>\n";

print "<p>Only documents marked &quot;Active&quot; are represented in the following statistics.\n";


print "<p><hr>";

print "<h3>License</h3>";
print "\n\n";
$sql = "select license, count(*) FROM document where pub_status = 'N' group by license";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
$free_count = 0;
$nonfree_count = 0;
$unknown_count = 0;
print "<table>\n";
print "<tr><th>License</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  $license = $row[0];
  $license =~ s/\s+$//;
  $count   = $row[1];
  print "<tr>\n";
  print "<td>$license</td>\n";
  print "<td align=right>$count</td>\n";
  $pct = sprintf( '%3.2f', $count / $document_count * 100 );
  print "<td align=right>$pct%</td>\n";
  print "</tr>\n";
  $total = $total + $count;

  if ( $license eq "GFDL" || $license eq "GPL" || $license eq "OPL" || $license eq "PD" ) {
    $free_count += $count;
  }
  elsif ( $license eq "" ) {
    $unknown_count += $count;
  }
  else {
    $nonfree_count += $count;
  }
}
print "<tr><td>Total</td><td align=right>$total</td></tr>";
print "</table>\n";

$free_pct = sprintf( '%3.2f', $free_count / $total * 100 );
$nonfree_pct = sprintf( '%3.2f', $nonfree_count / $total * 100 );
$unknown_pct = sprintf( '%3.2f', $unknown_count / $total * 100 );

print "<p><table>\n";
print "<tr><th>Type</th><th align=right>Count</th><th align=right>Percent</th></tr>\n";
print "<tr><td>Free</td><td align=right>$free_count</td><td align=right>$free_pct</td></tr>\n";
print "<tr><td>Non-Free</td><td align=right>$nonfree_count</td><td align=right>$nonfree_pct</td></tr>\n";
print "<tr><td>Unknown</td><td align=right>$unknown_count</td><td align=right>$unknown_pct</td></tr>\n";
print "<tr><td>Total</td><td align=right>$total</td></tr>";
print "</table>\n";


print "<p><hr>";

print "<h3>Class</h3>";
print "\n\n";
$sql = "select class_name, count(*) from class, document where pub_status = 'N' and class.class = document.class group by class_name";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Class</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<td>" . $row[0] . "</td>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><td>Total</td><td align=right>" . $total . "</td></tr>";
print "</table>\n";


print "<p><hr>";

print "<h3>Format</h3>";
print "\n\n";
$sql = "select format, count(*) from document where pub_status = 'N' group by format";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Format</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<td>" . $row[0] . "</td>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><td>Total</td><td align=right>" . $total . "</td></tr>";
print "</table>\n";


print "<p><hr>";

print "<h3>DTD</h3>";
print "\n\n";
$sql = "select dtd, count(*) from document where pub_status = 'N' group by dtd";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>DTD</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<td>" . $row[0] . "</td>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><td>Total</td><td align=right>" . $total . "</td></tr>";
print "</table>\n";

print "<p><hr>";

print "<h3>Format and DTD</h3>";
print "\n\n";
$sql = "select format, dtd, count(*) from document where pub_status = 'N' group by format, dtd";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Format</th><th>DTD</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  $format = $row[0];
  $dtd    = $row[1];
  $count  = $row[2];
  $pct = sprintf( '%3.2f', $count / $document_count * 100 );
  print "<tr>\n";
  print "<td>$format</td>\n";
  print "<td>$dtd</td>\n";
  print "<td align=right>$count</td>\n";
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $count;
}
print "<tr><td>Total</td><td></td><td align=right>" . $total . "</td></tr>";
print "</table>\n";

print "<p><hr>";

print "<h3>Details</h3>";
$sql = "select class, dtd, format, count(*) from document where pub_status = 'N' group by class, dtd, format";

$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

$total = 0;
print "<table>\n";
print "<tr><th>Class</th><th>DTD</th><th>Format</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<td>" . $row[0] . "</td>\n";
  print "<td>" . $row[1] . "</td>\n";
  print "<td>" . $row[2] . "</td>\n";
  print "<td align=right>" . $row[3] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[3] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[3];
}
print "<tr><td>Total</td><td></td><td></td><td align=right>" . $total . "</td></tr>";
print "</table>\n";




print "<p><hr>\n";

print "<h3>Miscellaneous Statistics</h3>\n";
$sql = "select last_update from document where pub_status='N'";

$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

$count = 0;
$avg_age   = 0;
($year2, $month2, $day2) = Today();
while (@row = $result->fetchrow) {

  $last_update = $row[0];
  if (($last_update != "") && ($last_update != "1970-01-01" )) {
    $year1 = substr($last_update,0,4);
    $month1 = substr($last_update,5,2);
    $day1 = substr($last_update,8,2);
    $age = Delta_Days($year1, $month1, $day1, $year2, $month2, $day2);
    if ( $count > 0 ) {
      $avg_age = (($avg_age * ($count - 1)) + $age) / $count;
    }
    else {
      $avg_age = $age;
    }

    $count++;
  }
}


print "<table>\n";
print "<tr><th>Statistic</th><th>Value</th></tr>";
print "<tr><td>Average Age Since Last Update</td><td>&nbsp;";
printf "%i", $avg_age;
print " days</td></tr>";
print "</table>\n";




print end_html;




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
  $url = $baseurl . $refurl;
}

sub print_document() {
  print "<p><li><b>";
  print $title;
  print "</b><br>\n";
  print a({href=>$url},$url);
  print br;
  print "\n";
  print "Version " . $version;

  $sql = "SELECT maintainer_name, document_maintainer.email FROM document_maintainer, maintainer where document_maintainer.doc_id = " . $doc_id . " AND document_maintainer.maintainer_id = maintainer.maintainer_id AND active AND role = 'Author' ORDER BY maintainer_name";
  $author_result=$conn->exec($sql);
  die $conn->errorMessage unless PGRES_TUPLES_OK eq $author_result->resultStatus;
  while (@author_row = $author_result->fetchrow) {
    read_author ();
    print_author();
  }
  
  print "\n\n";
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
