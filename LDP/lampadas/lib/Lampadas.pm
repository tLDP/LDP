#!/usr/bin/perl
# 
# This package provides Perl bindings for the Lampadas database,
# routines for accessing the CGI environment,
# and HTML generators for creating the web front end.
# 
package Lampadas;

use Lampadas::Database;

use CGI qw(:standard);
use Exporter;

@ISA	= qw(Exporter);
@EXPORT	= qw(
	new,
	Param,
	Config,

	CurrentUserID,
	CurrentUser,
	Admin,
	Maintainer,

	Users,
	User,
	UserDocs,
	UserNotes,
	AddUserNote,

	Docs,
	Doc,
	AddDoc,

	DocUsers,
	DocTopics,
	DocNotes,
	DocVersions,
	AddDocVersion,
	SaveDocVersion,
	DelDocVersion,
	
	Roles,
	Classes,
	PubStatuses,
	ReviewStatuses,
	Licenses,
	Topics,
	Topic,
	Subtopics,
	Formats,
	DTDs,

	DocCount,
	DocCountByClass,
	DocCountByPubStatus,

	StartPage,
	EndPage,

	ErrorsTable,
	NavBar,

	RoleCombo,
	ClassCombo,
	PubStatusCombo,
	ReviewStatusCombo,
	TechReviewStatusCombo,
	LicenseCombo,
	TopicCombo,
	SubtopicCombo,
	FormatCombo,
	DTDCombo,

	UsersTable,
	UserTable,
	UserDocsTable,
	UserNotesTable,
	DocTable,
	DocVersionsTable,
	DocUsersTable,
	DocTopicsTable,
	DocRatingTable,
	DocNotesTable,
	TopicsTable,

	PubStatusStatsTable,
	LicenseStatsTable,
	FreeNonfreeStatsTable,
	ClassStatsTable,
	FormatStatsTable,
	DTDStatsTable,
	FormatDTDStatsTable,
	DetailedStatsTable,
	MiscStatsTable,
	
	BarGraphTable,

	NavBox,
	TopicsBox,
	TitleBox,
	LoginBox,
	AdminBox,

	Login,
	Logout,
	AddUser,
	AddError,
	Mail,
);

$CGI	= new CGI;
$DB	= new Lampadas::Database;

# Initialize global variables
#
$VERSION = '0.1';
$currentuser_id = 0;
%currentuser = ();
&ReadCookie;

@errors = ();			# System errors, displayed on the next page
$debug = 0;			# Set this to 1 to get debugging messages

sub new {
	my $that = shift;
	my $class = ref($that) || $that;
	my $self = {};
	bless $self, $class;
	return $self;
}

sub Param {
	my $this = shift;
	my $paramname = shift;
	return &trim($CGI->param($paramname));
}

sub Config {
	my $self = shift;
	my $name = shift;
	my @row = $DB->Row("SELECT value FROM config WHERE name='$name'");
	my $value = $row[0];
	$value =~ s/\s+$//;
	return $value
}

sub CurrentUserID {
	return $currentuser_id;
}

sub CurrentUser {
	return %currentuser;
}

sub Admin {
	return 0 unless CurrentUserID();
	return $currentuser{admin};
}

sub Maintainer {
	return 0 unless (CurrentUserID());
	return 1 if (Admin());
	return 1 if ($DB->Value("SELECT COUNT(*) FROM document_user WHERE active='t' AND user_id=" . CurrentUserID())); 
	return 0;
}

sub Users {
	my $self = shift;
	my %users = ();
	my $sql = "SELECT user_id, username, first_name, middle_name, surname, email, admin FROM username";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$user_id = $row[0];
		$users{$user_id}{id}		= $row[0];
		$users{$user_id}{username}	= &trim($row[1]);
		$users{$user_id}{first_name}	= &trim($row[2]);
		$users{$user_id}{middle_name}	= &trim($row[3]);
		$users{$user_id}{surname}	= &trim($row[4]);
		$users{$user_id}{name}		= &trim(&trim($users{$user_id}{first_name} . ' ' . $users{$user_id}{middle_name}) . ' ' . $users{$user_id}{surname});
		$users{$user_id}{email}		= &trim($row[5]);
		$users{$user_id}{admin}		= &yn2bool($row[6]);
	}
	return %users;
}

sub User {
	my $self = shift;
	my $user_id = shift;
	my %user = ();
	my $sql = "SELECT username, first_name, middle_name, surname, email, admin, notes FROM username WHERE user_id=$user_id";
	my @row = $DB->Row("$sql");
	$user{id}		= $user_id;
	$user{username}		= &trim($row[0]);
	$user{first_name}	= &trim($row[1]);
	$user{middle_name}	= &trim($row[2]);
	$user{surname}		= &trim($row[3]);
	$user{name}		= &trim(&trim($user{first_name} . ' ' . $user{middle_name}) . ' ' . $user{surname});
	$user{email}		= &trim($row[4]);
	$user{admin}		= &yn2bool($row[5]);
	$user{notes}		= &trim($row[6]);

	return %user;
}

sub UserDocs {
	my $self = shift;
	my $user_id = shift;
	my %docs = ();
	$sql = "SELECT d.doc_id, d.title, d.class, d.pub_status, ps.pub_status_name, du.role, du.active, du.email FROM document d, document_user du, pub_status ps WHERE d.doc_id=du.doc_id AND d.pub_status = ps.pub_status AND user_id=$user_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$doc_id				= $row[0];
		$docs{$doc_id}{id}		= $doc_id;
		$docs{$doc_id}{title}		= &trim($row[1]);
		$docs{$doc_id}{class}		= &trim($row[2]);
		$docs{$doc_id}{pub_status}	= &trim($row[3]);
		$docs{$doc_id}{pub_status_name}	= &trim($row[4]);
		$docs{$doc_id}{role}		= &trim($row[5]);
		$docs{$doc_id}{active}		= &yn2bool($row[6]);
		$docs{$doc_id}{email}		= &trim($row[7]);
	}
	return %docs;
}

sub UserNotes {
	my ($self, $user_id) = @_;
	my $usernotes = ();
	my $sql = "SELECT un.date_entered, un.notes, u.username FROM username u, username_notes un WHERE u.user_id = un.user_id AND u.user_id = $user_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$date_entered	= &trim($row[0]);
		$notes		= &trim($row[1]);
		$username	= &trim($row[2]);
		$usernotes{$date_entered}{notes}	= $notes;
		$usernotes{$date_entered}{username}	= $username;
	}
	return %usernotes;
}

sub AddUserNote {
	my ($self, $user_id, $notes) = @_;
	my $sql = "INSERT INTO username (user_id, notes, creator_id) VALUES ($user_id, " . wsq($notes) . ", " . CurrentUserID() . ")";
}

sub Docs {
	my $self = shift;
	my %docs = ();
	my $sql = "SELECT doc_id, title, filename, class, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating FROM document";
	my $result = $DB->Recordset($sql);
	while (@row = $result->fetchrow) {
		$doc_id	= $row[0];
		$docs{$doc_id}{id}			= &trim($row[0]);
		$docs{$doc_id}{title}			= &trim($row[1]);
		$docs{$doc_id}{filename}		= &trim($row[2]);
		$docs{$doc_id}{class}			= &trim($row[3]);
		$docs{$doc_id}{format}			= &trim($row[4]);
		$docs{$doc_id}{dtd}			= &trim($row[5]);
		$docs{$doc_id}{dtd_version}		= &trim($row[6]);
		$docs{$doc_id}{version}			= &trim($row[7]);
		$docs{$doc_id}{last_update}		= &trim($row[8]);
		$docs{$doc_id}{url}			= &trim($row[9]);
		$docs{$doc_id}{isbn}			= &trim($row[10]);
		$docs{$doc_id}{pub_status}		= &trim($row[11]);
		$docs{$doc_id}{review_status}		= &trim($row[12]);
		$docs{$doc_id}{tickle_date}		= &trim($row[13]);
		$docs{$doc_id}{pub_date}		= &trim($row[14]);
		$docs{$doc_id}{ref_url}			= &trim($row[15]);
		$docs{$doc_id}{tech_review_status}	= &trim($row[16]);
		$docs{$doc_id}{maintained}		= &trim($row[17]);
		$docs{$doc_id}{license}			= &trim($row[18]);
		$docs{$doc_id}{abstract}		= &trim($row[19]);
		$docs{$doc_id}{rating}			= &trim($row[20]);
	}
	return %docs;
}

