#! /usr/bin/perl

use CGI qw(:standard);
use Pg;

$query = new CGI;
$dbmain = "ldp";
@row;

# Read parameters
$caller        = param('caller');
$doc_id        = param('doc_id');
$maintainer_id = param('maintainer_id');
$active        = param('active');
$role          = param('role');
$email         = param('email');

$conn=Pg::connectdb("dbname=$dbmain");

$username = $query->remote_user();
$result=$conn->exec("SELECT username, admin, maintainer_id FROM username WHERE username='$username'");
@row = $result->fetchrow;
$founduser = $row[0];
$founduser =~ s/\s+$//;
if ($username ne $founduser) {
	print $query->redirect("../newaccount.html");
	exit;
} else {
	if ($row[1] ne 't') {
		$user_maintainer_id = $row[2];
		$result=$conn->exec("SELECT count(*) FROM document_maintainer WHERE maintainer_id=$user_maintainer_id AND doc_id=$doc_id AND active='t'");
		@row = $result->fetchrow;
		unless ($row[0]) {
			print $query->redirect("../wrongpermission.html");
			exit;
		}
	}
}

#print header;
#print start_html;
$sql = "INSERT INTO document_maintainer(doc_id, maintainer_id, active, role, email) VALUES ($doc_id, $maintainer_id, '$active', '$role', '$email' )";
$result=$conn->exec($sql);

#update the maintained field in the document record
$sql = "SELECT COUNT(*) as active_maintainers FROM document_maintainer WHERE doc_id=$doc_id AND (role='Author' OR role='Co-Author' OR role='Maintainer') AND active='t'";
$result=$conn->exec($sql);
@row = $result->fetchrow;
$active_maintainers = $row[0];
if ( $active_maintainers > 0 ) { $maintained = "t" } else { $maintained = "f" }
$sql = "UPDATE document SET maintained='$maintained' WHERE doc_id=$doc_id";
$result=$conn->exec($sql);

#print header;
#print start_html;
#print $sql;
#print end_html;
#exit;

print $query->redirect($caller)

