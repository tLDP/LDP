#!/usr/bin/perl
# 
# This package provides Perl bindings for the Lampadas database,
# routines for accessing the CGI environment,
# and HTML generators for creating the web front end.
# 
package Lampadas;

use Lampadas::Database;
use HTML::Entities;
use HTTP::SimpleLinkChecker;

use CGI qw(:standard);
use Exporter;

@ISA	= qw(Exporter);
@EXPORT	= qw(
	new,
	Param,
	Config,

	RequestedLanguage,
	CurrentUserID,
	CurrentUser,
	Admin,
	SysAdmin,
	Maintainer,

	Users,
	User,
	UserDocs,
	UserFiles,
	UserNotes,
	AddUserNote,

	Docs,
	Doc,
	AddDoc,
	SaveDoc,
	Lintadas,
	LintadasDoc,

	DocFiles,
	AddDocFile,
	SaveDocFile,
	DocErrors,
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
	SaveTopic,
	Subtopics,
	SaveSubtopic,
	Formats,
	DTDs,
	Stylesheets,
	Strings,
	String,
	AddString,
	SaveString,
	DelString,
	Errors,
	AddError,
	
	DocCount,
	DocCountByClass,
	DocCountByPubStatus,

	StartPage,
	EndPage,

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
	CSSCombo,

	UsersTable,
	UserTable,
	NewUserTable,
	UserDocsTable,
	UserNotesTable,
	DocsTable,
	DocTable,
	DocVersionsTable,
	DocErrorsTable,
	DocFilesTable,
	DocUsersTable,
	DocTopicsTable,
	DocRatingTable,
	DocNotesTable,
	StringsTable,
	ErrorsTable,
	TopicsTable,
	TopicTable,
	SubtopicsTable,
	TopicDocsTable,
	MessagesTable,
	NavBar,

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
	UserBox,
	TopicsBox,
	HeaderBox,
	LoginBox,
	AdminBox,
	EditImage,

	Login,
	Logout,
	AddUser,
	SaveUser,
	AddMessage,
	Mail,

	CVSUpdate,
);

$CGI	= new CGI;
$DB	= new Lampadas::Database;

# Initialize global variables
#
$VERSION = '0.1';
$currentuser_id = 0;
%currentuser = ();
&ReadCookie;

@messages = ();			# System messages, displayed on the next page
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

sub RequestedLanguage {
	my ($self, $languagestring) = @_;
	$languagestring = $CGI->http('Accept-language') unless ($languagestring);
	my @languages = split(/,/, $languagestring);
	my $langval, $maxlangval, $lang, $maxlang;
	$maxlang = 'EN';	# default to English
	$maxlangval = 0;
	foreach $language (@languages) {
		$lang = uc(substr($language,0,2));
		if ($DB->Value("SELECT COUNT(*) FROM class_i18n WHERE lang='$lang'")) {
			if ($language =~ /q=/) {
				$langval = $language;
				$langval =~ s/^.*q=//;
				if ($langval > $maxlangval) {
					$maxlangval = $langval;
					$maxlang = $lang;
				}
			} else {
				$maxlang = $lang;
				$maxlangval = 1;
			}
		}
	}
	return uc($maxlang);
}

sub CurrentUserID {
	return $currentuser_id;
}

sub CurrentUser {
	return %currentuser;
}

sub Admin {
	return 0 unless CurrentUserID();
	return 1 if (SysAdmin());
	return $currentuser{admin};
}

sub SysAdmin {
	return 0 unless CurrentUserID();
	return $currentuser{sysadmin};
}

sub Maintainer {
	return 0 unless (CurrentUserID());
	return 1 if (Admin());
	return 1 if (SysAdmin());
	return 1 if ($DB->Value("SELECT COUNT(*) FROM document_user WHERE active='t' AND user_id=" . CurrentUserID())); 
	return 0;
}

sub Users {
	my $self = shift;
	my %users = ();
	my $sql = "SELECT user_id, username, first_name, middle_name, surname, email, admin, sysadmin FROM username";
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
		$users{$user_id}{sysadmin}	= &yn2bool($row[7]);
	}
	return %users;
}

sub User {
	my $self = shift;
	my $user_id = shift;
	my %user = ();
	my $sql = "SELECT username, first_name, middle_name, surname, email, admin, sysadmin, notes, stylesheet FROM username WHERE user_id=$user_id";
	my @row = $DB->Row("$sql");
	$user{id}		= $user_id;
	$user{username}		= &trim($row[0]);
	$user{first_name}	= &trim($row[1]);
	$user{middle_name}	= &trim($row[2]);
	$user{surname}		= &trim($row[3]);
	$user{name}		= &trim(&trim($user{first_name} . ' ' . $user{middle_name}) . ' ' . $user{surname});
	$user{email}		= &trim($row[4]);
	$user{admin}		= &yn2bool($row[5]);
	$user{sysadmin}		= &yn2bool($row[6]);
	$user{notes}		= &trim($row[7]);
	$user{stylesheet}	= &trim($row[8]);
	return %user;
}

sub UserDocs {
	my ($self, $user_id) = @_;
	$user_id = 0 unless ($user_id);
	my %docs = ();
	my $sql = "SELECT d.doc_id, d.title, d.class_id, d.pub_status, d.url, ps.pub_status_name, du.role, du.active, du.email FROM document d, document_user du, pub_status ps WHERE d.doc_id=du.doc_id AND d.pub_status = ps.pub_status AND user_id=$user_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$doc_id				= $row[0];
		$docs{$doc_id}{id}		= $doc_id;
		$docs{$doc_id}{title}		= &trim($row[1]);
		$docs{$doc_id}{class_id}	= &trim($row[2]);
		$docs{$doc_id}{pub_status}	= &trim($row[3]);
		$docs{$doc_id}{url}		= &trim($row[4]);
		$docs{$doc_id}{pub_status_name}	= &trim($row[5]);
		$docs{$doc_id}{role}		= &trim($row[6]);
		$docs{$doc_id}{active}		= &yn2bool($row[7]);
		$docs{$doc_id}{email}		= &trim($row[8]);
	}
	return %docs;
}

sub UserFiles {
	my ($self, $user_id) = @_;
	my %userfiles = ();
	my $recordset = $DB->Recordset("SELECT df.doc_id, filename FROM document_file df, document_user du WHERE df.doc_id=du.doc_id AND du.user_id=$user_id AND du.active='t'");
	while (@row = $recordset->fetchrow) {
		$doc_id		= &trim($row[0]);
		$filename	= &trim($row[1]);
		$userfiles{$filename}{doc_id}	= $doc_id;
		$userfiles{$filename}{filename}	= $filename;
	}
	return %userfiles;
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
	my ($self) = @_;
	my %docs = ();
	my $sql = "SELECT doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating FROM document";
	my $result = $DB->Recordset($sql);
	while (@row = $result->fetchrow) {
		$doc_id	= $row[0];
		$docs{$doc_id}{id}			= &trim($row[0]);
		$docs{$doc_id}{title}			= &trim($row[1]);
		$docs{$doc_id}{class_id}		= &trim($row[2]);
		$docs{$doc_id}{format}			= &trim($row[3]);
		$docs{$doc_id}{dtd}			= &trim($row[4]);
		$docs{$doc_id}{dtd_version}		= &trim($row[5]);
		$docs{$doc_id}{version}			= &trim($row[6]);
		$docs{$doc_id}{last_update}		= &trim($row[7]);
		$docs{$doc_id}{url}			= &trim($row[8]);
		$docs{$doc_id}{isbn}			= &trim($row[9]);
		$docs{$doc_id}{pub_status}		= &trim($row[10]);
		$docs{$doc_id}{review_status}		= &trim($row[11]);
		$docs{$doc_id}{tickle_date}		= &trim($row[12]);
		$docs{$doc_id}{pub_date}		= &trim($row[13]);
		$docs{$doc_id}{ref_url}			= &trim($row[14]);
		$docs{$doc_id}{tech_review_status}	= &trim($row[15]);
		$docs{$doc_id}{maintained}		= &trim($row[16]);
		$docs{$doc_id}{license}			= &trim($row[17]);
		$docs{$doc_id}{abstract}		= &trim($row[18]);
		$docs{$doc_id}{rating}			= &trim($row[19]);
	}
	return %docs;
}

sub Doc {
	my $self = shift;
	my $doc_id = shift;
	my $sql = "SELECT doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating FROM document WHERE doc_id=$doc_id";
	my @row = $DB->Row("$sql");
	$doc{id}			= &trim($row[0]);
	$doc{title}			= &trim($row[1]);
	$doc{class_id}			= &trim($row[2]);
	$doc{format}			= &trim($row[3]);
	$doc{dtd}			= &trim($row[4]);
	$doc{dtd_version}		= &trim($row[5]);
	$doc{version}			= &trim($row[6]);
	$doc{last_update}		= &trim($row[7]);
	$doc{url}			= &trim($row[8]);
	$doc{isbn}			= &trim($row[9]);
	$doc{pub_status}		= &trim($row[10]);
	$doc{review_status}		= &trim($row[11]);
	$doc{tickle_date}		= &trim($row[12]);
	$doc{pub_date}			= &trim($row[13]);
	$doc{ref_url}			= &trim($row[14]);
	$doc{tech_review_status}	= &trim($row[15]);
	$doc{maintained}		= &trim($row[16]);
	$doc{license}			= &trim($row[17]);
	$doc{abstract}			= &trim($row[18]);
	$doc{rating}			= &trim($row[19]);
	return %doc;
}