sub Doc {
	my $self = shift;
	my $doc_id = shift;
	my $sql = "SELECT doc_id, title, filename, class, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating FROM document WHERE doc_id=$doc_id";
	my @row = $DB->Row("$sql");
	$doc{id}			= &trim($row[0]);
	$doc{title}			= &trim($row[1]);
	$doc{filename}			= &trim($row[2]);
	$doc{class}			= &trim($row[3]);
	$doc{format}			= &trim($row[4]);
	$doc{dtd}			= &trim($row[5]);
	$doc{dtd_version}		= &trim($row[6]);
	$doc{version}			= &trim($row[7]);
	$doc{last_update}		= &trim($row[8]);
	$doc{url}			= &trim($row[9]);
	$doc{isbn}			= &trim($row[10]);
	$doc{pub_status}		= &trim($row[11]);
	$doc{review_status}		= &trim($row[12]);
	$doc{tickle_date}		= &trim($row[13]);
	$doc{pub_date}			= &trim($row[14]);
	$doc{ref_url}			= &trim($row[15]);
	$doc{tech_review_status}	= &trim($row[16]);
	$doc{maintained}		= &trim($row[17]);
	$doc{license}			= &trim($row[18]);
	$doc{abstract}			= &trim($row[19]);
	$doc{rating}			= &trim($row[20]);
	return %doc;
}

sub AddDoc {
	my ($self, $title, $filename, $class, $format, $dtd, $dtd_version, $version, $last_update, $url, $isbn, $pub_status, $review_status, $tickle_date, $pub_date, $ref_url, $tech_review_status, $maintained, $license, $abstract, $rating) = @_;
	my $doc_id = $DB->Value("SELECT MAX(doc_id) FROM document");
	$doc_id++;
	my $sql = "INSERT INTO document(doc_id, title, filename, class, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating)";
	$sql .= " VALUES ($doc_id, " . wsq($title) . ", " . wsq($filename) . ", " . wsq($class) . ", " . wsq($format) . ", " . wsq($dtd) . ", " . wsq($dtd_version) . ", " . wsq($version) . ", " . wsq($last_update) . ", " . wsq($url) . ", " . wsq($isbn) . ", " . wsq($pub_status) . ", " . wsq($review_status) . ", " . wsq($tickle_date) . ", " . wsq($pub_date) . ", " . wsq($ref_url) . ", " . wsq($tech_review_status) . ", " . wsq($maintained) . ", " . wsq($license) . ", " . wsq($abstract) . ", " . wsq($rating) . ")";
	$DB->Exec($sql);
	$doc_id = $DB->Value("SELECT MAX(doc_id) FROM document");
	return $doc_id;
}

sub DocUsers {
	my $self = shift;
	my $doc_id = shift;
	my %docusers = ();
	my $sql = "SELECT document_user.user_id, role, document_user.email, active, username, first_name, middle_name, surname FROM document_user, username WHERE document_user.user_id = username.user_id AND doc_id=$doc_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$user_id	= $row[0];
		$role		= &trim($row[1]);
		$key		= $user_id . $role;
		$docusers{$key}{id}		= &trim($row[0]);
		$docusers{$key}{role}		= &trim($row[1]);
		$docusers{$key}{email}		= &trim($row[2]);
		$docusers{$key}{active}		= &yn2bool($row[3]);
		$docusers{$key}{username}	= &trim($row[4]);
		$docusers{$key}{first_name}	= &trim($row[5]);
		$docusers{$key}{middle_name}	= &trim($row[6]);
		$docusers{$key}{surname}	= &trim($row[7]);
		$docusers{$key}{name}		= &trim(&trim($docusers{$key}{first_name} . ' ' . $docusers{$key}{middle_name}) . ' ' . $docusers{$key}{surname});
	}
	return %docusers;
}

sub DocTopics {
	my ($self, $doc_id) = @_;
	my %doctopics = ();
	my $sql = "SELECT dt.topic_num, dt.subtopic_num, t.topic_name, s.subtopic_name FROM topic t, subtopic s, document_topic dt WHERE t.topic_num = s.topic_num AND dt.topic_num = s.topic_num AND dt.subtopic_num = s.subtopic_num AND dt.doc_id = $doc_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$key = $row[0] . '.' . $row[1];
		$doctopics{$key}{topic_num}	= $row[0];
		$doctopics{$key}{subtopic_num}	= $row[1];
		$doctopics{$key}{topic_name}	= &trim($row[2]);
		$doctopics{$key}{subtopic_name}	= &trim($row[3]);
	}
	return %doctopics;
}

sub DocNotes {
	my ($self, $doc_id) = @_;
	my %docnotes = ();
	my $sql = "SELECT n.date_entered, n.notes, u.username FROM notes n, username u WHERE n.creator_id = u.user_id AND n.doc_id = $doc_id ORDER BY n.date_entered";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$date_entered	= &trim($row[0]);
		$notes		= &trim($row[1]);
		$notes		=~ s/</&lt;/;
		$notes		=~ s/>/&gt;/;
		$username	= &trim($row[2]);
		$docnotes{$date_entered}{notes}		= $notes;
		$docnotes{$date_entered}{username}	= $username;
	}
	return %docnotes;
}

sub DocVersions {
	my $self = shift;
	my $doc_id = shift;
	my %docversions = ();
	my $sql = "SELECT rev_id, version, pub_date, initials, notes FROM document_rev WHERE doc_id = $doc_id ORDER BY pub_date, version";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$rev_id = $row[0];
		$docversions{$rev_id}{rev_id}	= &trim($row[0]);
		$docversions{$rev_id}{version}	= &trim($row[1]);
		$docversions{$rev_id}{pub_date}	= &trim($row[2]);
		$docversions{$rev_id}{initials}	= &trim($row[3]);
		$docversions{$rev_id}{notes}	= &trim($row[4]);
	}
	return %docversions;
}

sub AddDocVersion {
	my ($self, $doc_id, $version, $pub_date, $initials, $notes) = @_;
	my $rev_id = $DB->Value("SELECT max(rev_id) FROM document_rev WHERE doc_id=$doc_id");
	$rev_id++;
	my $sql = "INSERT INTO document_rev(doc_id, rev_id, version, pub_date, initials, notes) VALUES ($doc_id, $rev_id, $version, " . &wsq($pub_date) . ", " . &wsq($initials) . ", " . &wsq($notes) . ")";
	$DB->Exec($sql);
	return $sql;
}

sub SaveDocVersion {
	my ($self, $doc_id, $rev_id, $version, $pub_date, $initials, $notes) = @_;
	my $sql = "UPDATE document_rev SET version=" . wsq($version) . ", pub_date=" . wsq($pub_date) . ", initials=" . wsq($initials) . ", notes=" . wsq($notes) . " WHERE doc_id=$doc_id AND rev_id=$rev_id";
	$DB->Exec($sql);
	return $sql;
}

sub DelDocVersion {
	my ($self, $doc_id, $rev_id) = @_;
	my $sql = "DELETE FROM document_rev WHERE doc_id=$doc_id AND rev_id=$rev_id";
	$DB->Exec($sql);
	return $sql;
}

sub Roles {
	my %roles = ();
	my $sql = "SELECT role FROM role";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$role = &trim($row[0]);
		$roles{$role} = $role;
	}
	return %roles;	
}

sub Classes {
	my %classes = ();
	my $sql = "SELECT class, class_name FROM class";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$class		= &trim($row[0]);
		$classname	= &trim($row[1]);
		$classes{$class} = $classname;
	}
	return %classes;
}

