#!/usr/bin/perl

use CGI qw(:standard);
use Pg;
use Time::localtime;

$dbmain='ldp';
@row;
$count = 0;
$query = new CGI;

# Read parameters
$chkBACKGROUNDER = param('chkBACKGROUNDER');
$chkHOWTO        = param('chkHOWTO');
$chkMINI         = param('chkMINI');
$chkGUIDE        = param('chkGUIDE');
$chkFAQ          = param('chkFAQ');
$chkQUICK        = param('chkQUICK');
$chkTEMPLATE     = param('chkTEMPLATE');

# Optional Fields
$chkSTATUS       = param('chkSTATUS');
$chkCLASS        = param('chkCLASS');
$chkFORMAT       = param('chkFORMAT');
$chkDTD          = param('chkDTD');
$chkPUBDATE      = param('chkPUBDATE');
$chkLASTUPDATE   = param('chkLASTUPDATE');
$chkTICKLEDATE   = param('chkTICKLEDATE');
$chkREVIEWSTATUS = param('chkREVIEWSTATUS');
$chkTECHSTATUS   = param('chkTECHSTATUS');
$chkURL          = param('chkURL');
$chkMAINTAINED   = param('chkMAINTAINED');
$chkLICENSE      = param('chkLICENSE');

$SORT1     = param('strSORT1');
$SORT2     = "";
$SORT3     = "";

if ( $SORT1 ) {
  $SORT2     = param('strSORT2');
  $SORT3     = param('strSORT3');
}
else {
  $SORT1 = "Title";
}

if ( $SORT2 ) { $SORT2 = ", $SORT2"; }
if ( $SORT3 ) { $SORT3 = ", $SORT3"; }

# Clear
$BACKGROUNDER = "";
$HOWTO = "";
$MINI = "";
$GUIDE = "";
$FAQ = "";
$QUICK = "";
$TEMPLATE = "";

$STATUS = "";
$CLASS = "";
$FORMAT = "";
$DTD = "";
$PUBDATE = "";
$LASTUPDATE = "";
$TICKLEDATE = "";
$REVIEWSTATUS = "";
$TECHSTATUS = "";
$URL = "";
$MAINTAINED = "";
$LICENSE = "";

# Translate them into checked phrases for checkboxes and WHERE clauses
$WHERE = "WHERE class in (''";
if ( $chkBACKGROUNDER eq "on" ) { $BACKGROUNDER = "checked "; $WHERE = $WHERE . ",'BACKGROUNDER'"; }
if ( $chkHOWTO eq "on" ) { $HOWTO = "checked "; $WHERE = $WHERE . ",'HOWTO'"; }
if ( $chkMINI eq "on" ) { $MINI = "checked "; $WHERE = $WHERE . ",'MINI'"; }
if ( $chkGUIDE eq "on" ) { $GUIDE = "checked "; $WHERE = $WHERE . ",'GUIDE'"; }
if ( $chkFAQ eq "on" ) { $FAQ = "checked "; $WHERE = $WHERE . ",'FAQ'"; }
if ( $chkQUICK eq "on" ) { $QUICK = "checked "; $WHERE = $WHERE . ",'QUICK'"; }
if ( $chkTEMPLATE eq "on" ) { $TEMPLATE = "checked "; $WHERE = $WHERE . ",'TEMPLATE'"; }

if ( length($WHERE) < 20  ) { $WHERE = $WHERE . ", 'BACKGROUNDER', 'HOWTO', 'MINI', 'GUIDE', 'FAQ', 'QUICK', 'TEMPLATE'" }

$WHERE = $WHERE . ") ";

if ( $chkSTATUS eq "on" ) { $STATUS = "checked "; }
if ( $chkCLASS eq "on" ) { $CLASS = "checked "; }
if ( $chkFORMAT eq "on" ) { $FORMAT = "checked "; }
if ( $chkDTD eq "on" ) { $DTD = "checked "; }
if ( $chkPUBDATE eq "on" ) { $PUBDATE = "checked "; }
if ( $chkLASTUPDATE eq "on" ) { $LASTUPDATE = "checked "; }
if ( $chkTICKLEDATE eq "on" ) { $TICKLEDATE = "checked "; }
if ( $chkREVIEWSTATUS eq "on" ) { $REVIEWSTATUS = "checked "; }
if ( $chkTECHSTATUS eq "on" ) { $TECHSTATUS = "checked "; }
if ( $chkURL eq "on" ) { $URL = "checked "; }
if ( $chkMAINTAINED eq "on" ) { $MAINTAINED = "checked "; }
if ( $chkLICENSE eq "on" ) { $LICENSE = "checked "; }

# print the page
print header(-expires=>'now');
print "<html><head>\n";
print "<title>Document List</title>\n";
print "<link rel=stylesheet href='../ldp.css' type='text/css'>\n";
print "</head>\n";
print "<body>\n";