sub AddDoc {
	my ($self, $title, $class_id, $format, $dtd, $dtd_version, $version, $last_update, $url, $isbn, $pub_status, $review_status, $tickle_date, $pub_date, $ref_url, $tech_review_status, $maintained, $license, $abstract, $rating) = @_;
	my $doc_id = $DB->Value("SELECT MAX(doc_id) FROM document");
	$doc_id++;
	my $sql = "INSERT INTO document(doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating)";
	$sql .= " VALUES ($doc_id, " . wsq($title) . ", $class_id, " . wsq($format) . ", " . wsq($dtd) . ", " . wsq($dtd_version) . ", " . wsq($version) . ", " . wsq($last_update) . ", " . wsq($url) . ", " . wsq($isbn) . ", " . wsq($pub_status) . ", " . wsq($review_status) . ", " . wsq($tickle_date) . ", " . wsq($pub_date) . ", " . wsq($ref_url) . ", " . wsq($tech_review_status) . ", " . wsq($maintained) . ", " . wsq($license) . ", " . wsq($abstract) . ", " . wsq($rating) . ")";
	$DB->Exec($sql);
	$doc_id = $DB->Value("SELECT MAX(doc_id) FROM document");
	return $doc_id;
}

sub SaveDoc {
	my ($self, $doc_id, $title, $class_id, $format, $dtd, $dtd_version, $version, $last_update, $url, $isbn, $pub_status, $review_status, $tickle_date, $pub_date, $ref_url, $tech_review_status, $license, $abstract) = @_;
	my $sql = "UPDATE document SET";
	$sql .= "  title=" . wsq($title);
	$sql .= ", class_id=$class_id";
	$sql .= ", format=" . wsq($format);
	$sql .= ", dtd=" . wsq($dtd);
	$sql .= ", dtd_version=" . wsq($dtd_version);
	$sql .= ", version=" . wsq($version);
	$sql .= ", last_update=" . wsq($last_update);
	$sql .= ", url=" . wsq($url);
	$sql .= ", isbn=" . wsq($isbn);
	$sql .= ", pub_status=" . wsq($pub_status);
	$sql .= ", review_status=" . wsq($review_status);
	$sql .= ", tickle_date=" . wsq($tickle_date);
	$sql .= ", pub_date=" . wsq($pub_date);
	$sql .= ", ref_url=" . wsq($ref_url);
	$sql .= ", tech_review_status=" . wsq($tech_review_status);
	$sql .= ", license=" . wsq($license);
	$sql .= ", abstract=" . wsq($abstract);
	$sql .= " WHERE doc_id=$doc_id";
	$DB->Exec($sql);
}

sub Lintadas {
	my $self = @_;
	my %docs = Docs();
	foreach $doc_id (keys %docs) {
		LintadasDoc($foo, $doc_id);
	}
}

sub LintadasDoc {
	my ($self, $doc_id) = @_;
	my $cvsroot = Config($foo, 'cvs_root');

	$DB->Exec("DELETE from document_error WHERE doc_id=$doc_id");

	# Do not test deleted (D) documents. We just don't care about them.
	# 
	return if ($doc{pub_status} eq 'D');

	# Test document ref_url (canonical, home url)
	# 
	my $doc = Doc($foo, $doc_id);
	if ($doc{ref_url}) {
		my $code = HTTP::SimpleLinkChecker::check_link($doc{ref_url});
		unless ($code eq '200') {
			AddError($doc_id, "Home URL returns code $code");
		}
	}
	
	# Load meta-data from source files
	#
	$DB->Exec("UPDATE document SET format=NULL WHERE doc_id=$doc_id");
	$DB->Exec("UPDATE document SET dtd=NULL WHERE doc_id=$doc_id");
	$DB->Exec("UPDATE document SET dtd_version=NULL WHERE doc_id=$doc_id");
	my %docfiles = DocFiles($foo, $doc_id);
	foreach $key (keys %docfiles) {
		$DB->Exec("UPDATE document_file SET format=NULL WHERE doc_id=$doc_id AND filename=" . wsq($key));
		$filename = $cvsroot . $key;
		if (-e $filename) {
			if (-r $filename) {
				my $format = '';
				$fileext = $filename;
				$fileext =~ s/^.*\.//;
				if ($fileext =~ /SGML/i) {
					$format = 'SGML';
					$readmetadata = 1;
				} elsif ($fileext =~ /XML/i) {
					$format = 'XML';
					$readmetadata = 1;
				} elsif ($fileext =~ /WT/i) {
					$format = 'WIKI';
					$readmetadata = 0;
					$dtd = 'N/A';
					$dtd_version = '';
				} else {
					AddError($doc_id, "Unrecognized file format $format ($key)");
					next;
				}

				if ($readmetadata) {
					$dtd_version = `grep -i DOCTYPE $filename | head -n 1`;
					if ($dtd_version =~ /DocBook/i) {
						$dtd = "DocBook";
						$dtd_version =~ s/^.*?DocBook\s+//i;
						$dtd_version =~ s/\/\/.*//;
						$dtd_version =~ s/^XML\s*//;
						$dtd_version =~ s/^V//i;
					} elsif ($dtd_version =~ /LinuxDoc/i) {
						$dtd = "LinuxDoc";
						$dtd_version='';
					} else {
						$dtd = '';
						$dtd_version = '';
					}
				}
				$DB->Exec("UPDATE document_file SET format=" . wsq($format) . " WHERE doc_id=$doc_id AND filename=" . wsq($key));
				$DB->Exec("UPDATE document SET format=" . wsq($format) . " WHERE doc_id=$doc_id");
				$DB->Exec("UPDATE document SET dtd=" . wsq($dtd) . " WHERE doc_id=$doc_id");
				$DB->Exec("UPDATE document SET dtd_version=" . wsq($dtd_version) . " WHERE doc_id=$doc_id");
#				$DB->Exec("UPDATE document SET abstract=" . wsq($abstract) . " WHERE doc_id=$doc_id");
					
				unless (-w $filename) {
					$DB->Exec("INSERT INTO document_error(doc_id, error) VALUES ($doc_id, 'File not writable ($key)')");
				}
			} else {
				$DB->Exec("INSERT INTO document_error(doc_id, error) VALUES ($doc_id, 'File not readable ($key)')");
				$DB->Exec("UPDATE document_file SET format='' WHERE doc_id=$doc_id AND filename=" . wsq($key));
				$DB->Exec("UPDATE document SET format='' WHERE doc_id=$doc_id");
				$DB->Exec("UPDATE document SET dtd='' WHERE doc_id=$doc_id");
				$DB->Exec("UPDATE document SET dtd_version='' WHERE doc_id=$doc_id");
			}
		} else {
			$DB->Exec("INSERT INTO document_error(doc_id, error) VALUES ($doc_id, 'File not found ($key)')");
		}
	}
}

sub DocFiles {
	my ($self, $doc_id) = @_;
	my %docfiles = ();
	my $sql = "SELECT filename, format FROM document_file WHERE doc_id=$doc_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$filename	= &trim($row[0]);
		$format		= &trim($row[1]);
		$docfiles{$filename}{filename}	= $filename;
		$docfiles{$filename}{format}	= $format;
	}
	return %docfiles;
}

sub AddDocFile {
	my ($self, $doc_id, $filename) = @_;
	my $insecure = 0;
	$insecure++ if ($filename =~ /\.\./);
	unless ($insecure) {
		my $sql = "INSERT INTO document_file (doc_id, filename) VALUES ($doc_id, " . wsq($filename) . ")";
		$DB->Exec($sql);
	}
}

sub SaveDocFile {
	my ($self, $doc_id, $oldfilename, $filename) = @_;
	my $insecure = 0;
	$insecure++ if ($filename =~ /\.\./);
	my $root = $filename;
	unless ($insecure) {
		my $sql = "UPDATE document_file SET filename=" . wsq($filename) . " WHERE doc_id=$doc_id AND filename=" . wsq($oldfilename);
		$DB->Exec($sql);
	}
}

sub DelDocFile {
	my ($self, $doc_id, $oldfilename) = @_;
	my $sql = "DELETE FROM document_file WHERE doc_id=$doc_id AND filename=" . wsq($oldfilename);
	$DB->Exec($sql);
}

sub DocErrors {
	my ($self, $doc_id) = @_;
	my %docerrors = ();
	my $sql = "SELECT error FROM document_error WHERE doc_id=$doc_id";
	my $recordset = $DB->Recordset($sql);
	my $count = 0;
	while (@row = $recordset->fetchrow) {
		$count++;
		$docerrors{$count}{error} = &trim($row[0]);
	}
	return %docerrors;
}