sub PubStatuses {
	my %pubstatuses = ();
	my $sql = "SELECT pub_status, pub_status_name, pub_status_desc FROM pub_status";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$pubstatus	= &trim($row[0]);
		$pubstatusname	= &trim($row[1]);
		$pubstatusdesc	= &trim($row[2]);
		$pubstatuses{$pubstatus}{name} = $pubstatusname;
		$pubstatuses{$pubstatus}{description} = $pubstatusdesc;
	}
	return %pubstatuses;
}

sub ReviewStatuses {
	my %reviewstatuses = ();
	my $sql = "SELECT review_status, review_status_name FROM review_status";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$reviewstatus		= &trim($row[0]);
		$reviewstatusname	= &trim($row[1]);
		$reviewstatuses{$reviewstatus}{name} = $reviewstatusname;
	}
	return %reviewstatuses;
}

sub Licenses {
	my %licenses = ();
	my $sql = "SELECT license FROM license";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$license = &trim($row[0]);
		$licenses{$license} = $license;
	}
	return %licenses;
}

sub Topics {
	my %topics = ();
	my $sql = "SELECT topic_num, topic_name, topic_description FROM topic";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$topicnum	= &trim($row[0]);
		$topicname	= &trim($row[1]);
		$topicdesc	= &trim($row[2]);
		$topics{$topicnum}{num}		= $topicnum;
		$topics{$topicnum}{name}	= $topicname;
		$topics{$topicnum}{description}	= $topicdesc;
	}
	return %topics;
}

sub Topic {
	my ($self, $topic_num) = @_;
	my %topic = ();
	my $sql = "SELECT topic_num, topic_name, topic_description FROM topic WHERE topic_num=$topic_num";
	my $recordset = $DB->Recordset($sql);
	my @row = $recordset->fetchrow;
	$topicnum	= &trim($row[0]);
	$topicname	= &trim($row[1]);
	$topicdesc	= &trim($row[2]);
	$topic{num}		= $topicnum;
	$topic{name}		= $topicname;
	$topic{description}	= $topicdesc;
	return %topic;
}

sub Subtopics {
	my ($self, $topic_num) = @_;
	my %subtopics = ();
	my $sql = "SELECT topic.topic_num, topic_name, topic_description, subtopic_num, subtopic_name, subtopic_description from subtopic, topic WHERE subtopic.topic_num = topic.topic_num";
	$sql .= " AND topic.topic_num = $topic_num" if ($topic_num);
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$topicnum	= &trim($row[0]);
		$topicname	= &trim($row[1]);
		$topicdesc	= &trim($row[2]);
		$subtopicnum	= &trim($row[3]);
		$subtopicname	= &trim($row[4]);
		$subtopicdesc	= &trim($row[5]);
		$key		= $topicnum . '.' . $subtopicnum;
		$subtopics{$key}{topicnum}	= $topicnum;
		$subtopics{$key}{topicname}	= $topicname;
		$subtopics{$key}{topicdesc}	= $topicdesc;
		$subtopics{$key}{num}		= $subtopicnum;
		$subtopics{$key}{name}		= $subtopicname;
		$subtopics{$key}{description}	= $subtopicdesc;
	}
	return %subtopics;
}

sub Formats {
	my %formats = ();
	my $sql = "select format, format_name from format";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$format		= &trim($row[0]);
		$formatname	= &trim($row[1]);
		$formats{$format}{name}	= $formatname;
	}
	return %formats;
}

sub DTDs {
	my %dtds = ();
	my $sql = "select dtd from dtd";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$dtd		= &trim($row[0]);
		$dtds{$dtd}{dtd}	= $dtd;
	}
	return %dtds;
}

sub DocCount {
	return $DB->Value("SELECT COUNT(*) FROM document");
}

sub DocCountByClass {
	my ($self, $class) = @_;
	return $DB->Value("SELECT COUNT(*) FROM document WHERE class IN (" . $class . ")");
}

sub DocCountByPubStatus {
	my ($self, $pub_status) = @_;
	return $DB->Value("SELECT COUNT(*) FROM document WHERE pub_status in (" . $pub_status . ")");
}

sub ReadCookie {
	$session_id = $CGI->cookie('lampadas_session');
	$currentuser_id = $DB->Value("SELECT user_id FROM username WHERE session_id='$session_id'");
	if ($currentuser_id) {
		%currentuser = User($foo, $currentuser_id);
	}
}

sub StartPage {
	my $self = shift;
	my $title = shift;
	my $cookie = shift;

	if ($cookie) {
		print $CGI->header(-cookie=>$cookie,-expires=>'now');
		push @errors, "cookie: $cookie" if ($debug);
	} else {
		print $CGI->header(-expires=>'now');
	}

	print "<html><head>\n";
	print "<title>$title</title>\n";
	print "<link rel='stylesheet' href='css/default.css' type='text/css'>\n";
	print "</head>\n";
	print "<body>\n";

	if ($debug) {
		push @errors, "UserID: $currentuser_id";
		push @errors, "UserName: " . $currentuser{username};
	}
	
	print "<table style='width:100%' class='layout'>\n";
	print "<tr><td colspan=2>\n";
	TitleBox($title);
	ErrorsTable();
	print "</td><tr>\n";

	print "<tr><td valign=top width='200'>\n";
	LoginBox() unless ($currentuser_id);
	AdminBox() if (Maintainer());
	NavBox();
	TopicsBox();
	print "</td><td valign=top>\n";
}

sub EndPage {
	print "</td></tr>\n";
	print "</table>\n";

	print "<p><hr>\n";
	print "<p><center>\n";
	print Config($foo, 'copyright');
	print "</center>\n";
	print "</body>\n";
	print "</html>\n";
	exit;
}

sub RoleCombo {
	my $self = shift;
	my $selected = shift;
	my %roles = Roles();
	my $rolecombo = "<select name='role'>\n";
	foreach $role (sort keys %roles) {
		if ($selected eq $role) {
			$rolecombo .= "<option selected>$role</option>\n";
		} else {
			$rolecombo .= "<option>$role</option>\n";
		}
	}
	$rolecombo .= "</select>\n";
	return $rolecombo;
}

sub ClassCombo {
	my $self = shift;
	my $selected = shift;
	my %classes = Classes();
	my $classcombo = "<select name='class'>\n";
	foreach $class (sort keys %classes) {
		if ($selected eq $class) {
			$classcombo .= "<option selected>$class</option>\n";
		} else {
			$classcombo .= "<option>$class</option>\n";
		}
	}
	$classcombo .= "</select>\n";
	return $classcombo;
}

sub PubStatusCombo {
	my $self = shift;
	my $selected = shift;
	my %pubstatuses = PubStatuses();
	my $pubstatuscombo = "<select name='pub_status'>\n";
	foreach $pubstatus (sort { $pubstatuses{$a}{name} cmp $pubstatuses{$b}{name} } keys %pubstatuses) {
		if ($selected eq $pubstatus) {
			$pubstatuscombo .= "<option value='$pubstatus' selected>$pubstatuses{$pubstatus}{name}</option>\n";
		} else {
			$pubstatuscombo .= "<option value='$pubstatus'>$pubstatuses{$pubstatus}{name}</option>\n";
		}
	}
	$pubstatuscombo .= "</select>\n";
	return $pubstatuscombo;
}

sub ReviewStatusCombo {
	my $self = shift;
	my $selected = shift;
	my %reviewstatuses = ReviewStatuses();
	my $reviewstatuscombo = "<select name='review_status'>\n";
	$reviewstatuscombo .= "<option></option\n";
	foreach $reviewstatus (sort { $reviewstatuses{$a}{name} cmp $reviewstatuses{$b}{name} } keys %reviewstatuses) {
		if ($selected eq $reviewstatus) {
			$reviewstatuscombo .= "<option value='$reviewstatus' selected>$reviewstatuses{$reviewstatus}{name}</option>\n";
		} else {
			$reviewstatuscombo .= "<option value='$reviewstatus'>$reviewstatuses{$reviewstatus}{name}</option>\n";
		}
	}
	$reviewstatuscombo .= "</select>\n";
	return $reviewstatuscombo;
}