print "<h1>Document List</h1>\n";

#print "<p>Welcome, " . $query->remote_user();

print "<p><a href='../index.html'>Index</a> ";
print "<a href='topic_list.pl'>Topics</a>\n";
print "<a href='maintainer_list.pl'>Maintainers</a>\n";
print "<a href='editor_list.pl'>Editors</a>\n";

print "<p><form action='document_edit.pl' method=POST>\n";
print "<p>Jump to a document by ID: <input type=text size=5 name=doc_id>\n";
print "<input type=submit value=Jump>\n";
print "</form>\n";

print "<form name=filter method=POST action='document_list.pl'>";

print "<p><table border=2 cellspacing=5>";
print "<tr><th>Classes</th><th>Optional Fields</th><th>Sorting Options</th></tr>";
print "<tr><td valign=top>\n";
print "<input type=checkbox $BACKGROUNDER name=chkBACKGROUNDER>Backgrounder<br>\n";
print "<input type=checkbox $HOWTO name=chkHOWTO>HOWTOs<br>\n";
print "<input type=checkbox $MINI name=chkMINI>Mini-HOWTOs<br>\n";
print "<input type=checkbox $GUIDE name=chkGUIDE>Guides<br>\n";
print "<input type=checkbox $FAQ name=chkFAQ>FAQs<br>\n";
print "<input type=checkbox $QUICK name=chkQUICK>Quick References<br>\n";
print "<input type=checkbox $TEMPLATE name=chkTEMPLATE>Templates\n";
print "</td>\n";

print "<td valign=top>\n";
print "<input type=checkbox $STATUS name=chkSTATUS>Status<br>\n";
print "<input type=checkbox $CLASS name=chkCLASS>Class<br>\n";
print "<input type=checkbox $FORMAT name=chkFORMAT>Format<br>\n";
print "<input type=checkbox $DTD name=chkDTD>DTD<br>\n";
print "<input type=checkbox $PUBDATE name=chkPUBDATE>Publication Date<br>\n";
print "<input type=checkbox $LASTUPDATE name=chkLASTUPDATE>Last Update<br>\n";
print "<input type=checkbox $TICKLEDATE name=chkTICKLEDATE>Tickle Date<br>\n";
print "<input type=checkbox $REVIEWSTATUS name=chkREVIEWSTATUS>Review Status<br>\n";
print "<input type=checkbox $TECHSTATUS name=chkTECHSTATUS>Tech Review Status<br>\n";
print "<input type=checkbox $URL name=chkURL>URL<br>\n";
print "<input type=checkbox $MAINTAINED name=chkMAINTAINED>Maintained<br>\n";
print "<input type=checkbox $LICENSE name=chkLICENSE>License<br>\n";
print "</td>\n";

print "<td valign=top>\n";
print "<select name=strSORT1>\n";
print "<option></option>\n";
print "<option>Title</option>\n";
print "<option value='document.pub_status, title'>Status</option>\n";
print "<option value='review_status_name, title'>Review Status</option>\n";
print "<option value=tech_review_status_name, title'>Tech Review Status</option>\n";
print "<option value='class, title'>Class</option>\n";
print "<option value='format, title'>Format</option>\n";
print "<option value='dtd, title'>DTD</option>\n";
print "<option value='pub_date, title'>Publication Date</option>\n";
print "<option value='last_update, title'>Last Update</option>\n";
print "<option value='tickle_date, title'>Tickle Date</option>\n";
print "<option value='url, title'>URL</option>\n";
print "<option value='maintained, title'>Maintained</option>\n";
print "<option value='license, title'>License</option>\n";
print "</select><br>";

print "</td>\n";

print "</tr></table>\n";
print "<input type=submit value=Reload>\n";

print "</form>\n";

print "<p><hr>";

print "<p><table border=1>\n";
print "<tr><th>Title</th>";
if ( $STATUS ) { print "<th>Status</th>"; }
if ( $REVIEWSTATUS ) { print "<th>Review Status</th>"; }
if ( $TECHSTATUS ) { print "<th>Tech Status</th>"; }
if ( $MAINTAINED ) { print "<th>Maintained</th>"; }
if ( $LICENSE ) { print "<th>License</th>"; }
if ( $CLASS ) { print "<th>Class</th>"; }
if ( $FORMAT ) { print "<th>Format</th>"; }
if ( $DTD ) { print "<th>DTD</th>"; }
if ( $PUBDATE ) { print "<th>Pub Date</th>"; }
if ( $LASTUPDATE ) { print "<th>Last Update</th>"; }
if ( $TICKLEDATE ) { print "<th>Tickle Date</th>"; }
if ( $URL ) { print "<th>URL</th>"; }
print "</tr>\n";


