#!/usr/bin/perl

use CGI qw(:standard);
use Pg;
use Lampadas;

$L = new Lampadas;

$dbmain='ldp';
@row;
$count = 0;
$query = new CGI;

# Read parameters
#
$chkBACKGROUNDER = $L->Param('chkBACKGROUNDER');
$chkHOWTO        = $L->Param('chkHOWTO');
$chkMINI         = $L->Param('chkMINI');
$chkGUIDE        = $L->Param('chkGUIDE');
$chkFAQ          = $L->Param('chkFAQ');
$chkQUICK        = $L->Param('chkQUICK');
$chkTEMPLATE     = $L->Param('chkTEMPLATE');

# Optional Fields
#
$chkSTATUS       = $L->Param('chkSTATUS');
$chkCLASS        = $L->Param('chkCLASS');
$chkFORMAT       = $L->Param('chkFORMAT');
$chkDTD          = $L->Param('chkDTD');
$chkPUBDATE      = $L->Param('chkPUBDATE');
$chkLASTUPDATE   = $L->Param('chkLASTUPDATE');
$chkTICKLEDATE   = $L->Param('chkTICKLEDATE');
$chkREVIEWSTATUS = $L->Param('chkREVIEWSTATUS');
$chkTECHSTATUS   = $L->Param('chkTECHSTATUS');
$chkURL          = $L->Param('chkURL');
$chkMAINTAINED   = $L->Param('chkMAINTAINED');
$chkLICENSE      = $L->Param('chkLICENSE');
$chkVERSION      = $L->Param('chkVERSION');
$chkFILENAME     = $L->Param('chkFILENAME');
$chkRATING       = $L->Param('chkRATING');

$SORT     = $L->Param('strSORT');
$SORT = "Title" unless ($SORT);

$strSTATUS = $L->Param('strSTATUS');

$mydocuments = $L->Param("MyDocuments");
$reload = $L->Param('Reload');

# if we're not reloading, or aren't a maintainer, the default is to show only Active ('N') documents.
unless (($reload eq 'Reload') or ($mydocuments eq 'MyDocuments') or ($L->Maintainer())) {
	$strSTATUS = 'N';
}


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
$VERSION = "";
$FILENAME = "";
$RATING = "";

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
if ( $chkVERSION eq "on" ) { $VERSION = "checked "; }
if ( $chkFILENAME eq "on" ) { $FILENAME = "checked "; }
if ( $chkRATING eq "on" ) { $RATING = "checked "; }

# print the page
$L->StartPage('Document List');



print "<table class='box'>";
print "<form name=filter method=POST action='document_list.pl'>";
print "<tr><th>Classes</th><th>Optional Fields</th><th>Sorting Options</th>";
print "<th>Status</th>" if ($L->Maintainer());
print "</tr>";
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
print "<table><tr><td valign=top>\n";
print "<input type=checkbox $STATUS name=chkSTATUS>Status<br>\n" if ($L->Maintainer());
print "<input type=checkbox $CLASS name=chkCLASS>Class<br>\n";
print "<input type=checkbox $URL name=chkURL>URL<br>\n";
print "<input type=checkbox $RATING name=chkRATING>Rating<br>\n";
if ($L->Maintainer()) {
	print "<input type=checkbox $FORMAT name=chkFORMAT>Format<br>\n";
	print "<input type=checkbox $DTD name=chkDTD>DTD<br>\n";
	print "<input type=checkbox $PUBDATE name=chkPUBDATE>Publication Date<br>\n";
	print "<input type=checkbox $LASTUPDATE name=chkLASTUPDATE>Last Update<br>\n";
	print "</td><td valign=top>\n";
	print "<input type=checkbox $TICKLEDATE name=chkTICKLEDATE>Tickle Date<br>\n";
	print "<input type=checkbox $REVIEWSTATUS name=chkREVIEWSTATUS>Review Status<br>\n";
	print "<input type=checkbox $TECHSTATUS name=chkTECHSTATUS>Tech Review Status<br>\n";
	print "<input type=checkbox $MAINTAINED name=chkMAINTAINED>Maintained<br>\n";
	print "<input type=checkbox $LICENSE name=chkLICENSE>License<br>\n";
	print "<input type=checkbox $VERSION name=chkVERSION>Version<br>\n";
	print "<input type=checkbox $FILENAME name=chkFILENAME>Filename<br>\n";
}
print "</td></tr></table>\n";
print "</td>\n";