sub TechReviewStatusCombo {
	my $self = shift;
	my $selected = shift;
	my %reviewstatuses = ReviewStatuses();
	my $reviewstatuscombo = "<select name='tech_review_status'>\n";
	$reviewstatuscombo .= "<option></option\n";
	foreach $reviewstatus (sort { $reviewstatuses{$a}{name} cmp $reviewstatuses{$b}{name} } keys %reviewstatuses) {
		if ($selected eq $reviewstatus) {
			$reviewstatuscombo .= "<option value='$reviewstatus' selected>$reviewstatuses{$reviewstatus}{name}</option>\n";
		} else {
			$reviewstatuscombo .= "<option value='$reviewstatus'>$reviewstatuses{$reviewstatus}{name}</option>\n";
		}
	}
	$reviewstatuscombo .= "</select>\n";
	return $reviewstatuscombo;
}

sub LicenseCombo {
	my $self = shift;
	my $selected = shift;
	my %licenses = Licenses();
	my $licensecombo = "<select name='license'>\n";
	$licensecombo .= "<option></option>\n";
	foreach $license (sort keys %licenses) {
		if ($selected eq $license) {
			$licensecombo .= "<option selected>$license</option>\n";
		} else {
			$licensecombo .= "<option>$license</option>\n";
		}
	}
	$licensecombo .= "</select>\n";
	return $licensecombo;
}

sub TopicCombo {
	my $self = shift;
	my $selected = shift;
	my %topics = Topics();
	my $topiccombo = "<select name='topic'>\n";
	foreach $topic (sort { $a <=> $b } keys %topics) {
		if ($selected eq $topic) {
			$topiccombo .= "<option value='$topic' selected>$topics{$topic}{num}. $topics{$topic}{name}</option>\n";
		} else {
			$topiccombo .= "<option value='$topic'>$topics{$topic}{num}. $topics{$topic}{name}</option>\n";
		}
	}
	$topiccombo .= "</select>\n";
	return $topiccombo;
}

sub SubtopicCombo {
	my $self = shift;
	my $selected = shift;
	my %subtopics = Subtopics();
	my $subtopiccombo = "<select name='topic'>\n";
	foreach $subtopic (sort { $subtopics{$a}{topicnum} * 100 + $subtopics{$a}{num} <=> $subtopics{$b}{topicnum} * 100 + $subtopics{$b}{num} } keys %subtopics) {
		if ($selected eq $subtopic) {
			$subtopiccombo .= "<option value='$subtopic' selected>$subtopics{$subtopic}{topicnum}.$subtopics{$subtopic}{num}. $subtopics{$subtopic}{topicname}: $subtopics{$subtopic}{name}</option>\n";
		} else {
			$subtopiccombo .= "<option value='$subtopic'>$subtopics{$subtopic}{topicnum}.$subtopics{$subtopic}{num}. $subtopics{$subtopic}{topicname}: $subtopics{$subtopic}{name}</option>\n";
		}
	}
	$subtopiccombo .= "</select>\n";
	return $subtopiccombo;
}

sub FormatCombo {
	my $self = shift;
	my $selected = shift;
	my %formats = Formats();
	my $formatcombo = "<select name='format'>\n";
	foreach $format (sort keys %formats) {
		if ($selected eq $format) {
			$formatcombo .= "<option selected>$format</option>\n";
		} else {
			$formatcombo .= "<option>$format</option>\n";
		}
	}
	$formatcombo .= "</select>\n";
	return $formatcombo;
}

sub DTDCombo {
	my $self = shift;
	my $selected = shift;
	my %dtds = DTDs();
	my $dtdcombo = "<select name='dtd'>\n";
	foreach $dtd (sort keys %dtds) {
		if ($selected eq $dtd) {
			$dtdcombo .= "<option selected>$dtd</option>\n";
		} else {
			$dtdcombo .= "<option>$dtd</option>\n";
		}
	}
	$dtdcombo .= "</select>\n";
	return $dtdcombo;
}

sub UsersTable {
	my $table = "<table class='box'>\n";
	my %users = Users();
	$table .= "<tr><th>Username</th><th>Name</th><th>Email</th><th>Admin</th></tr>\n";
	foreach $key (sort { uc($users{$a}{username}) cmp uc($users{$b}{username}) } keys %users) {
		$table .= "<tr><td>" . a({href=>"user_edit.pl?user_id=$users{$key}{id}"},"$users{$key}{username}") . "</td>";
		$table .= "<td>$users{$key}{name}</td>\n";
		$table .= "<td>$users{$key}{email}</td>\n";
		$table .= "<td>" . bool2yn($users{$key}{admin}) . "</td>\n";
		$table .= "</tr>";
		$count++;
	}
	$table .= "</table>\n";
	return $table;
}

sub UserTable {
	my $self = shift;
	my $user_id = shift;
	my %user = User($foo, $user_id);
	my $table = '';
	$table .= "<table width='100%' class='box'>\n";
	$table .= "<form name=edit method=POST action='user_save.pl'>";
	$table .= "<input type=hidden name=user_id value=$user{id}></input>";
	$table .= "<tr><th colspan=2>User Details</th><th>Notes</th></tr>\n";
	$table .= "<tr><th>Username</th><td><input type=text name='username' size=30 value='$user{username}'></input></td>\n";
	$table .= "<td rowspan=5 style='width:100%'><textarea name='notes' style='width:100%' rows=10 wrap>$user{notes}</textarea></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr><th>First Name</th><td><input type=text name='first_name' size=30 value='$user{first_name}'></input></td></tr>\n";
	$table .= "<tr><th>Middle Name</th><td><input type=text name='middle_name' size=30 value='$user{middle_name}'></input></td></tr>\n";
	$table .= "<tr><th>Surname</th><td><input type=text name='surname' size=30 value='$user{surname}'></input></td></tr>\n";
	$table .= "<tr><th>Email</th><td><input type=text name='email' size=30 value='$user{email}'></input></td></tr>\n";
	if (&Admin()) {
		$table .= "<tr><th>Admin</th><td><select name='admin'>\n";
		if ($user{admin}) {
			$table .= "<option selected value='t'>Yes</option>\n";
			$table .= "<option value='f'>No</option>\n";
		} else {
			$table .= "<option value='t'>Yes</option>\n";
			$table .= "<option selected value='f'>No</option>\n";
		}
		$table .= "</select></td></tr>\n";
	}
	$table .= "<tr><th>New Password</th><td><input type=password name='password' size=12></input></td></tr>";
	$table .= "<tr><td></td><td><input type=submit value=Save></td></tr>";
	$table .= "</form>";
	$table .= "</table>";
	return $table;
}

sub UserDocsTable {
	my $self = shift;
	my $user_id = shift;
	my %docs = UserDocs($foo, $user_id);
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th>Title</th><th>Class</th><th>Doc Status</th><th>Role</th><th>Active</th><th>Feedback Email</th></tr>\n";
	foreach $doc (sort { uc($docs{$a}{title}) cmp uc($docs{$b}{title}) } keys %docs) {
		$table .= "<tr>";
		$table .= "<td valign=top><a href='document_edit.pl?doc_id=$docs{$doc}{id}'>$docs{$doc}{title}</a>\n";
		if ($docs{$doc}{url}) {
			$table .= " <a href=$docs{$doc}{url}>Go!</a>"
		}
		$table .= "</td>\n";
		$table .= "<td valign=top>$docs{$doc}{class}</td>\n";
		$table .= "<td valign=top>$docs{$doc}{pub_status_name}</td>\n";
		$table .= "<td valign=top>$docs{$doc}{role}</td>\n";
		$table .= "<td valign=top>" . &bool2yn($docs{$doc}{active}) . "</td>\n";
		$table .= "<td valign=top>$docs{$doc}{email}</td>\n";
		$table .= "</tr>\n";
	}
	$table .= "</table>\n";
	return $table;
}