# Connect and load the tuples
$conn=Pg::connectdb("dbname=$dbmain");
$sql = "SELECT doc_id, title, pub_status_name, class, format, tickle_date, dtd, lr.review_status_name, tr.review_status_name as tech_review_status_name, url, pub_date, last_update, maintained, license FROM document, pub_status, review_status lr, review_status tr $WHERE AND document.pub_status=pub_status.pub_status AND document.review_status = lr.review_status and document.tech_review_status = tr.review_status ORDER BY $SORT1";
#print "<tr><td colspan=20>$sql</td></tr>";

$result=$conn->exec("$sql");
die $conn->errorMessage unless PGRES_TUPLES_OK eq $result->resultStatus;

while (@row = $result->fetchrow) {
  $doc_id                  = $row[0];
  $title                   = $row[1];
  $pub_status_name         = $row[2];
  $class                   = $row[3];
  $format                  = $row[4];
  $tickle_date             = $row[5];
  $dtd                     = $row[6];
  $review_status_name      = $row[7];
  $tech_review_status_name = $row[8];
  $url                     = $row[9];
  $pub_date                = $row[10];
  $last_update             = $row[11];
  $maintained              = $row[12];
  $maintained              =~ s/f/No/;
  $maintained              =~ s/t/Yes/;
  $license                 = $row[13];
  print "<tr>";
  print "<td>";
  print a({href=>"document_edit.pl?doc_id=$doc_id"},"$title");
  if ( $url ne "" ) { print "&nbsp;&nbsp;&nbsp;<a href='$url'>Go!</a>" }
  print "</td>";
  if ( $STATUS) { print "<td>$pub_status_name</td>"; }
  if ( $REVIEWSTATUS) { print "<td>$review_status_name</td>"; }
  if ( $TECHSTATUS) { print "<td>$tech_review_status_name</td>"; }
  if ( $MAINTAINED ) { print "<td>$maintained</td>"; }
  if ( $LICENSE ) { print "<td>$license</td>"; }
  if ( $CLASS ) { print "<td>$class</td>"; }
  if ( $FORMAT) { print "<td>$format</td>"; }
  if ( $DTD ) { print "<td>$dtd</td>"; }
  if ( $PUBDATE ) { print "<td>$pub_date</td>"; }
  if ( $LASTUPDATE ) { print "<td>$last_update</td>"; }
  if ( $TICKLEDATE ) {
    $date = `date -I`;
    if ( $date gt $tickle_date  ) {
      print "<td><font color=red>$tickle_date</font></td>"
    }
    else {
      print "<td>$tickle_date</td>"
    }
  }
  if ( $URL ) { print "<td>$url</td>"; }
  print "</tr>\n";
  $count++;
}
print "</table>\n";

print "<p>Count: $count";

print "<p><hr>";

print "<h1>New Document</h1>\n";

print "<p><form method=POST action='document_add.pl'>\n";
print "<input type=hidden name=caller value='document_list.pl'>\n";
print "<table>\n";
print "<tr><td align=right>Title:</td><td><input type=text name=title size=60 width=60></td></tr>\n";

print "<tr><td align=right>Status:</td><td>";
print "<select name=pub_status>\n";
print "<option value='N'>Active</option>\n";
print "<option value='?'>Unknown</option>\n";
print "<option value='A'>Archived</option>\n";
print "<option value='D'>Deleted</option>\n";
print "<option value='O'>Offsite</option>\n";
print "<option value='P'>Pending</option>\n";
print "<option value='R'>Replaced</option>\n";
print "<option value='W'>Wishlist</option>\n";
print "</select>\n";
print "</td></tr>\n";

print "<tr><td align=right>Class:</td><td>";
print "<select name=class>\n";
print "<option>BACKGROUNDER</option>\n";
print "<option>HOWTO</option>\n";
print "<option>MINI</option>\n";
print "<option>FAQ</option>\n";
print "<option>QUICK</option>\n";
print "<option>GUIDE</option>\n";
print "<option>TEMPLATE</option>\n";
print "</select>\n";
print "</td></tr>\n";

print "<tr><td align=right>Format:</td><td>";
print "<select name=format>\n";
print "<option></option>\n";
print "<option>SGML</option>\n";
print "<option>XML</option>\n";
print "<option>TEXT</option>\n";
print "<option>LaTeX</option>\n";
print "<option>PDF</option>\n";
print "</select>\n";
print "</td></tr>\n";

print "<tr><td align=right>DTD:</td><td>";
print "<select name=dtd>\n";
print "<option></option>\n";
print "<option>N/A</option>\n";
print "<option>HTML</option>\n";
print "<option>DocBook</option>\n";
print "<option>LinuxDoc</option>\n";
print "</select>\n";
print "</td></tr>\n";

print "<tr><td></td><td><input type=submit value=Add></td></tr>\n";
print "</table></form>\n";

print end_html;