sub DocUsers {
	my ($self, $doc_id) = @_;
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
	my $language = RequestedLanguage();
	my $sql = "SELECT class_id, lang, class_name, class_description FROM class_i18n WHERE lang=" . wsq($language);
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$class_id		= &trim($row[0]);
		$lang			= &trim($row[1]);
		$classname		= &trim($row[2]);
		$classdescription	= &trim($row[3]);
		$key			= $class_id;
		$classes{$key}{id}		= $class_id;
		$classes{$key}{lang}		= $lang;
		$classes{$key}{name}		= $classname;
		$classes{$key}{description}	= $classdescription;
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

sub SaveTopic {
	my ($self, $topic_num, $topic_name, $topic_description) = @_;
	$sql = "UPDATE topic SET topic_name=" . wsq($topic_name) . ", topic_description=" . wsq($topic_description) . " WHERE topic_num=$topic_num";
	$DB->Exec($sql);
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

sub SaveSubtopic {
	my ($self, $topic_num, $subtopic_num, $subtopic_name, $subtopic_description) = @_;
	$DB->Exec("UPDATE subtopic SET subtopic_name=" . wsq($subtopic_name) . ", subtopic_description=" . wsq($subtopic_description) . " WHERE topic_num=$topic_num AND subtopic_num=$subtopic_num");
}

sub Formats {
	my %formats = ();
	my $sql = "SELECT format, format_name FROM format";
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
	my $sql = "SELECT dtd FROM dtd";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$dtd		= &trim($row[0]);
		$dtds{$dtd}{dtd}	= $dtd;
	}
	return %dtds;
}

sub Stylesheets {
	my %stylesheets = ();
#	my @filenames = `cd css; ls *.css`;
	my @filenames = `cd ../css; ls *.css`;
	foreach $filename (@filenames) {
		$stylesheet = $filename;
		chomp $stylesheet;
		$stylesheets{$stylesheet}{stylesheet}	= $stylesheet;
	}
	return %stylesheets;
}

sub Strings {
	my ($self, $language) = @_;
	$language = RequestedLanguage() unless ($language);
	my %strings = ();
	my $sql = "SELECT string_id, lang, string FROM string_i18n WHERE lang='$language'";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$string_id	= $row[0];
		$lang		= $row[1];
		$string		= &trim($row[2]);
		$key		= $string_id . $lang;
		$strings{$key}{id}	= $string_id;
		$strings{$key}{lang}	= $lang;
		$strings{$key}{string}	= $string;
	}
	return %strings;
}

sub String {
	my ($self, $string_id) = @_;
	my $language = RequestedLanguage();
	my $string = $DB->Value("SELECT string FROM string_i18n WHERE string_id=$string_id AND lang='$language'");
	return $string;
}

sub AddString {
	my ($self, $lang, $string) = @_;
	my $string_id = $DB->Value("SELECT MAX(string_id) FROM string");
	$string_id++;
	$sql = "INSERT INTO string(string_id) VALUES($string_id)";
	$DB->Exec($sql);
	$sql = "INSERT INTO string_i18n(string_id, lang, string) VALUES($string_id, '$lang', " . wsq($string) . ")";
	$DB->Exec($sql);
}

sub SaveString {
	my ($self, $string_id, $lang, $string) = @_;
	$sql = "UPDATE string_i18n SET string=" .wsq($string) . " WHERE string_id=$string_id AND lang='$lang'";
	$DB->Exec($sql);
}

sub DelString {
	my ($self, $string_id, $lang) = @_;
	$sql = "DELETE FROM string_i18n WHERE string_id=$string_id AND lang='$lang'";
	$DB->Exec($sql);
	$sql = "DELETE FROM string WHERE string_id=$string_id";
	$DB->Exec($sql);
}

sub Errors {
	my %errors = ();
	my $sql = "SELECT doc_id, error FROM document_error";
	my $recordset = $DB->Recordset($sql);
	my $count = 0;
	while (@row = $recordset->fetchrow) {
		$doc_id	= &trim($row[0]);
		$error	= &trim($row[1]);
		$count++;
		$errors{$count}{doc_id}	= $doc_id;
		$errors{$count}{error}	= $error;
	}
	return %errors;
}