sub UserNotesTable {
	my ($self, $user_id) = @_;
	my %usernotes = UserNotes($foo, $user_id);
	my $table = "<table class='box'>\n";
	$table .= "<form name=notes method=POST action='user_note_add.pl'>\n";
	$table .= "<tr><th colspan=3>User Notes</th></tr>\n";
	$table .= "<tr><th>Date and Time</th><th>User</th><th>Notes</th></tr>\n";
	foreach $date_entered (sort keys %usernotes) {
		$table .= "<tr>\n";
		$table .= "<td valign=top>$date_entered</td>\n";
		$table .= "<td valign=top>$usernotes{$date_entered}{username}</td>\n";
		$table .= "<td valign=top>$usernotes{$date_entered}{notes}</td>\n";
		$table .= "</tr>\n";
	}
	$table .= "<tr><td colspan=2 align=right>To add a note, type the note, then click Save.</td>\n";
	$table .= "<td><textarea name=notes rows=10 cols=40 wrap></textarea>\n";
	$table .= "<input type=hidden name=user_id value=$user_id>\n";
	$table .= "<input type=submit value='Save'></td>\n";
	$table .= "</tr>";
	$table .= "</table>\n";
	$table .= "</form>";
	return $table;
}

sub DocTable {
	my $self = shift;
	my $doc_id = shift;
	if ($doc_id) {
		my %doc = Doc($foo, $doc_id);
	} else {
		my %doc = ();
		$doc{dtd} = "DocBook";
		$doc{format} = "XML";
	}
	my $doctable = '';
	$doctable .= "<table style='width:100%' class='box'>\n";
	if ($doc_id) {
		$doctable .= "<form method=POST action='document_save.pl' name='document'>\n";
	} else {
		$doctable .= "<form method=POST action='document_add.pl' name='document'>\n";
	}
	$doctable .= "<input name='doc_id' type=hidden value=$doc_id>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th colspan=6>Document Details</th>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th align=right>Title</th><td colspan=5><input type=text name=title size=60 style='width:100%' value='$doc{title}'></td>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th align=right>\n";
	if ($doc_id) {
		$doctable .= "<a href='document_wiki.pl?doc_id=$doc_id'>Filename</a>\n";
	} else {
		$doctable .= "Filename";
	}
	$doctable .= "</th><td colspan=5><input type=text name=filename size=60 style='width:100%' value='$doc{filename}'></td>\n";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right><a href='$url'>URL</a></th><td colspan=5><input type=text name=url size=60 style='width:100%' value='$doc{url}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right><a href='$ref_url'>Home</a></th><td colspan=5><input type=text name=ref_url size=60 style='width:100%' value='$doc{ref_url}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Status</th><td>";
	$doctable .= PubStatusCombo($foo, $doc{pub_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Class</th><td>\n";
	$doctable .= ClassCombo($foo, $doc{class});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Maintained</th><td>\n";
	if ($doc{maintained}) {
		$doctable .= 'Yes';
	} else {
		$doctable .= 'No';
	}
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Review Status</th><td>";
	$doctable .= ReviewStatusCombo($foo, $doc{review_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Tech Review</th><td>";
	$doctable .= TechReviewStatusCombo($foo, $doc{tech_review_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>License</th><td>";
	$doctable .= LicenseCombo($foo, $doc{license});
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Published</th><td><input type=text name=pub_date size=10 value='$doc{pub_date}'></td>";
	$doctable .= "<th align=right>Updated</th><td><input type=text name=last_update size=10 value='$doc{last_update}'></td>";
	$doctable .= "<th align=right>Version</th><td><input type=text name=version size=10 value='$doc{version}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Format</th><td>";
	$doctable .= FormatCombo($foo, $doc{format});
	$doctable .= "</td>";
	$doctable .= "<th align=right>DTD</th><td>";
	$doctable .= DTDCombo($foo, $doc{dtd});
	$doctable .= "</td>";
	$doctable .= "<th align=right>DTD Version</th><td>";
	$doctable .= "<input type=text name=dtd_version size=10 value='$doc{dtd_version}'>";
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Tickle Date</th><td><input type=text name=tickle_date size=10 value='$doc{tickle_date}'></td>";
	$doctable .= "<th align=right>ISBN</th><td><input type=text name=isbn size=14 value='$doc{isbn}'></td>";
	$doctable .= "<th align=right>Rating</th>\n";
	$doctable .= "<td>";
	$doctable .= BarGraphTable($foo, $doc{rating});
	$doctable .= "</td>\n";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Abstract</th>";
	$doctable .= "<td colspan=5><textarea name=abstract rows=6 cols=60 style='width:100%' wrap>$doc{abstract}</textarea></td>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr><td></td><td><input type=submit name=save value=Save></td></tr>\n";
	$doctable .= "</form>\n";
	$doctable .= "</table>\n";
	return $doctable;
}

sub PubStatusStatsTable{
	my $document_total = DocCount();
	my $sql = "SELECT pub_status_name, COUNT(*) FROM pub_status, document WHERE pub_status.pub_status = document.pub_status GROUP BY pub_status_name";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Publication Status Statistics</th></tr>\n";
	$table .= "<tr><th>Status</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n";
		$table .= "<th>" . $row[0] . "</th>\n";
		$table .= "<td align=right>" . $row[1] . "</td>\n";
		$pct = sprintf( '%3.2f', $row[1] / $document_total * 100 );
		$table .= "<td align=right>" . $pct . "%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $row[1];
	}
	$table .= "<tr><th>Total</th><td align=right>$total</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub LicenseStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT license, COUNT(*) FROM document WHERE pub_status = 'N' GROUP BY license";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>License Statistics</th></tr>\n";
	$table .= "<tr><th>License</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$license = $row[0];
		$license =~ s/\s+$//;
		$count   = $row[1];
		$table .= "<tr>\n";
		$table .= "<th>$license</th>\n";
		$table .= "<td align=right>$count</td>\n";
		$pct = sprintf( '%3.2f', $count / $active_count * 100 );
		$table .= "<td align=right>$pct%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $count;
	}
	$table .= "<tr><th>Total</th><td align=right>$total</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub FreeNonfreeStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT l.free, COUNT(*) FROM document d, license l WHERE d.license = l.license GROUP BY free";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		if ($row[0] eq 't') {
			$free_count = $row[1];
		} else {
			$nonfree_count = $row[1];
		}
	}
	my $unknown_count = $DB->Value("SELECT COUNT(*) FROM document WHERE license IS NULL OR license=''");
	my $free_pct = sprintf( '%3.2f', $free_count / $active_count * 100 );
	my $nonfree_pct = sprintf( '%3.2f', $nonfree_count / $active_count * 100 );
	my $unknown_pct = sprintf( '%3.2f', $unknown_count / $active_count * 100 );
	
	my $table = "<table classi'box'>\n";
	$table .= "<tr><th colspan=3>Free/NonFree Statistics</th></tr>\n";
	$table .= "<tr><th>Type</th><th align=right>Count</th><th align=right>Percent</th></tr>\n";
	$table .= "<tr><th>Free*</th><td align=right>$free_count</td><td align=right>$free_pct</td></tr>\n";
	$table .= "<tr><th>Non-Free</th><td align=right>$nonfree_count</td><td align=right>$nonfree_pct</td></tr>\n";
	$table .= "<tr><th>Unknown</th><td align=right>$unknown_count</td><td align=right>$unknown_pct</td></tr>\n";
	$table .= "<tr><th>Total</th><td align=right>$active_count</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub ClassStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT class_name, count(*) FROM class, document WHERE pub_status = 'N' and class.class = document.class group by class_name";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Classes</th></tr>\n";
	$table .= "<tr><th>Class</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n";
		$table .= "<th>" . $row[0] . "</th>\n";
		$table .= "<td align=right>" . $row[1] . "</td>\n";
		$pct = sprintf( '%3.2f', $row[1] / $active_count * 100 );
		$table .= "<td align=right>" . $pct . "%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $row[1];
	}
	$table .= "<tr><th>Total</th><td align=right>" . $total . "</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub FormatStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT format, count(*) FROM document WHERE pub_status = 'N' group by format";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Format Statistics</th></tr>\n";
	$table .= "<tr><th>Format</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n";
		$table .= "<th>" . $row[0] . "</th>\n";
		$table .= "<td align=right>" . $row[1] . "</td>\n";
		$pct = sprintf( '%3.2f', $row[1] / $active_count * 100 );
		$table .= "<td align=right>" . $pct . "%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $row[1];
	}
	$table .= "<tr><th>Total</th><td align=right>" . $total . "</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub DTDStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT dtd, count(*) FROM document WHERE pub_status = 'N' group by dtd";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>DTD Statistics</th></tr>\n";
	$table .= "<tr><th>DTD</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n";
		$table .= "<th>" . $row[0] . "</th>\n";
		$table .= "<td align=right>" . $row[1] . "</td>\n";
		$pct = sprintf( '%3.2f', $row[1] / $active_count * 100 );
		$table .= "<td align=right>" . $pct . "%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $row[1];
	}
	$table .= "<tr><th>Total</th><td align=right>" . $total . "</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub FormatDTDStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT format, dtd, count(*) FROM document WHERE pub_status = 'N' group by format, dtd";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=4>Format and DTD Statistics</th></tr>\n";
	$table .= "<tr><th>Format</th><th>DTD</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$format = $row[0];
		$dtd    = $row[1];
		$count  = $row[2];
		$pct = sprintf( '%3.2f', $count / $active_count * 100 );
		$table .= "<tr>\n";
		$table .= "<th>$format</th>\n";
		$table .= "<th>$dtd</th>\n";
		$table .= "<td align=right>$count</td>\n";
		$table .= "<td align=right>" . $pct . "%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $count;
	}
	$table .= "<tr><th>Total</th><td></td><td align=right>" . $total . "</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub DetailedStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $sql = "SELECT class, dtd, format, count(*) FROM document WHERE pub_status = 'N' group by class, dtd, format";
	my $recordset = $DB->Recordset($sql);
	my $total = 0;
	my $table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=4>Detailed Statistics</th></tr>\n";
	$table .= "<tr><th>Class</th><th>DTD</th><th>Format</th><th>Count</th><th>Percent</th></tr>";
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n";
		$table .= "<th>" . $row[0] . "</th>\n";
		$table .= "<th>" . $row[1] . "</th>\n";
		$table .= "<th>" . $row[2] . "</th>\n";
		$table .= "<td align=right>" . $row[3] . "</td>\n";
		$pct = sprintf( '%3.2f', $row[3] / $active_count * 100 );
		$table .= "<td align=right>" . $pct . "%</td>\n";
		$table .= "</tr>\n";
		$total = $total + $row[3];
	}
	$table .= "<tr><th>Total</th><td></td><td></td><td align=right>" . $total . "</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub MiscStatsTable {
	use Date::Calc qw(:all);
	my $sql = "SELECT last_update FROM document WHERE pub_status='N'";
	my $recordset = $DB->Recordset($sql);
	my $count = 0;
	my $avg_age   = 0;
	my ($year2, $month2, $day2) = Today();
	while (@row = $recordset->fetchrow) {
		my $last_update = $row[0];
		if (($last_update) && ($last_update ne "1970-01-01" )) {
			my $year1 = substr($last_update,0,4);
			my $month1 = substr($last_update,5,2);
			my $day1 = substr($last_update,8,2);
			my $age = Delta_Days($year1, $month1, $day1, $year2, $month2, $day2);
			if ($count) {
				$avg_age = (($avg_age * ($count - 1)) + $age) / $count;
			} else {
				$avg_age = $age;
			}
			$count++;
		}
	}
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=2>Miscellaneous Statistics</th></tr>";
	$table .= "<tr><th>Statistic</th><th>Value</th></tr>";
	$table .= "<tr><th>Average Age Since Last Update</th><td>&nbsp;";
	$table .= sprintf("%i", $avg_age);
	$table .= " days</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub BarGraphTable {
	my ($self, $value) = @_;
	my $graph = '';
	if ($value) {
		$graph .= "<table class='bargraph'>\n";
		for ( $i = 1; $i <= 10; $i++ ) {
			$graph .= "<td class='";
			if ( $value >= $i ) { $graph .= "baron" } else { $graph .= "baroff" }
			$graph .= "'>&nbsp;&nbsp;</td>\n";
		}
		$graph .= "</tr></table>\n";
	} else {
		$graph .= "Not rated";
	}
	return $graph;
}

