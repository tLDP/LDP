#!/usr/bin/perl

use CGI qw(:standard);
use Pg;
use Date::Calc qw(:all);
use Lampadas;

$L = new Lampadas;

$baseurl = "http://www.linuxdoc.org";
$basesql = "SELECT doc_id, title, class, ref_url, version, format FROM document ";
$dbmain='ldp';

$conn=Pg::connectdb("dbname=$dbmain");

$L->StartPage('Statistics');

$document_total = $L->DocCount();
$document_count = $L->DocCountByPubStatus("'N'");


print "<h2>Status</h3>";
print "\n\n";
$sql = "select pub_status_name, count(*) from pub_status, document where pub_status.pub_status = document.pub_status group by pub_status_name";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Status</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<th>" . $row[0] . "</th>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_total * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><th>Total</th><td align=right>$total</td></tr>";
print "</table>\n";

print "<p>Only documents marked &quot;Active&quot; are represented in the following statistics.\n";


print "<p><hr>";

print "<h2>License</h3>";
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
  print "<th>$license</th>\n";
  print "<td align=right>$count</td>\n";
  $pct = sprintf( '%3.2f', $count / $document_count * 100 );
  print "<td align=right>$pct%</td>\n";
  print "</tr>\n";
  $total = $total + $count;

  if ( $license eq "GFDL" || $license eq "GPL" || $license eq "OPL" || $license eq "LDPL" || $license eq "PD" ) {
    $free_count += $count;
  }
  elsif ( $license eq "" ) {
    $unknown_count += $count;
  }
  else {
    $nonfree_count += $count;
  }
}
print "<tr><th>Total</th><td align=right>$total</td></tr>";
print "</table>\n";

$free_pct = sprintf( '%3.2f', $free_count / $total * 100 );
$nonfree_pct = sprintf( '%3.2f', $nonfree_count / $total * 100 );
$unknown_pct = sprintf( '%3.2f', $unknown_count / $total * 100 );

print "<p><table>\n";
print "<tr><th>Type</th><th align=right>Count</th><th align=right>Percent</th></tr>\n";
print "<tr><th>Free*</th><td align=right>$free_count</td><td align=right>$free_pct</td></tr>\n";
print "<tr><th>Non-Free</th><td align=right>$nonfree_count</td><td align=right>$nonfree_pct</td></tr>\n";
print "<tr><th>Unknown</th><td align=right>$unknown_count</td><td align=right>$unknown_pct</td></tr>\n";
print "<tr><th>Total</th><td align=right>$total</td></tr>";
print "</table>\n";

print "<p>*Free licenses include GFDL, GPL, OPL, and PD.\n";

print "<p><hr>";

print "<h2>Class</h3>";
print "\n\n";
$sql = "select class_name, count(*) from class, document where pub_status = 'N' and class.class = document.class group by class_name";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Class</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<th>" . $row[0] . "</th>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><th>Total</th><td align=right>" . $total . "</td></tr>";
print "</table>\n";


print "<p><hr>";

print "<h2>Format</h3>";
print "\n\n";
$sql = "select format, count(*) from document where pub_status = 'N' group by format";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>Format</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<th>" . $row[0] . "</th>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><th>Total</th><td align=right>" . $total . "</td></tr>";
print "</table>\n";


print "<p><hr>";

print "<h2>DTD</h3>";
print "\n\n";
$sql = "select dtd, count(*) from document where pub_status = 'N' group by dtd";
$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;
$total = 0;
print "<table>\n";
print "<tr><th>DTD</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<th>" . $row[0] . "</th>\n";
  print "<td align=right>" . $row[1] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[1] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[1];
}
print "<tr><th>Total</th><td align=right>" . $total . "</td></tr>";
print "</table>\n";

print "<p><hr>";

print "<h2>Format and DTD</h3>";
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
  print "<th>$format</th>\n";
  print "<th>$dtd</th>\n";
  print "<td align=right>$count</td>\n";
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $count;
}
print "<tr><th>Total</th><td></td><td align=right>" . $total . "</td></tr>";
print "</table>\n";

print "<p><hr>";

print "<h2>Details</h3>";
$sql = "select class, dtd, format, count(*) from document where pub_status = 'N' group by class, dtd, format";

$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

$total = 0;
print "<table>\n";
print "<tr><th>Class</th><th>DTD</th><th>Format</th><th>Count</th><th>Percent</th></tr>";
while (@row = $result->fetchrow) {
  print "<tr>\n";
  print "<th>" . $row[0] . "</th>\n";
  print "<th>" . $row[1] . "</th>\n";
  print "<th>" . $row[2] . "</th>\n";
  print "<td align=right>" . $row[3] . "</td>\n";
  $pct = sprintf( '%3.2f', $row[3] / $document_count * 100 );
  print "<td align=right>" . $pct . "%</td>\n";
  print "</tr>\n";
  $total = $total + $row[3];
}
print "<tr><th>Total</th><td></td><td></td><td align=right>" . $total . "</td></tr>";
print "</table>\n";




print "<p><hr>\n";

print "<h2>Miscellaneous Statistics</h3>\n";
$sql = "select last_update from document where pub_status='N'";

$result=$conn->exec($sql);
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

$count = 0;
$avg_age   = 0;
($year2, $month2, $day2) = Today();
while (@row = $result->fetchrow) {

  $last_update = $row[0];
  if (($last_update ne "") && ($last_update ne "1970-01-01" )) {
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
print "<tr><th>Average Age Since Last Update</th><td>&nbsp;";
printf "%i", $avg_age;
print " days</td></tr>";
print "</table>\n";



$L->EndPage();