print "<td valign=top>\n";
print "<select name=strSORT>\n";
if ( $SORT eq "title" ) { print '<option selected value="title">Title</option>'; } else { print '<option value="title">Title</option>' }
if ( $SORT eq "class" ) { print '<option selected value="class">Class</option>'; } else { print '<option value="class">Class</option>' }
if ( $SORT eq "rating" ) { print '<option selected value="rating">Rating</option>'; } else { print '<option value="rating">Rating</option>' }
if ($L->Maintainer()) {
	if ( $SORT eq "document.pub_status" ) { print '<option selected value="document.pub_status">Status</option>'; } else { print '<option value="document.pub_status">Status</option>' }
	if ( $SORT eq "review_status_name" ) { print '<option selected value="review_status_name">Review Status</option>'; } else { print '<option value="review_status_name">Review Status</option>' }
	if ( $SORT eq "tech_review_status_name" ) { print '<option selected value="tech_review_status_name">Tech Review Status</option>'; } else { print '<option value="tech_review_status_name">Tech Review Status</option>' }
	if ( $SORT eq "format" ) { print '<option selected value="format">Format</option>'; } else { print '<option value="format">Format</option>' }
	if ( $SORT eq "dtd" ) { print '<option selected value="dtd">DTD</option>'; } else { print '<option value="dtd">DTD</option>' }
	if ( $SORT eq "pub_date" ) { print '<option selected value="pub_date">Publication Date</option>'; } else { print '<option value="pub_date">Publication Date</option>' }
	if ( $SORT eq "last_update" ) { print '<option selected value="last_update">Last Update</option>'; } else { print '<option value="last_update">Last Update</option>' }
	if ( $SORT eq "tickle_date" ) { print '<option selected value="tickle_date">Tickle Date</option>'; } else { print '<option value="tickle_date">Tickle Date</option>' }
	if ( $SORT eq "url" ) { print '<option selected value="url">URL</option>'; } else { print '<option value="url">URL</option>' }
	if ( $SORT eq "maintained" ) { print '<option selected value="maintained">Maintained</option>'; } else { print '<option value="maintained">Maintained</option>' }
	if ( $SORT eq "license" ) { print '<option selected value="license">License</option>'; } else { print '<option value="license">License</option>' }
	if ( $SORT eq "filename" ) { print '<option selected value="filename">Filename</option>'; } else { print '<option value="filename">Filename</option>' }
}
print "</select><br>";
print "</td>\n";

if ($L->Maintainer()) {
	print "<td valign=top>\n";
	print "<select name=strSTATUS>\n";
	print "<option></option>\n";
	if ( $strSTATUS eq "N" ) { print '<option selected value="N">Active</option>'; } else { print '<option value="N">Active</option>' }
	if ( $strSTATUS eq "?" ) { print '<option selected value="?">Unknown</option>'; } else { print '<option value="?">Unknown</option>' }
	if ( $strSTATUS eq "A" ) { print '<option selected value="A">Archived</option>'; } else { print '<option value="A">Archived</option>' }
	if ( $strSTATUS eq "D" ) { print '<option selected value="D">Deleted</option>'; } else { print '<option value="D">Deleted</option>' }
	if ( $strSTATUS eq "O" ) { print '<option selected value="O">Offsite</option>'; } else { print '<option value="O">Offsite</option>' }
	if ( $strSTATUS eq "P" ) { print '<option selected value="P">Pending</option>'; } else { print '<option value="P">Pending</option>' }
	if ( $strSTATUS eq "R" ) { print '<option selected value="R">Replaced</option>'; } else { print '<option value="R">Replaced</option>' }
	if ( $strSTATUS eq "W" ) { print '<option selected value="W">Wishlist</option>'; } else { print '<option value="W">Wishlist</option>' }
	if ( $strSTATUS eq "C" ) { print '<option selected value="C">Cancelled</option>'; } else { print '<option value="C">Cancelled</option>' }
	print "</select>\n";
	print "</td>\n";
}

print "</tr></table>\n";
print "<input type=submit name=Reload value=Reload>\n";

# connect to the database
$conn=Pg::connectdb("dbname=$dbmain");