sub DocVersionsTable {
	my ($self, $doc_id) = @_;
	my $table = '';
	my %docversions = DocVersions($foo, $doc_id);
	
	$table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=6>Document Versions</th></tr>\n";
	$table .= "<tr><th>Version</th><th>Date</th><th>Initials</th><th>Notes</th></tr>";
	foreach $key (sort { $docversions{$a}{pub_date} cmp $docversions{$b}{pub_date} } keys %docversions) {
		$table .= "<tr>";
		$table .= "<form method=POST action='document_rev_save.pl'>";
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
		$table .= "<input type=hidden name=rev_id value=$docversions{$key}{rev_id}>";
		$table .= "<input type=hidden name=doc_id value=$doc_id>";
		$table .= "<td valign=top><input type=text name=version width=12 size=12 value='$docversions{$key}{version}'></input></td>\n";
		$table .= "<td valign=top><input type=text name=pub_date width=12 size=12 value='$docversions{$key}{pub_date}'></input></td>\n";
		$table .= "<td valign=top><input type=text name=initials width=5 size=5 value='$docversions{$key}{initials}'></input></td>\n";
		$table .= "<td><textarea name=notes rows=3 cols=40 style='width:100%' wrap>$docversions{$key}{notes}</textarea>\n";
		$table .= "<td valign=top><input type=checkbox name=chkDel>Del</td>";
		$table .= "<td valign=top><input type=submit value=Save></td>\n";
		$table .= "</form>";
		$table .= "</tr>\n";
	}

	$table .= "<tr>";
	$table .= "<form method=POST action='document_rev_add.pl'>";
	$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
	$table .= "<input type=hidden name=doc_id value=$doc_id>";

	$table .= "<td valign=top><input type=text name=version width=12 size=12></input></td>\n";
	$table .= "<td valign=top><input type=text name=pub_date width=12 size=12></input></td>\n";
	$table .= "<td valign=top><input type=text name=initials width=5 size=5></input></td>\n";
	$table .= "<td><textarea name=notes rows=3 cols=40 style='width:100%' wrap></textarea>\n";

	$table .= "<td valign=top></td>\n";
	$table .= "<td valign=top><input type=submit value=Add></td>\n";
	$table .= "</form>";
	$table .= "</tr>\n";

	$table .= "</table>\n";
	return $table;
}