sub AddError {
	my ($doc_id, $error) = @_;
	$DB->Exec("INSERT INTO document_error(doc_id, error) VALUES ($doc_id, " . wsq($error) . " )");
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
	my ($self, $title, $cookie) = @_;

	if ($cookie) {
		print $CGI->header(-cookie=>$cookie,-expires=>'now');
		push @messages, "cookie: $cookie" if ($debug);
	} else {
		print $CGI->header(-expires=>'now');
	}

	my %user = CurrentUser();
	my $stylesheet = $user{stylesheet};
	$stylesheet = 'default' unless ($stylesheet);
	print "<html><head>\n";
	print "<title>Lampadas || $title</title>\n";
#	print "<link rel='stylesheet' href='css/default.css' type='text/css'>\n";
	print "<link rel='stylesheet' href='css/$stylesheet.css' type='text/css'>\n";
	print "</head>\n";
	print "<body><a name='top'>\n";

	if ($debug) {
		push @messages, "UserID: $currentuser_id";
		push @messages, "UserName: " . $currentuser{username};
	}

	print "<table style='width:100%' class='layout'>\n";
	print "<tr><td colspan=2>\n";
	HeaderBox($foo, $title);
	print "</td></tr>\n";
	if (scalar @messages) {
		print "<tr><td colspan=2>\n";
		MessagesTable();
		print "</td><tr>\n";
	}
	print "<tr><td valign=top width='200'>\n";
	LoginBox() unless ($currentuser_id);
	UserBox();
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
	print "<br>";
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
	my $language = RequestedLanguage();
	my %classes = Classes();
	my $classcombo = "<select name='class_id'>\n";
	foreach $class_id (sort { $classes{$a}{name} cmp $classes{$b}{name} } keys %classes) {
		if ($selected eq $class_id) {
			$classcombo .= "<option value='$class_id' selected>$classes{$class_id}{name}</option>\n";
		} else {
			$classcombo .= "<option value='$class_id'>$classes{$class_id}{name}</option>\n";
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
	$reviewstatuscombo .= "<option></option>\n";
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
	$reviewstatuscombo .= "<option></option>\n";
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
	$formatcombo .= "<option></option>\n";
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

sub StylesheetCombo {
	my ($self, $selected) = @_;
	my %stylesheets = Stylesheets();
	my $stylesheetcombo = "<select name='stylesheet'>\n";
	foreach $stylesheet (sort keys %stylesheets) {
		$stylesheet =~ s/\.css//;
		if ($selected eq $stylesheet) {
			$stylesheetcombo .= "<option selected>$stylesheet</option>\n";
		} else {
			$stylesheetcombo .= "<option>$stylesheet</option>\n";
		}
	}
	$stylesheetcombo .= "</select>\n";
	return $stylesheetcombo;
}

sub DTDCombo {
	my $self = shift;
	my $selected = shift;
	my %dtds = DTDs();
	my $dtdcombo = "<select name='dtd'>\n";
	$dtdcombo .= "<option></option>\n";
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
	$table .= "<tr><th>Username</th><th>Name</th><th>Email</th><th>Admin</th><th>SysAdmin</th></tr>\n";
	foreach $key (sort { uc($users{$a}{username}) cmp uc($users{$b}{username}) } keys %users) {
		$table .= "<tr><td>" . a({href=>"user_edit.pl?user_id=$users{$key}{id}"},"$users{$key}{username}") . "</td>";
		$table .= "<td>$users{$key}{name}</td>\n";
		$table .= "<td>$users{$key}{email}</td>\n";
		$table .= "<td>" . bool2yn($users{$key}{admin}) . "</td>\n";
		$table .= "<td>" . bool2yn($users{$key}{sysadmin}) . "</td>\n";
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
	$table .= "<tr><th colspan=2>User Details</th><th>Comments</th></tr>\n";
	$table .= "<tr><th>Username</th><td><input type=text name='username' size=20 value='$user{username}'></input></td>\n";
	$table .= "<td valign=top rowspan=12 style='width:100%'><textarea name='notes' style='width:100%' rows=10 wrap>$user{notes}</textarea></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr><th>First Name</th><td><input type=text name='first_name' size=20 value='$user{first_name}'></input></td></tr>\n";
	$table .= "<tr><th>Middle Name</th><td><input type=text name='middle_name' size=20 value='$user{middle_name}'></input></td></tr>\n";
	$table .= "<tr><th>Surname</th><td><input type=text name='surname' size=20 value='" . html($user{surname}) . "'></input></td></tr>\n";
	$table .= "<tr><th>Email</th><td><input type=text name='email' size=20 value='$user{email}'></input></td></tr>\n";
	$table .= "<tr><th>Stylesheet</th><td>";
	$table .= StylesheetCombo($foo, $user{stylesheet});
	$table .= "</td></tr>\n";
	$table .= "<tr><th>New Password</th><td><input type=password name='password' size=12></input></td></tr>";
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
		$table .= "<tr><th>SysAdmin</th><td><select name='sysadmin'>\n";
		if ($user{sysadmin}) {
			$table .= "<option selected value='t'>Yes</option>\n";
			$table .= "<option value='f'>No</option>\n";
		} else {
			$table .= "<option value='t'>Yes</option>\n";
			$table .= "<option selected value='f'>No</option>\n";
		}
		$table .= "</select></td></tr>\n";
	}
	$table .= "<tr><td></td><td><input type=submit value=Save></td></tr>";
	$table .= "</form>";
	$table .= "</table>";
	return $table;
}

sub NewUserTable {
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th>New User</th></tr>\n";
	$table .= "<tr><td>\n";
	$table .= "Welcome to the " . Config($foo, 'owner') . " Lampadas system.\n";

	$table .= "<p>To create a new user account, fill out this form.\n";

	$table .= "<p><form name='newuser' action='user_add.pl' method='POST'>\n";
	$table .= "<table>\n";
	$table .= "<tr>\n";
	$table .= "<td align=right>*Username</td>\n";
	$table .= "<td><input type=text name=username size=20></input></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr>\n";
	$table .= "<td align=right>*Enter your email address.<br>Your password will be mailed to this address, so it must be valid.</td>\n";
	$table .= "<td><input type=text name=email size=20></input></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr>\n";
	$table .= "<td align=right>First Name</td>\n";
	$table .= "<td><input type=text name=first_name size=20></input></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr>\n";
	$table .= "<td align=right>Middle Name</td>\n";
	$table .= "<td><input type=text name=middle_name size=20></input></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr>\n";
	$table .= "<td align=right>Surname</td>\n";
	$table .= "<td><input type=text name=surname size=20></input></td>\n";
	$table .= "</tr>\n";
	$table .= "<tr>\n";
	$table .= "<td></td><td><input type=submit value='Create Account!'></td>\n";
	$table .= "</tr>\n";
	$table .= "</table\n";
	$table .= "</form>\n";

	$table .= "<p>*Required Fields\n";
	$table .= "</td></tr></table>\n";
	return $table;
}

sub UserDocsTable {
	my $self = shift;
	my $user_id = shift;
	my %docs = UserDocs($foo, $user_id);
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=6>User Documents</th></tr>\n";
	$table .= "<tr><th>Title</th>";
	$table .= "<th>Status</th>";
	$table .= "<th>Role</th>";
	$table .= "<th>Active</th>";
	$table .= "<th>Feedback Email</th></tr>\n";
	foreach $doc (sort { uc($docs{$a}{title}) cmp uc($docs{$b}{title}) } keys %docs) {
		$table .= "<tr>";
		$table .= "<td valign=top>";
		$table .= "<a href='document_edit.pl?doc_id=$docs{$doc}{id}'>" . EditImage() . "</a>";
		if ($docs{$doc}{url}) {
			$table .= "<a href='$docs{$doc}{url}'>$docs{$doc}{title}</a>";
		} else {
			$table .= "$docs{$doc}{title}";
		}
		$table .= "</td>\n";
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
	my $table = "<table style='width:100%' class='box'>\n";
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
	$table .= "<td><textarea name=notes style='width:100%' rows=10 wrap></textarea>\n";
	$table .= "<input type=hidden name=user_id value=$user_id>\n";
	$table .= "<input type=submit value='Save'></td>\n";
	$table .= "</tr>";
	$table .= "</table>\n";
	$table .= "</form>";
	return $table;
}

sub DocsTable {
	my ($self) = @_;
	my %docs = Docs();
	my %userdocs = UserDocs($foo, CurrentUserID());
	my %classes = Classes();
	my %pubstatuses = PubStatuses();
	my %reviewstatuses = ReviewStatuses();
	
	my $mypub_status = Param($foo,'strSTATUS');
	$mypub_status = "N" unless ($mypub_status);
	my %myclasses = ();
	foreach $class_id (keys %classes) {
		$param = "chkCLASS" . $class_id;
		if (Param($foo, "$param") eq 'on') {
			$myclasses{$class_id} = 1;
		}
	}

	# Optional Fields
	#
	$chkSTATUS       = Param($foo,'chkSTATUS');
	$chkCLASS        = Param($foo,'chkCLASS');
	$chkFORMAT       = Param($foo,'chkFORMAT');
	$chkDTD          = Param($foo,'chkDTD');
	$chkPUBDATE      = Param($foo,'chkPUBDATE');
	$chkLASTUPDATE   = Param($foo,'chkLASTUPDATE');
	$chkTICKLEDATE   = Param($foo,'chkTICKLEDATE');
	$chkREVIEWSTATUS = Param($foo,'chkREVIEWSTATUS');
	$chkTECHSTATUS   = Param($foo,'chkTECHSTATUS');
	$chkURL          = Param($foo,'chkURL');
	$chkMAINTAINED   = Param($foo,'chkMAINTAINED');
	$chkLICENSE      = Param($foo,'chkLICENSE');
	$chkVERSION      = Param($foo,'chkVERSION');
	$chkRATING       = Param($foo,'chkRATING');

	$SORT	= Param($foo,'strSORT');
	$SORT	= "title" unless ($SORT);

	$strSTATUS = Param($foo,'strSTATUS');

	# if we're not reloading, or aren't a maintainer, the default is to show only Active ('N') documents.
	unless (($reload eq 'Reload') or (Maintainer())) {
		$strSTATUS = 'N';
	}

	$reload = Param($foo,'Reload');

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
	$RATING = "";

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
	if ( $chkRATING eq "on" ) { $RATING = "checked "; }

	my $table = '';

	$table .= "<table style='width:100%' class='box'>\n";
	$table .= "<form name=filter method=POST action='document_list.pl'>";
	$table .= "<tr><th>Classes</th><th>Optional Fields</th><th>Sort By</th>";
	$table .= "<th>Status</th>" if (Maintainer());
	$table .= "</tr>";
	$table .= "<tr><td align=center valign=top>\n";
	$table .= "<table><tr><td>";
	foreach $class_id (sort { $classes{$a}{name} cmp $classes{$b}{name} } keys %classes) {
		my $name = 'chkCLASS' . $class_id;
		my $value = Param($foo, $name);
		if ($value eq 'on') {
			$table .= "<input type='checkbox' checked name='$name'>$classes{$class_id}{name}<br>\n";
		} else {
			$table .= "<input type='checkbox' name='$name'>$classes{$class_id}{name}<br>\n";
		}
	}
	$table .= "</td></tr></table>\n";
	$table .= "</td>\n";

	$table .= "<td align=center valign=top>\n";
	$table .= "<table><tr><td valign=top>\n";
	$table .= "<input type=checkbox $STATUS name=chkSTATUS>Status<br>\n" if (Maintainer());
	$table .= "<input type=checkbox $CLASS name=chkCLASS>Class<br>\n";
	$table .= "<input type=checkbox $URL name=chkURL>URL<br>\n";
	$table .= "<input type=checkbox $RATING name=chkRATING>Rating<br>\n";
	if (Maintainer()) {
		$table .= "<input type=checkbox $FORMAT name=chkFORMAT>Format<br>\n";
		$table .= "<input type=checkbox $DTD name=chkDTD>DTD<br>\n";
		$table .= "<input type=checkbox $PUBDATE name=chkPUBDATE>Pub Date<br>\n";
		$table .= "<input type=checkbox $LASTUPDATE name=chkLASTUPDATE>Last Update<br>\n";
		$table .= "</td><td valign=top>\n";
		$table .= "<input type=checkbox $TICKLEDATE name=chkTICKLEDATE>Tickle Date<br>\n";
		$table .= "<input type=checkbox $REVIEWSTATUS name=chkREVIEWSTATUS>Review Status<br>\n";
		$table .= "<input type=checkbox $TECHSTATUS name=chkTECHSTATUS>Tech Status<br>\n";
		$table .= "<input type=checkbox $MAINTAINED name=chkMAINTAINED>Maintained<br>\n";
		$table .= "<input type=checkbox $LICENSE name=chkLICENSE>License<br>\n";
		$table .= "<input type=checkbox $VERSION name=chkVERSION>Version<br>\n";
	}
	$table .= "</td></tr></table>\n";
	$table .= "</td>\n";

	$table .= "<td align=center valign=top>\n";
	$table .= "<table><tr><td valign=top>\n";
	$table .= "<select name=strSORT>\n";
	if ( $SORT eq "title" ) { $table .= '<option selected value="title">Title</option>'; } else { $table .= '<option value="title">Title</option>' }
	if ( $SORT eq "class" ) { $table .= '<option selected value="class">Class</option>'; } else { $table .= '<option value="class">Class</option>' }
	if ( $SORT eq "rating" ) { $table .= '<option selected value="rating">Rating</option>'; } else { $table .= '<option value="rating">Rating</option>' }
	if (Maintainer()) {
		if ( $SORT eq "document.pub_status" ) { $table .= '<option selected value="document.pub_status">Status</option>'; } else { $table .= '<option value="document.pub_status">Status</option>' }
		if ( $SORT eq "review_status_name" ) { $table .= '<option selected value="review_status_name">Review Status</option>'; } else { $table .= '<option value="review_status_name">Review Status</option>' }
		if ( $SORT eq "tech_review_status_name" ) { $table .= '<option selected value="tech_review_status_name">Tech Status</option>'; } else { $table .= '<option value="tech_review_status_name">Tech Status</option>' }
		if ( $SORT eq "format" ) { $table .= '<option selected value="format">Format</option>'; } else { $table .= '<option value="format">Format</option>' }
		if ( $SORT eq "dtd" ) { $table .= '<option selected value="dtd">DTD</option>'; } else { $table .= '<option value="dtd">DTD</option>' }
		if ( $SORT eq "pub_date" ) { $table .= '<option selected value="pub_date">Pub Date</option>'; } else { $table .= '<option value="pub_date">Pub Date</option>' }
		if ( $SORT eq "last_update" ) { $table .= '<option selected value="last_update">Last Update</option>'; } else { $table .= '<option value="last_update">Last Update</option>' }
		if ( $SORT eq "tickle_date" ) { $table .= '<option selected value="tickle_date">Tickle Date</option>'; } else { $table .= '<option value="tickle_date">Tickle Date</option>' }
		if ( $SORT eq "url" ) { $table .= '<option selected value="url">URL</option>'; } else { $table .= '<option value="url">URL</option>' }
		if ( $SORT eq "maintained" ) { $table .= '<option selected value="maintained">Maintained</option>'; } else { $table .= '<option value="maintained">Maintained</option>' }
		if ( $SORT eq "license" ) { $table .= '<option selected value="license">License</option>'; } else { $table .= '<option value="license">License</option>' }
	}
	$table .= "</select><br>";
	$table .= "</td></tr></table>\n";
	$table .= "</td>\n";

	if (Maintainer()) {
		$table .= "<td align=center valign=top>\n";
		$table .= "<table><tr><td valign=top>\n";
		$table .= "<select name=strSTATUS>\n";
		$table .= "<option></option>\n";
		if ( $strSTATUS eq "N" ) { $table .= '<option selected value="N">Active</option>'; } else { $table .= '<option value="N">Active</option>' }
		if ( $strSTATUS eq "?" ) { $table .= '<option selected value="?">Unknown</option>'; } else { $table .= '<option value="?">Unknown</option>' }
		if ( $strSTATUS eq "A" ) { $table .= '<option selected value="A">Archived</option>'; } else { $table .= '<option value="A">Archived</option>' }
		if ( $strSTATUS eq "D" ) { $table .= '<option selected value="D">Deleted</option>'; } else { $table .= '<option value="D">Deleted</option>' }
		if ( $strSTATUS eq "O" ) { $table .= '<option selected value="O">Offsite</option>'; } else { $table .= '<option value="O">Offsite</option>' }
		if ( $strSTATUS eq "P" ) { $table .= '<option selected value="P">Pending</option>'; } else { $table .= '<option value="P">Pending</option>' }
		if ( $strSTATUS eq "R" ) { $table .= '<option selected value="R">Replaced</option>'; } else { $table .= '<option value="R">Replaced</option>' }
		if ( $strSTATUS eq "W" ) { $table .= '<option selected value="W">Wishlist</option>'; } else { $table .= '<option value="W">Wishlist</option>' }
		if ( $strSTATUS eq "C" ) { $table .= '<option selected value="C">Cancelled</option>'; } else { $table .= '<option value="C">Cancelled</option>' }
		$table .= "</select>\n";
		$table .= "</td></tr></table>\n";
		$table .= "</td>\n";
	}
	$table .= "</tr>\n";
	$table .= "<tr><td colspan=4>\n";
	$table .= "<input type=submit name=Reload value=Reload>\n";
	$table .= "</td></tr>\n";
	$table .= "</form>\n";
	$table .= "</table>\n";

	# Documents
	#
	$table .= "<table class='box'>\n";
	$table .= "<tr><th colspan='2'>Title</th>";
	$table .= "<th>Status</th>" if (Param($foo, chkSTATUS));
	$table .= "<th>Review</th>" if (Param($foo, chkREVIEWSTATUS));
	$table .= "<th>Tech Status</th>" if (Param($foo, chkTECHSTATUS));
	$table .= "<th>Rating</th>" if (Param($foo, chkRATING));
	$table .= "<th>Maintained</th>" if (Param($foo, chkMAINTAINED));
	$table .= "<th>License</th>" if (Param($foo, chkLICENSE));
	$table .= "<th>Version</th>" if (Param($foo, chkVERSION));
	$table .= "<th>Class</th>" if (Param($foo, chkCLASS));
	$table .= "<th>Format</th>" if (Param($foo, chkFORMAT));
	$table .= "<th>DTD</th>" if (Param($foo, chkDTD));
	$table .= "<th>Pub Date</th>" if (Param($foo, chkPUBDATE));
	$table .= "<th>Last Update</th>" if (Param($foo, chkLASTUPDATE));
	$table .= "<th>Tickle Date</th>" if (Param($foo, chkTICKLEDATE));
	$table .= "<th>URL</th>" if (Param($foo, chkURL));
	$table .= "</tr>\n";

	my $sort = Param($foo, strSORT);
	if ($sort eq 'class') {
		@docids = sort { $classes{$docs{$a}{class_id}}{name} cmp $classes{$docs{$b}{class_id}}{name} } keys %docs;
	} elsif ($sort eq 'rating') {
		@docids = sort { $docs{$a}{rating} <=> $docs{$b}{rating} } keys %docs;
	} elsif ($sort eq 'pub_status') {
		@docids = sort { $docs{$a}{pub_status} cmp $docs{$b}{pub_status} } keys %docs;
	} elsif ($sort eq 'review_status_name') {
		@docids = sort { $reviewstatuses{$docs{$a}{review_status}}{name} cmp $reviewstatuses{$docs{$b}{review_status}}{name} } keys %docs;
	} elsif ($sort eq 'tech_review_status_name') {
		@docids = sort { $reviewstatuses{$docs{$a}{tech_review_status}}{name} cmp $reviewstatuses{$docs{$b}{tech_review_status}}{name} } keys %docs;
	} elsif ($sort eq 'format') {
		@docids = sort { $docs{$a}{format} cmp $docs{$b}{format} } keys %docs;
	} elsif ($sort eq 'dtd') {
		@docids = sort { $docs{$a}{dtd} cmp $docs{$b}{dtd} } keys %docs;
	} elsif ($sort eq 'pub_date') {
		@docids = sort { $docs{$a}{pub_date} cmp $docs{$b}{pub_date} } keys %docs;
	} elsif ($sort eq 'last_update') {
		@docids = sort { $docs{$a}{last_update} cmp $docs{$b}{last_update} } keys %docs;
	} elsif ($sort eq 'tickle_date') {
		@docids = sort { $docs{$a}{tickle_date} cmp $docs{$b}{tickle_date} } keys %docs;
	} elsif ($sort eq 'url') {
		@docids = sort { $docs{$a}{url} cmp $docs{$b}{url} } keys %docs;
	} elsif ($sort eq 'maintained') {
		@docids = sort { $docs{$a}{maintained} cmp $docs{$b}{maintained} } keys %docs;
	} elsif ($sort eq 'license') {
		@docids = sort { $docs{$a}{license} cmp $docs{$b}{license} } keys %docs;
	} else {
		@docids = sort { &sortTitle($docs{$a}{title}) cmp &sortTitle($docs{$b}{title}) } keys %docs;
	}
	
	foreach $doc_id (@docids) {

		if (scalar keys %myclasses) {
			my $classok = 0;
			foreach $class_id (keys %myclasses) {
				if ($docs{$doc_id}{class_id} eq $class_id) {
					$classok = 1;
				}
			}
			next unless ($classok);
		}

		if ($mypub_status) {
			my $pub_statusok = 0;
			if ($docs{$doc_id}{pub_status} eq $mypub_status) {
				$pub_statusok = 1;
			}
			next unless ($pub_statusok);
		}

		next unless (($docs{$doc_id}{url}) or Admin() or (exists $userdocs{$doc_id}));

		$table .= "<tr>";
		if (Maintainer()) {
			$table .= "<td>";
			if (Admin() or ($userdocs{$doc_id}{active})) {
				$table .= "<a href='document_edit.pl?doc_id=$doc_id'>" . EditImage() . "</a>";
			}
			$table .= "</td>";

			$table .= "<td>";
			if ($docs{$doc_id}{url}) {
				$table .= "<a href='$docs{$doc_id}{url}'>$docs{$doc_id}{title}</a>";
			} else {
				$table .= $docs{$doc_id}{title};
			}
			$table .= "</td>\n";
		} elsif ($docs{$doc_id}{url}) {
			$table .= "<td>";
			$table .= "<a href='$docs{$doc_id}{url}'>$docs{$doc_id}{title}</a>";
			$table .= "</td>\n";
		} else {
			next;
		}
		$table .= "<td>$pubstatuses{$docs{$doc_id}{pub_status}}{name}</td>" if (Param($foo, chkSTATUS));
		$table .= "<td>$reviewstatuses{$docs{$doc_id}{review_status}}{name}</td>" if (Param($foo, chkREVIEWSTATUS));
		$table .= "<td>$reviewstatuses{$docs{$doc_id}{tech_review_status}}{name}</td>" if (Param($foo, chkTECHSTATUS));
		$table .= "<td>$docs{$doc_id}{rating}</td>" if (Param($foo, chkRATING));
		$table .= "<td>$docs{$doc_id}{maintained}</td>" if (Param($foo, chkMAINTAINED));
		$table .= "<td>$docs{$doc_id}{license}</td>" if (Param($foo, chkLICENSE));
		$table .= "<td>$docs{$doc_id}{version}</td>" if (Param($foo, chkVERSION));
		$table .= "<td>$classes{$docs{$doc_id}{class_id}}{name}</td>" if (Param($foo, chkCLASS));
		$table .= "<td>$docs{$doc_id}{format}</td>" if (Param($foo, chkFORMAT));
		$table .= "<td>$docs{$doc_id}{dtd}</td>" if (Param($foo, chkDTD));
		$table .= "<td>$docs{$doc_id}{pub_date}</td>" if (Param($foo, chkPUBDATE));
		$table .= "<td>$docs{$doc_id}{last_update}</td>" if (Param($foo, chkLASTUPDATE));
		if (Param($foo, chkTICKLEDATE)) {
			$tickle_date = $docs{$doc_id}{tickle_date};
			$date = `date -I`;
			if ($date gt $tickle_date) {
				$table .= "<td><font color=red>$tickle_date</font></td>";
			} else {
				$table .= "<td>$tickle_date</td>";
			}
		}
	
		$table .= "<td>$docs{$doc_id}{url}</td>" if (Param($foo, chkURL));
		$table .= "</tr>\n";
	}
	$table .= "</table>\n";
	return $table;
}

sub sortTitle {
	my $title = shift;
	my $oldtitle;
	$title = uc($title);
	while ($title ne $oldtitle) { 
		$oldtitle = $title;
		$title =~ s/^LINUX\b\s*//;
		$title =~ s/^THE\s+//;
		$title =~ s/^A\s+//;
		$title =~ s/^AND\s+//;
		$title =~ s/^\+\s*//;
		$title =~ s/^\-\s*//;
		$title =~ s/^\/\s*//;
		$title =~ s/^\s*//;
	}
	return $title;
}

sub DocTable {
	my ($self, $doc_id) = @_;
	if ($doc_id) {
		my %doc = Doc($foo, $doc_id);
		LintadasDoc($foo, $doc_id);
#	} else {
#		my %doc = ();
#		$doc{dtd} = "DocBook";
#		$doc{format} = "XML";
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
	$doctable .= "<th align=right>";
	if ($doc{url}) {
		$doctable .= "<a href='$doc{url}'>URL</a>";
	} else {
		$doctable .= "URL";
	}
	$doctable .= "</th><td colspan=5><input type=text name=url size=60 style='width:100%' value='$doc{url}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>";
	if ($doc{ref_url}) {
		$doctable .= "<a href='$doc{ref_url}'>Home URL</a>";
	} else {
		$doctable .= "Home URL";
	}
	$doctable .= "</th><td colspan=5><input type=text name=ref_url size=60 style='width:100%' value='$doc{ref_url}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Status</th><td>";
	$doctable .= PubStatusCombo($foo, $doc{pub_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Class</th><td>\n";
	$doctable .= ClassCombo($foo, $doc{class_id});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Maint</th><td>\n";
	if ($doc{maintained}) {
		$doctable .= 'Yes';
	} else {
		$doctable .= 'No';
	}
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Language</th><td>";
	$doctable .= ReviewStatusCombo($foo, $doc{review_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Accuracy</th><td>";
	$doctable .= TechReviewStatusCombo($foo, $doc{tech_review_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>License</th><td>";
	$doctable .= LicenseCombo($foo, $doc{license});
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Pub Date</th><td><input type=text name=pub_date size=10 value='$doc{pub_date}'></td>";
	$doctable .= "<th align=right>Updated</th><td><input type=text name=last_update size=10 value='$doc{last_update}'></td>";
	$doctable .= "<th align=right>Version</th><td><input type=text name=version size=10 value='$doc{version}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Tickle Date</th><td><input type=text name=tickle_date size=10 value='$doc{tickle_date}'></td>";
	$doctable .= "<th align=right>ISBN</th><td><input type=text name=isbn size=14 value='$doc{isbn}'></td>";
	$doctable .= "<th align=right>Rating</th>\n";
	$doctable .= "<td>";
	$doctable .= BarGraphTable($foo, $doc{rating});
	$doctable .= "</td>\n";
	if ($doc_id) {
		$doctable .= "</tr>\n<tr>\n";
		$doctable .= "<th align=right>Format</th><td>";
		$doctable .= $doc{format};
		$doctable .= "</td>";
		$doctable .= "<th align=right>DTD</th><td>";
		$doctable .= $doc{dtd};
		$doctable .= "</td>";
		$doctable .= "<th align=right>DTD Ver</th><td>";
		$doctable .= $doc{dtd_version};
		$doctable .= "</td>";
	}
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Abstract</th>";
	$doctable .= "<td colspan=5><textarea name=abstract rows=6 cols=40 style='width:100%' wrap>$doc{abstract}</textarea></td>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr><td></td><td><input type=submit name=save value=Save></td></tr>\n";
	$doctable .= "</form>\n";
	$doctable .= "</table>\n";
	return $doctable;
}

sub PubStatusStatsTable{
	my $document_total = DocCount();
	my $sql = "SELECT pub_status_name, COUNT(*) FROM pub_status, document WHERE pub_status.pub_status = document.pub_status GROUP BY pub_status_name";
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Publication Status Statistics</th></tr>\n";
	$table .= "<tr><th>Status</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>License Statistics</th></tr>\n";
	$table .= "<tr><th>License</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	
	my $table = "<table class='box'>\n";
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
	my $language = RequestedLanguage();
	my $sql = "SELECT class_name, count(*) FROM class_i18n ci, document d WHERE d.pub_status = 'N' and ci.class_id=d.class_id and ci.lang='$language' GROUP BY class_name";
	my $total = 0;
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Classes</th></tr>\n";
	$table .= "<tr><th>Class</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>Format Statistics</th></tr>\n";
	$table .= "<tr><th>Format</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=3>DTD Statistics</th></tr>\n";
	$table .= "<tr><th>DTD</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	my $total = 0;
	my $table = "<table class='box'>\n";
	$table .= "<tr><th colspan=4>Format and DTD Statistics</th></tr>\n";
	$table .= "<tr><th>Format</th><th>DTD</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	$table .= "<tr><th colspan=2>Total</th><td align=right>" . $total . "</td></tr>";
	$table .= "</table>\n";
	return $table;
}

sub DetailedStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'");
	my $language = RequestedLanguage();
	my $sql = "SELECT class_name, dtd, format, count(*) FROM class_i18n ci, document d WHERE d.pub_status = 'N' AND ci.lang = '$language' AND ci.class_id=d.class_id GROUP BY class_name, dtd, format";
	my $total = 0;
	my $table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=5>Detailed Statistics</th></tr>\n";
	$table .= "<tr><th>Class</th><th>DTD</th><th>Format</th><th>Count</th><th>Percent</th></tr>";
	my $recordset = $DB->Recordset($sql);
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
	$table .= "<tr><th colspan=3>Total</th><td align=right>" . $total . "</td></tr>";
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
			$graph .= "'>&nbsp;</td>\n";
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
	
	$table .= "<table style='width:100%' class='box'>\n";
	$table .= "<tr><th colspan=6>Document Versions</th></tr>\n";
	$table .= "<tr><th>Version</th><th>Date</th><th>Initials</th><th colspan=3>Notes</th></tr>";
	foreach $key (sort { $docversions{$a}{pub_date} cmp $docversions{$b}{pub_date} } keys %docversions) {
		$table .= "<tr>";
		$table .= "<form method=POST action='document_rev_save.pl'>";
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>";
		$table .= "<input type=hidden name=rev_id value=$docversions{$key}{rev_id}>";
		$table .= "<input type=hidden name=doc_id value=$doc_id>";
		$table .= "<td valign=top><input type=text name=version width=12 size=12 value='$docversions{$key}{version}'></input></td>\n";
		$table .= "<td valign=top><input type=text name=pub_date width=12 size=12 value='$docversions{$key}{pub_date}'></input></td>\n";
		$table .= "<td valign=top><input type=text name=initials width=5 size=5 value='$docversions{$key}{initials}'></input></td>\n";
		$table .= "<td style='width:100%'><textarea name=notes rows=3 style='width:100%' wrap>$docversions{$key}{notes}</textarea>\n";
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
	$table .= "<td><textarea name=notes rows=3 style='width:100%' wrap></textarea>\n";

	$table .= "<td valign=top></td>\n";
	$table .= "<td valign=top><input type=submit value=Add></td>\n";
	$table .= "</form>";
	$table .= "</tr>\n";

	$table .= "</table>\n";
	return $table;
}

sub DocErrorsTable {
	my ($self, $doc_id) = @_;
	my %docerrors = DocErrors($foo, $doc_id);
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th>Document Errors</th></tr>\n";
	foreach $key (keys %docerrors) {
		$table .= "<tr><td>$docerrors{$key}{error}</td></tr>\n";
	}
	$table .= "</table>\n";
	return $table;
}

sub DocFilesTable {
	my ($self, $doc_id) = @_;
	my %docfiles = DocFiles($foo, $doc_id);
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th colspan=5>Document Files</th></tr>\n";
	foreach $filename (sort keys %docfiles) {
		$table .= "<tr>\n";
		$table .= "<td>\n";
		$table .= "<a href='file_edit.pl?filename=$filename&doc_id=$doc_id'>" . EditImage() . "</a>";
		$table .= "</td>\n";
		$table .= "<td style='width:100%'>\n";
		$table .= "<form method=POST action='document_file_save.pl'>";
		$table .= "<input type=hidden name=doc_id value='$doc_id'>";
		$table .= "<input type=hidden name='oldfilename' value=" . wsq($filename) . "</input>\n";
		$table .= "<input type=text name='filename' size=40 style='width:100%' value='$filename'></input>\n";
		$table .= "</td>\n";
		$table .= "<td valign=top><input type=checkbox name='chkDel'>Del</td>\n";
		$table .= "<td><input type=submit value=Save></td>\n";
		$table .= "</form></td></tr>\n";
	}
	$table .= "<tr>\n";
	$table .= "<td></td>\n";
	$table .= "<td>\n";
	$table .= "<form method=POST action='document_file_add.pl'>";
	$table .= "<input type=hidden name=doc_id value=$doc_id>";
	$table .= "<input type=text name='filename' size=40 style='width:100%'></input>\n";
	$table .= "</td>\n";
	$table .= "<td></td>\n";
	$table .= "<td><input type=submit value=Add></td>\n";
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

		$table .= "<td valign=top>";
		if (Admin() or (CurrentUserID() == $docusers{$key}{id})) {
			$table .= "<a href='user_edit.pl?user_id=$docusers{$key}{id}'>$docusers{$key}{name}</a>";
		} else {
			$table .= "$docusers{$key}{name}";
		}
		$table .= "</td>";
		$table .= "<td valign=top><input type=text name=email width=30 size=30 value='$docusers{$key}{email}'></input></td>\n";
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

	$table .= "<td valign=top><input type=text name=email width=30 size=30></td>\n";
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
		$table .= "<td><a href='topic_list.pl#$key'>$doctopics{$key}{topic_num}.$doctopics{$key}{subtopic_num} $doctopics{$key}{topic_name}: $doctopics{$key}{subtopic_name}</td>";
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
	$table .= "<table class='box'>\n";
	$table .= "<form action='document_vote_save.pl' method=GET>\n";
	$table .= "<tr><th colspan=3>Document Rating</th></tr>\n";
	$table .= "<input type=hidden name=doc_id value=$doc_id>\n";
	$table .= "<tr><th>Ratings</th><td>$vote_count</td>\n";
	$table .= "<td rowspan=3>\n";
	$table .= "You can rate each document on a scale from 1 to 10, where 1 is very poor and 10 is excellent.\n";
	$table .= "Your vote is averaged with the votes of others to obtain a rating for the document.\n";
	$table .= "<p>Enter a vote of 0 to remove your vote.";
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
	my $table = "<table style='width:100%' class='box'>\n";
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
	$table .= "<td><textarea name=notes rows=10 wrap></textarea>\n";
	$table .= "<input type=hidden name=doc_id value=$doc_id>\n";
	$table .= "<input type=submit value='Save'></td>\n";
	$table .= "</tr>";
	$table .= "</table>\n";
	$table .= "</form>";
	return $table;
}

sub StringsTable {
	my ($self) = @_;
	my $language = RequestedLanguage();
	my %strings = Strings();
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th>ID</th><th colspan=3>String ($language)</th></tr>\n";
	foreach $key (sort { $strings{$a}{id} <=> $strings{$b}{id} } keys %strings) {
		next unless ($strings{$key}{lang} eq $language);
		$table .= "<form name='string' action='string_save.pl'>\n";
		$table .= "<input type='hidden' name='string_id' value='$strings{$key}{id}'>\n";
		$table .= "<input type='hidden' name='lang' value='$strings{$key}{lang}'>\n";
		$table .= "<tr>\n";
		$table .= "<th>$strings{$key}{id}</th>\n";
		$table .= "<td style='width:100%'><textarea name='string' style='width:100%' cols=20 rows=10 wrap>$strings{$key}{string}</textarea></td>\n";
		$table .= "<td><input type=checkbox name=chkDel>Del</td>";
		$table .= "<td><input type=submit value='Save'></td>\n";
		$table .= "</tr>\n";
		$table .= "</form>";
	}
	$table .= "<form name='string' action='string_add.pl'>\n";
	$table .= "<input type='hidden' name='lang' value='$language'>\n";
	$table .= "<tr>\n";
	$table .= "<th></th>\n";
	$table .= "<td style='width:100%'><textarea name='string' style='width:100%' cols=20 rows=10 wrap></textarea></td>\n";
	$table .= "<td></td>\n";
	$table .= "<td><input type=submit value='Add'></td>\n";
	$table .= "</tr>\n";
	$table .= "</form>";
	$table .= "</table>";
	return $table;
}

sub ErrorsTable {
	my ($self) = @_;
	my %errors = Errors();
	my %docs = Docs();
	my $table = '';
	$table .= "<table class='box'>\n";
	$table .= "<tr><th>Document</th><th>Error</th></tr>\n";
	foreach $key (sort { $docs{$errors{$a}{doc_id}}{title} cmp $docs{$errors{$b}{doc_id}}{title} } keys %errors) {
		$doc_id = $errors{$key}{doc_id};
		$table .= "<tr>";
		$table .= "<td><a href='document_edit.pl?doc_id=$doc_id'>$docs{$doc_id}{title}</a></td>\n";
		$table .= "<td>$errors{$key}{error}</td>\n";
		$table .= "</tr>\n";
	}
	$table .= "</table>\n";
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

sub TopicTable {
	my ($self, $topic_num) = @_;
	my %topics = Topics();
	my $table = "<table style='width:100%' class='box'>\n";
	$table .= "<form name=topic method=POST action='topic_save.pl'>\n";
	$table .= "<input type=hidden name='topic_num' value='$topic_num'></input>\n";
	$table .= "<tr><th colspan=2>Topic Details</th></tr>\n";
	$table .= "<tr><th>Topic Num</th><td>$topic_num</td></tr>\n";
	$table .= "<tr><th>Topic</th><td><input type=text name='topic_name' value='$topics{$topic_num}{name}'></input></td></tr>\n";
	$table .= "<tr><th>Description</th><td><textarea cols=40 rows=5 style='width:100%' name='topic_description' wrap>$topics{$topic_num}{description}</textarea></td></tr>\n";
	$table .= "<tr><td></td><td><input type=submit value='Save'></td></tr>\n";
	$table .= "</form>\n";
	$table .= "</table>\n";
	return $table;
}

sub SubtopicsTable {
	my ($self, $subtopic_num) = @_;
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

sub SubtopicTable {
	my ($self, $subtopic_id) = @_;
	my %subtopics = Subtopics();
	my $table = "<table class='box'>\n";
	$table .= "<form name=subtopic method=POST action='subtopic_save.pl'>\n";
	$table .= "<input type=hidden name='topic_num' value='$subtopics{$subtopic_id}{topicnum}'></input>\n";
	$table .= "<input type=hidden name='subtopic_num' value='$subtopics{$subtopic_id}{num}'></input>\n";
	$table .= "<tr><th colspan=2>Subtopic Details</th></tr>\n";
	$table .= "<tr><th>Topic Num</th><td>$subtopics{$subtopic_id}{topicnum}</td></tr>\n";
	$table .= "<tr><th>Subtopic Num</th><td>$subtopics{$subtopic_id}{num}</td></tr>\n";
	$table .= "<tr><th>Subtopic</th><td><input type=text name='subtopic_name' value='$subtopics{$subtopic_id}{name}'></input></td></tr>\n";
	$table .= "<tr><th>Description</th><td><textarea cols=40 rows=5 style='width:100%' name='subtopic_description' wrap>$subtopics{$subtopic_id}{description}</textarea></td></tr>\n";
	$table .= "<tr><td></td><td><input type=submit value='Save'></td></tr>\n";
	$table .= "</form>\n";
	$table .= "</table>\n";
	return $table;
}

sub TopicDocsTable {
	my %docs = Docs();
	my %userdocs = UserDocs($foo, CurrentUserID());
	my $sql = "SELECT topic.topic_num, topic.topic_name, subtopic.subtopic_num, subtopic.subtopic_name, document.doc_id, document.title, topic_description, subtopic_description, url ";
	$sql .= "FROM topic, subtopic, document_topic, document ";
	$sql .= "WHERE topic.topic_num = subtopic.topic_num and topic.topic_num = document_topic.topic_num and subtopic.subtopic_num = document_topic.subtopic_num and document_topic.doc_id = document.doc_id AND document.pub_status='N' ";
	$sql .= "ORDER BY topic_num, subtopic_num, title";
	$recordset=$DB->Recordset($sql);

	$last_topic_num = 0;
	$last_subtopic_num = 0;
	my $table = "<table>\n";
	while (@row = $recordset->fetchrow) {
		$topic_num		= $row[0];
		$topic_name		= &trim($row[1]);
		$subtopic_num		= $row[2];
		$subtopic_name		= &trim($row[3]);
		$doc_id			= $row[4];
		$title			= &trim($row[5]);
		$topic_description	= &trim($row[6]);
		$subtopic_description	= &trim($row[7]);
		$url			= &trim($row[8]);
		if ($topic_num != $last_topic_num) {
			$table .= "<tr><td>";
			$table .= "<a href='topic_edit.pl?topic_num=$topic_num'>" . EditImage() . "</a>" if (Admin());
			$table .= "<a name='$topic_num'></td>";
			$table .= "<td><h2>";
			$table .= "$topic_num $topic_name";
			$table .= "</h2></td></tr>";
			$table .= "<tr><td></td><td><blockquote>$topic_description</blockquote></td></tr>\n";
		}
		if ($subtopic_num != $last_subtopic_num) {
			$table .= "<tr><td>";
			$table .= "<a href='subtopic_edit.pl?subtopic_id=$topic_num.$subtopic_num'>" . EditImage() . "</a>" if (Admin());
			$table .= "<a name='$topic_num.$subtopic_num'></td>";
			$table .= "<td><h3>";
			$table .= "$topic_num.$subtopic_num $subtopic_name";
			$table .= "</h3></td></tr>";
			$table .= "<tr><td></td><td><blockquote>$subtopic_description</blockquote></td></tr>\n";
		}
		if (Admin() or (exists $userdocs{$doc_id}) or ($url)) {
			$table .= "<tr><td>";
			if (Admin() or (exists $userdocs{$doc_id})) {
				$table .= "<a href='document_edit.pl?doc_id=$doc_id'>" . EditImage() . "</a>";
			}
			$table .= "</td><td>";
			if ($url) {
				$table .= "<a href='$url'>$title</a>";
			} elsif (Admin() or (exists $userdocs{$doc_id})) {
				$table .= "$title";
			}
			$table .= "</td></tr>\n";
		}
		
		$last_topic_num = $topic_num;
		$last_subtopic_num = $subtopic_num;
	}
	$table .= "</table>\n";
	return $table;
}

sub MessagesTable {
	my $message = '';
	if (scalar @messages) {
		print "<table><tr><td>\n";
		while (scalar @messages) {
			my $error = pop @messages;
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
	print "<tr><th>Main Menu</th></tr>\n";
	print "<tr><td><a href='welcome.pl'>Home</a></td></tr>\n";
	print "<tr><td><a href='document_list.pl'>Document Table</a></td></tr>\n";
	print "<tr><td><a href='topic_list.pl'>Topic Listing</a></td></tr>\n";
	print "<tr><td><a href='statistics.pl'>Statistics</a></td></tr>\n";
	print "</table>\n";
}

sub UserBox {
	if (CurrentUserID()) {
		print "<table class='navbox'>\n";
		print "<tr><th>\n";
		if ($currentuser_id) {
			print "$currentuser{name}";
			if (SysAdmin()) {
				print " (SysAdmin)";
			} elsif (Admin()) {
				print " (Admin)";
			} elsif (Maintainer()) {
				print " (Maintainer)";
			}
		}
		print "</th></tr>\n";
		print "<tr><td><a href='user_home.pl'>My Home</a></td></tr>\n";
		print "<tr><td><a href='user_edit.pl?user_id=$currentuser{id}'>Preferences</a></td></tr>";
		print "<tr><td><a href='logout.pl'>Log out</a></td></tr>\n";
		print "</table>\n";
	}
}

sub TopicsBox {
	my %topics = Topics();
	my %subtopics = Subtopics();
	print "<table class='navbox'>\n";
	print "<tr><th>Topics</th></tr>\n";
	print "<tr><td>\n";
	foreach $topic_num (sort { $a <=> $b } keys %topics) {
		print "<p>" if ($topic_num != 1);
		print "<a href='topic_list.pl#$topic_num'>$topics{$topic_num}{name}</a><br>\n";
		foreach $subtopic_num (sort { $subtopics{$a}{num} <=> $subtopics{$b}{num} } keys %subtopics) {
			if ($subtopics{$subtopic_num}{topicnum} == $topic_num) {
				print "&nbsp;&nbsp;<a href='topic_list.pl#$subtopic_num'>$subtopics{$subtopic_num}{name}</a><br>\n";
			}
		}
	}
	print "</td></tr>\n";
	print "</table>\n";
}

sub HeaderBox {
	my ($foo, $title) = @_;
	my $project = Config($foo, project);
	my $table = "<table class = 'header'><tr>\n";
	$table .= "<th>$project Lampadas System</th>";
	$table .= "</tr></table>\n";
	
	$table .= "<table class='title'><tr>\n";
	$table .= "<td><h1>$title</h1></td>\n";
	$table .= "</tr></table>\n";
	print $table;
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
	print "<table class='navbox'>\n";
	print "<tr><th>Admin Tools</th></tr>\n";
	print "<tr><td><a href='lintadas.pl'>Run Lintadas on All Docs</a></td></tr>\n";
	print "<tr><td><a href='error_list.pl'>View All Errors</a></td></tr>\n";
	print "<tr><td><a href='user_list.pl'>Manage User Accounts</a></td></tr>\n";
	print "<tr><td><a href='document_new.pl'>Add a Document</a></td></tr>\n";
	if (SysAdmin()) {
		print "<tr><td><a href='cvs_update.pl'>Force CVS Update</a></td></tr>\n";
		print "<tr><td><a href='string_edit.pl'>Edit Strings</a></td></tr>\n";
	}
	print "</td></tr></table>\n";
}

sub EditImage {
	return "<img src='images/edit.png' alt='Edit' height='20' width='20' border='0' hspace='5' vspace='0' align='top'>";
}

sub Login {
	use String::Random;
	my $self = shift;
	my $title = shift;
	my $username = $CGI->param('username');
	push @messages, "Param('username'): " . $username if ($debug);
	my $password = $CGI->param('password');
	push @messages, "Param('password'): " . $password if ($debug);
	my $count = $DB->Value("SELECT COUNT(*) FROM username WHERE username='$username'");
	if ($count) {
		push @messages, "Found the user" if ($debug);
		my $foundpw = $DB->Value("SELECT password FROM username WHERE username='$username'");
		if ($password eq $foundpw) {

			push @messages, "Password matched" if ($debug);
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
				$DB->Exec("UPDATE username SET session_id='$session_id' WHERE user_id='$currentuser_id'");
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
	my ($self, $username, $first_name, $middle_name, $surname, $email, $admin, $sysadmin, $password, $notes) = @_;
	my $message = '';
	if ($username and $email) {
		$count = $DB->Value("SELECT COUNT(*) FROM username WHERE username='$username'");
		if ($count) {
			$message = "The username you requested, '$username', is already taken.\n";
		} else {
			$count = $DB->Value("SELECT COUNT(*) FROM username WHERE email='$email'");
			if ($count) {
				$message = "There is already an account using your email address.\n";
			} else {
				unless ($password) {
					my $pwgen = new String::Random;
					$pwgen->{A} = ['A'..'Z', 'a'..'z'];
					$password = $pwgen->randpattern('AAAAAAAA');
				}
				my $user_id = $DB->Value("SELECT MAX(user_id) FROM username");
				$user_id++;
				$DB->Exec("INSERT INTO username(user_id, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes) VALUES ($user_id, " . wsq($username) . ", " . wsq($first_name) . ", " . wsq($middle_name) . ", " . wsq($surname) . ", " . wsq($email) . ", " . wsq($admin) . ", " . wsq($sysadmin) . ", " . wsq($password) . ", " . wsq($notes) . ")");
				%newuser = User($foo, $user_id);
				if ($newuser{username} eq $username) {
					StartPage($foo, 'Account Created');
					Mail($foo, $email, 'Lampadas Password', "Your Lampadas password is $password");
					$message = "Your account has been created.\n";
					$message .= "<p>Your password has been mailed to your email address,\n";
					$message .= "and you can use it to log in.\n";
					$message .= "Once you log in for the first time,\n";
					$message .= "you can change your password.\n";
				} else {
					$message = "There was an error creating your account.\n";
					$message .= "Please try again, and if the problem persists, notify the webmaster.\n";
				}
			}
		}
	} else {
		$message = "You didn't fill out all of the fields in the form.\n";
	}
	return $message;
}

sub SaveUser {
	my ($self, $user_id, $username, $first_name, $middle_name, $surname, $email, $admin, $sysadmin, $password, $notes, $stylesheet) = @_;
	$admin = 'f' unless ($admin eq 't');
	$sysadmin = 'f' unless ($sysadmin eq 't');
	$DB->Exec("UPDATE username SET username=" . wsq($username) . ", first_name=" . wsq($first_name) . ", middle_name=" . wsq($middle_name) . ", surname=" . wsq($surname) . ", email=" . wsq($email) . ", admin=" . wsq($admin) . ", sysadmin=" . wsq($sysadmin) . ", notes=" . wsq($notes) . ", stylesheet=" . wsq($stylesheet) .  " WHERE user_id=$user_id");
	if ($password) {
		$DB->Exec("UPDATE username SET password=" . wsq($password) . " WHERE user_id=$user_id");
	}
}

sub AddMessage {
	my ($self, $message) = @_;
	push @messages, $message;
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
		push @messages, "Error sending mail"
	}
}

sub CVSUpdate {
	my @cvsresponse = CVS('-q update -d -P');
	return @cvsresponse;
}

sub CVS {
	my $cvscommand = shift;
	my $cvsroot = Config($foo, 'cvs_root');
	my @cvsresponse = `cd $cvsroot; cvs $cvscommand`;
	return @cvsresponse;
}


#############################3

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
	$temp =~ s/\'/\'\'/g;
	if ($temp) {
		return "'$temp'";
	} else {
		return 'NULL';
	}
}

sub html {
	my $temp = shift;
	$temp =~ s/\'/&#39\;/;
	return $temp;
}
1;