if ($L->Maintainer()) {
	print "<input type=submit value='MyDocuments' name=MyDocuments>\n";
}

print "</form>\n";

print "<p><table>\n";
print "<tr><th>Title</th>";
if ( $STATUS ) { print "<th>Status</th>"; }
if ( $REVIEWSTATUS ) { print "<th>Review Status</th>"; }
if ( $TECHSTATUS ) { print "<th>Tech Status</th>"; }
if ( $RATING ) { print "<th>Rating</th>"; }
if ( $MAINTAINED ) { print "<th>Maintained</th>"; }
if ( $LICENSE ) { print "<th>License</th>"; }
if ( $VERSION ) { print "<th>Version</th>"; }
if ( $FILENAME ) { print "<th>Filename</th>"; }
if ( $CLASS ) { print "<th>Class</th>"; }
if ( $FORMAT ) { print "<th>Format</th>"; }
if ( $DTD ) { print "<th>DTD</th>"; }
if ( $PUBDATE ) { print "<th>Pub Date</th>"; }
if ( $LASTUPDATE ) { print "<th>Last Update</th>"; }
if ( $TICKLEDATE ) { print "<th>Tickle Date</th>"; }
if ( $URL ) { print "<th>URL</th>"; }
print "</tr>\n";

# load the tuples
$sql = "SELECT document.doc_id, title, pub_status_name, class, format, tickle_date, dtd, lr.review_status_name, tr.review_status_name as tech_review_status_name, url, pub_date, last_update, maintained, license, version, filename, rating";
$sql .= " FROM document,";
$sql .= " pub_status,";
$sql .= " review_status lr,";
$sql .= " review_status tr";
$sql .= ", document_user du" if ($mydocuments);
$sql .= " $WHERE";
if ($mydocuments){
	$sql .= " AND document.doc_id=du.doc_id";
	$sql .= " AND du.user_id=" . $L->CurrentUserID();
	$sql .= " AND du.active='t'";
}
$sql .= " AND document.pub_status=pub_status.pub_status";
$sql .= " AND document.review_status = lr.review_status";
$sql .= " AND document.tech_review_status = tr.review_status";
$sql .= " AND url > ''" unless ($L->Maintainer());
if ( $strSTATUS ) { $sql = $sql . " AND document.pub_status='" . $strSTATUS . "'" };
$sql = $sql . " ORDER BY $SORT";
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
	$version                 = $row[14];
	$filename                = $row[15];
	$rating                  = $row[16];
	print "<tr>";
	if ($L->Maintainer()) {
		print "<td>\n";
		print a({href=>"document_edit.pl?doc_id=$doc_id"},"$title");
		print "&nbsp;&nbsp;&nbsp;<a href='$url'>Go!</a>" if ($url);
		print "</td>\n";
	} elsif ($url) {
		print "<td>\n";
		print "&nbsp;&nbsp;&nbsp;<a href='$url'>$title</a>";
		print "</td>\n";
	}
	if ( $STATUS) { print "<td>$pub_status_name</td>"; }
	if ( $REVIEWSTATUS) { print "<td>$review_status_name</td>"; }
	if ( $TECHSTATUS) { print "<td>$tech_review_status_name</td>"; }
	if ( $RATING) { print "<td>$rating</td>"; }
	if ( $MAINTAINED ) { print "<td>$maintained</td>"; }
	if ( $LICENSE ) { print "<td>$license</td>"; }
	if ( $VERSION ) { print "<td>$version</td>"; }
	if ( $FILENAME ) { print "<td>$filename</td>"; }
	if ( $CLASS ) { print "<td>$class</td>"; }
	if ( $FORMAT) { print "<td>$format</td>"; }
	if ( $DTD ) { print "<td>$dtd</td>"; }
	if ( $PUBDATE ) { print "<td>$pub_date</td>"; }
	if ( $LASTUPDATE ) { print "<td>$last_update</td>"; }
	if ( $TICKLEDATE ) {
		$date = `date -I`;
		if ($date gt $tickle_date) {
			print "<td><font color=red>$tickle_date</font></td>";
		} else {
			print "<td>$tickle_date</td>";
		}
	}

	if ($URL) { print "<td>$url</td>"; }
	print "</tr>\n";
	$count++;
}
print "</table>\n";

print "<p>Count: $count";

$L->EndPage();