sub DocUsersTable {
	my ($self, $doc_id) = @_;
	my $table = '';
	my %docusers = DocUsers($foo, $doc_id);
	
	$table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=6>Document Contributors</th></tr>\n";
	$table .= "<tr><th>Status</th><th>Role</th><th>Name</th><th>Feedback Email</th><th colspan=2>Action</th></tr>";
	foreach $key (sort keys %docusers) {
		$table .= "<tr>";
		$table .= "<form method=POST action='document_user_save.pl'>";
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
		$table .= "<input type=hidden name=doc_id value=$doc_id>";
		$table .= "<input type=hidden name=user_id value=$docusers{$key}{id}>";

		$table .= '<td valign=top><select name="active">';
		if ($docusers{$key}{active}) {
			$table .= '<option selected value="t">Active</option>';
			$table .= '<option value="f">Inactive</option>';
		} else {
			$table .= '<option value="t">Active</option>';
			$table .= '<option selected value="f">Inactive</option>';
		}
		$table .= "</select></td>";

		$table .= "<td valign=top>";
		$table .= RoleCombo($foo, $docusers{$key}{role});
		$table .= "</td>\n";

		$table .= "<td valign=top><a href='user_edit.pl?user_id=$docusers{$key}{id}'>$docusers{$key}{name}</a></td>\n";
		$table .= "<td valign=top><input type=text name=email width=20 size=20 value='$docusers{$key}{email}'></input></td>\n";
		$table .= "<td valign=top><input type=checkbox name=chkDel>Del</td>";
		$table .= "<td valign=top><input type=submit value=Save></td>\n";
		$table .= "</form>";
		$table .= "</tr>\n";
	}

	# For assigning a new contributor
	$table .= "<tr>";
	$table .= "<form method=POST action='document_user_add.pl'>";
	$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
	$table .= "<input type=hidden name=doc_id value=$doc_id>";

	$table .= '<td valign=top><select name="active">';
	$table .= '<option value="t">Active</option>';
	$table .= '<option value="f">Inactive</option>';
	$table .= "</select></td>";

	$table .= "<td valign=top>";
	$table .= RoleCombo();
	$table .= "</td>\n";

	$table .= "<td valign=top>";

	$sql = "SELECT user_id, first_name, middle_name, surname FROM username ORDER BY first_name, middle_name, surname";
	$authors_result = $DB->Recordset($sql);

	$table .= "<select name=user_id\n";
	$table .= "<option>\n";
	while (@row = $authors_result->fetchrow) {
		$user_id = $row[0];
		$first_name	= &trim($row[1]);
		$middle_name	= &trim($row[2]);
		$surname	= &trim($row[3]);
		$name = &trim(&trim("$first_name $middle_name") . " " . $surname);
		$table .= "<option value=$user_id>$name</option>\n"
	}
	$table .= "</select>\n";
	$table .= "</td>\n";

	$table .= "<td valign=top><input type=text name=email width=20 size=20></td>\n";
	$table .= "<td valign=top></td>\n";
	$table .= "<td valign=top><input type=submit value=Add></td>\n";
	$table .= "</form>";
	$table .= "</tr>\n";

	$table .= "<tr><td colspan=5><small>Note: Deleting a record here doesn't delete the user. It only deletes the association between the user and this document.</small></td></tr>\n";
	$table .= "</table>\n";
}

sub DocTopicsTable {
	my ($self, $doc_id) = @_;
	my %doctopics = DocTopics($foo, $doc_id);
	my $table = "<table class='box'>";
	$table .= "<tr><th colspan=2>Document Topics</th></tr>\n";
	$table .= "<tr><th>Topic</th><th>Action</th></tr>\n";
	foreach $key (keys %doctopics) {
  		$table .= "<tr>\n";
		$table .= "<form method=POST action='document_topic_del.pl'>\n";
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
		$table .= "<input type=hidden name=doc_id value=$doc_id>";
		$table .= "<input type=hidden name=topic_num value=$doctopics{$key}{topic_num}>";
		$table .= "<input type=hidden name=subtopic_num value=$doctopics{$key}{subtopic_num}>";
		$table .= "<td>$doctopics{$key}{topic_num}.$doctopics{$key}{subtopic_num} $doctopics{$key}{topic_name}: $doctopics{$key}{subtopic_name}</td>";
		$table .= "<td valign=top><input type=submit value=Delete></td>\n";
		$table .= "</form>\n";
		$table .= "</tr>\n";
	}
	$table .= "<tr>";
	$table .= "<form method=POST action='document_topic_add.pl'>";
	$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
	$table .= "<input type=hidden name=doc_id value=$doc_id>";
	$table .= "<td valign=top>\n";
	$table .= SubtopicCombo();
	$table .= "</td>\n";
	$table .= "<td valign=top><input type=submit value=Add></td>\n";
	$table .= "</form>\n";
	$table .= "</tr></table>\n";
	return $table;
}

sub DocRatingTable {
	my ($self, $doc_id) = @_;
	my $vote_count	= $DB->Value("SELECT COUNT(*) FROM doc_vote WHERE doc_id=$doc_id");
	my $vote	= $DB->Value("SELECT vote FROM doc_vote WHERE doc_id=$doc_id AND user_id=" . CurrentUserID());
	$table .= "<table class='box'><tr><th colspan=3>Document Rating</th></tr>\n";
	$table .= "<form action='document_vote_save.pl' method=POST>\n";
	$table .= "<input type=hidden name=doc_id value=$doc_id>\n";
	$table .= "<tr><th>Ratings</th><td>$vote_count</td>\n";
	$table .= "<td rowspan=3>\n";
	$table .= "You can rate each document on a scale from 1 to 10, where 1 is very poor and 10 is excellent.\n";
	$table .= "Your vote is averaged with the votes of others to obtain a rating for the document.\n";
	$table .= "</td>\n";
	$table .= "</tr>\n";
	$table .= "<tr><th>Average</th><td>" . BarGraphTable($foo, $doc{rating}) . "</td></tr>\n";
	$table .= "<tr><th>Your Rating</th><td><input name=vote type=text size=2 width=2 value=$vote></input>\n";
	$table .= "<input type=submit value='Rate'></td>\n";
	$table .= "</form>";
	$table .= "</tr></table>";
	return $table;	
}

sub DocNotesTable {
	my ($self, $doc_id) = @_;
	my %docnotes = DocNotes($foo, $doc_id);
	my $table = "<table class='box'>\n";
	$table .= "<form name=notes method=POST action='document_note_add.pl'>\n";
	$table .= "<tr><th colspan=3>Document Notes</th></tr>\n";
	$table .= "<tr><th>Date and Time</th><th>User</th><th>Notes</th></tr>\n";
	foreach $date_entered (sort keys %docnotes) {
		$table .= "<tr>\n";
		$table .= "<td valign=top>$date_entered</td>\n";
		$table .= "<td valign=top>$docnotes{$date_entered}{username}</td>\n";
		$table .= "<td valign=top>$docnotes{$date_entered}{notes}</td>\n";
		$table .= "</tr>\n";
	}
	$table .= "<tr><td colspan=2 align=right>To add a note, type the note, then click Save.</td>\n";
	$table .= "<td><textarea name=notes rows=10 cols=40 wrap></textarea>\n";
	$table .= "<input type=hidden name=doc_id value=$doc_id>\n";
	$table .= "<input type=submit value='Save'></td>\n";
	$table .= "</tr>";
	$table .= "</table>\n";
	$table .= "</form>";
	return $table;
}

sub TopicsTable {
	my $self = shift;
	my %topics = Topics();
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Topics</th></tr>\n";
	foreach $topic_num (sort { $a <=> $b } keys %topics) {
		$table .= "<tr><td align='right'>" . $topics{$topic_num}{num} . "</td>\n";
		$table .= "<td><a href='subtopic_list.pl?topic_num=$topic_num'>$topics{$topic_num}{name}</a></td>\n";
		$table .= "<td>$topics{$topic_num}{description}</td></tr>\n";
	}
	$table .= "</table>\n";
	return $table;
}

sub SubtopicsTable {
	my ($self, $topic_num) = @_;
	my %subtopics = Subtopics($foo, $topic_num);
	my %topic = Topic($foo, $topic_num);
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>$topic{name}</th></tr>\n";
	foreach $subtopic_num (sort { $subtopics{$a}{num} <=> $subtopics{$b}{num} } keys %subtopics) {
		$table .= "<tr><td align='right'>" . $subtopics{$subtopic_num}{num} . '</td><td>' . $subtopics{$subtopic_num}{name} . "</td>\n";
		$table .= "<td>$subtopics{$subtopic_num}{description}</td></tr>\n";
	}
	$table .= "</table>\n";
	return $table;
}

sub ErrorsTable {
	my $message = '';
	if (scalar @errors) {
		print "<table><tr><td>\n";
		while (scalar @errors) {
			my $error = pop @errors;
			$message = $error . "<p>" . $message;
		}
		print "<p>$message\n";
		print "</td></tr></table>\n";
	}
}

sub NavBar {
	print "<table class='navbar'><tr>\n";
	print "<th><a href='document_list.pl'>Documents</a></th>\n";
	print "<th><a href='topic_list.pl'>Topics</a></th> \n";
	print "</tr>\n";
	print "</table>\n";
}

sub NavBox {
	print "<table class='navbox'>\n";
	print "<tr><th>Menu</th></tr>\n";
	print "<tr><td><a href='document_list.pl'>Document Table</a></td></tr>\n";
	print "<tr><td><a href='statistics.pl'>Statistics</a></td></tr>\n";
	print "</table>\n";
}

sub TopicsBox {
	my %topics = Topics();
	my %subtopics = Subtopics();
	print "<table class='navbox'>\n";
	print "<tr><th>Topics</th></tr>\n";
	print "<tr><td>\n";
	foreach $topic_num (sort { $a <=> $b } keys %topics) {
		print "<a href='topic_doc_list.pl?topic_num=$topic_num'>$topics{$topic_num}{name}</a><br>\n";
		foreach $subtopic_num (sort { $subtopics{$a}{num} <=> $subtopics{$b}{num} } keys %subtopics) {
			if ($subtopics{$subtopic_num}{topicnum} == $topic_num) {
				print "&nbsp;&nbsp;&nbsp;&nbsp;<a href='subtopic_doc_list.pl?subtopic_num=$subtopic_num'>$subtopics{$subtopic_num}{name}</a><br>\n";
			}
		}
	}
	print "</td></tr>\n";
	print "</table>\n";
}

sub TitleBox {
	my $title = shift;
	print "<table width='100%'><tr>\n";
	print "<td><h1>$title</h1></td>\n";
	print "<td align=right>\n";
	if ($currentuser_id) {
		print "<a href='user_edit.pl?user_id=$currentuser{id}'>$currentuser{name}</a> ";
		if (Admin()) {
			print "(Administrator) ";
		} elsif (Maintainer()) {
			print "(Maintainer) ";
		}
		print "<br><a href='logout.pl'>Log out</a>\n";
	}
	print "</td></tr></table>\n";
}

sub LoginBox {
	print "<table class='navbox'>\n";
	print "<form name='login' action='login.pl' method=POST>\n";
	print "<tr><th colspan=2>Log In</th></tr>\n";
	print "<tr>\n";
	print "<td colspan=2 align=center>\n";
	print "<a href='newuser.pl'>Create Account</a>";
	print "</td>\n";
	
	print "<tr>\n";
	print "<td align=right>Username</td>\n";
	print "<td><input type=text size=12 name=username></input></td>\n";
	print "</tr>\n";
	print "<tr>\n";
	print "<td align=right>Password</td>\n";
	print "<td><input type=password size=12 name=password></input></td>\n";
	print "</tr>\n";
	print "<tr>\n";
	print "<td colspan=2 align=center>\n";
	print "<input type=submit name='login' value='Login'>\n";
	print "<input type=submit name='mailpass' value='Mail Password'>\n";
	print "</td>\n";
	print "</tr>\n";
	print "</form>\n";
	print "</table>\n";
}

sub AdminBox {
	return unless Admin();
	print "<p><table class='navbox'>\n";
	print "<tr><th>Admin Tools</th></tr>\n";
	print "<tr><td><a href='user_list.pl'>Users</a></t></tr>\n";
	print "<tr><td><a href='document_new.pl'>New Document</a></td></tr>\n";
	print "<tr><td><a href='topic_list.pl'>Edit Topics</a></td></tr>\n";
	print "</td></tr></table>\n";
}

sub Login {
	use String::Random;
	my $self = shift;
	my $title = shift;
	my $username = $CGI->param('username');
	push @errors, "Param('username'): " . $username if ($debug);
	my $password = $CGI->param('password');
	push @errors, "Param('password'): " . $password if ($debug);
	my $count = $DB->Value("SELECT COUNT(*) FROM username WHERE username='$username'");
	if ($count) {
		push @errors, "Found the user" if ($debug);
		my $foundpw = $DB->Value("SELECT password FROM username WHERE username='$username'");
		if ($password eq $foundpw) {

			push @errors, "Password matched" if ($debug);
			# Load settings, since cookie won't be read until the next page
			#
			$currentuser_id = $DB->Value("SELECT user_id FROM username WHERE username='$username'");
			%currentuser = User($foo, $currentuser_id);

			# If there is already a session_id, reuse it. This is so if they log on from multiple
			# computers their session id doesn't get clobbered.
			#
			my $session_id = $DB->Value("SELECT session_id FROM username WHERE user_id=$currentuser_id");
			unless ($session_id) {
				my $sessiongen = new String::Random;
				$sessiongen->{A} = ['A'..'Z', 'a'..'z'];
				$session_id = $sessiongen->randpattern('AAAAAAAAAAAAAAAAAAAA');
				$DB->Exec("UPDATE username SET session_id='$session_id' WHERE username='$username'");
			}

			my $cookie_domain = Config($foo, 'cookie_domain');
			
			# Set Cookie
			# 
			my $cookie=$CGI->cookie(
				-name    => 'lampadas_session',
				-value   => $session_id,
				-expires => '+1M'
			);
			StartPage($foo, $title, $cookie);
			return 0;
		} else {
			StartPage($foo, 'Invalid password');
			return 1;
		}
	} else {
		StartPage($foo, 'Invalid username');
		return 1;
	}
}

sub Logout {
	my $self = shift;
	my $title = shift;
	my $cookie = $CGI->cookie(-name => 'lampadas_session', -value => '');
	$currentuser_id = 0;
	%currentuser = ();
	StartPage($foo, $title, $cookie);
}

sub AddUser {
	use String::Random;
	my $self = shift;
	my ($username, $first_name, $middle_name, $surname, $email, $admin, $password) = @_;
	unless ($password) {
		my $pwgen = new String::Random;
		$pwgen->{A} = ['A'..'Z', 'a'..'z'];
		$password = $pwgen->randpattern('AAAAAAAA');
		Mail($foo, $email, 'Lampadas Password', "Your Lampadas password is $password");
	}
	my @row = $DB->Row("SELECT MAX(user_id) FROM username");
	my $user_id=  $row[0];
	$user_id++;
	$DB->Exec("INSERT INTO username(user_id, username, first_name, middle_name, surname, email, admin, password) VALUES ($user_id, '$username', '$first_name', '$middle_name', '$surname', '$email', '$admin', '$password')");
	%newuser = User($foo, $user_id);
	return %newuser;
}

sub AddError {
	my ($self, $error) = @_;
	push @errors, $error;
}

sub Redirect {
	my $self = shift;
	my $url = shift;
	unless ($url =~ /http/) {
		my $hostname = Config($foo, 'hostname');
		my $rootdir = Config($foo, 'root_dir');
		$url = 'http://' . $hostname . $rootdir . $url;
	}
	print $CGI->redirect($url);
	exit;
}

sub Mail {
	use Mail::Sendmail;
	my $self = shift;
	my ($to, $subject, $message) = @_;
	my $from = Config($foo, 'local_email');
	my $smtp = Config($foo, 'smtp_server');
	my %mail = (to		=> $to,
		    from	=> $from,
		    subject	=> $subject,
		    message	=> $message,
		    smtp	=> $smtp);
	unless (&Mail::Sendmail::sendmail(%mail)) {
		push @errors, "Error sending mail"
	}
}

sub trim {
	my $temp = shift;
	$temp =~ s/^\s+//;
	$temp =~ s/\s+$//;
	return $temp;
}

sub yn2bool {
	my $temp = shift;
	if (($temp eq 't') or ($temp eq 'T')) {
		return 1;
	} else {
		return 0;
	}
}

sub bool2yn {
	my $temp = shift;
	if ($temp) {
		return 'Yes';
	} else {
		return 'No';
	}
}

sub wsq {
	my $temp = shift;
	$temp =~ s/'/''/g;
	if ($temp) {
		return "'$temp'";
	} else {
		return 'NULL';
	}
}

1;
