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
	Docs,
	Doc,
	DocUsers,
	
	Roles,
	Classes,
	PubStatuses,
	ReviewStatuses,
	Licenses,
	Topics,
	Subtopics,
	Formats,
	DTDs,

	StartPage,
	EndPage,
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
	DocTable,
	
	TitleBox,
	LoginBox,
	AdminBox,
	NavBox,

	Login,
	Logout,
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
	my $sql = "SELECT username, first_name, middle_name, surname, email, admin FROM username WHERE user_id=$user_id";
	my @row = $DB->Row("$sql");
	$user{id}		= $user_id;
	$user{username}		= &trim($row[0]);
	$user{first_name}	= &trim($row[1]);
	$user{middle_name}	= &trim($row[2]);
	$user{surname}		= &trim($row[3]);
	$user{name}		= &trim(&trim($user{first_name} . ' ' . $user{middle_name}) . ' ' . $user{surname});
	$user{email}		= &trim($row[4]);
	$user{admin}		= &yn2bool($row[5]);

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
6}

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

sub DocUsers {
	my $self = shift;
	my $doc_id = shift;
	my %docusers = ();
	my $sql = "SELECT document_user.user_id, role, document_user.email, active, username, first_name, middle_name, surname FROM document_user, username WHERE document_user.user_id = username.user_id AND doc_id=$doc_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$user_id = $row[0];
		$docusers{$user_id}{id}			= &trim($row[0]);
		$docusers{$user_id}{role}		= &trim($row[1]);
		$docusers{$user_id}{email}		= &trim($row[2]);
		$docusers{$user_id}{active}		= &yn2bool($row[3]);
		$docusers{$user_id}{username}		= &trim($row[4]);
		$docusers{$user_id}{first_name}		= &trim($row[5]);
		$docusers{$user_id}{middle_name}	= &trim($row[6]);
		$docusers{$user_id}{surname}		= &trim($row[7]);
		$docusers{$user_id}{name}		= &trim(&trim($docusers{$user_id}{first_name} . ' ' . $docusers{$user_id}{middle_name}) . ' ' . $docusers{$user_id}{surname});
	}
	return %docusers;
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
	my $sql = "select topic_num, topic_name, topic_description from topic";
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

sub Subtopics {
	my $self = shift;
	my $topic_num = shift;
	my %subtopics = ();
	my $sql = "select topic.topic_num, topic_name, topic_description, subtopic_num, subtopic_name, subtopic_description from subtopic, topic where subtopic.topic_num = topic.topic_num";
	$sql .= " WHERE topic_num = $topic_num" if ($topic_num);
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
	
	TitleBox($title);
#	NavBar();
	Errors();
	print "<table width='100%'><tr><td valign=top width='180'>\n";
	LoginBox() unless ($currentuser_id);
	AdminBox() if (Maintainer());
	NavBox();
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
	$formatcombo .= "<option></option>\n";
	foreach $format (sort { $formats{$a}{name} <=> $formats{$b}{name} } keys %formats) {
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
	$dtdcombo .= "<option></option>\n";
	foreach $dtd (sort { $dtds{$a}{dtd} <=> $dtds{$b}{dtd} } keys %dtds) {
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
	$table .= "<tr><th>Username</th><th>First Name</th><th>Middle Name</th><th>Surname</th><th>Email</th><th>Admin</th></tr>\n";
	foreach $key (sort { uc($users{$a}{username}) cmp uc($users{$b}{username}) } keys %users) {
		$table .= "<tr><td>" . a({href=>"user_edit.pl?user_id=$users{$key}{id}"},"$users{$key}{username}") . "</td>";
		$table .= "<td>$users{$key}{first_name}</td>\n";
		$table .= "<td>$users{$key}{middle_name}</td>\n";
		$table .= "<td>$users{$key}{surname}</td>\n";
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
	$table .= "<table class='box'>\n";
	$table .= "<form name=edit method=POST action='user_save.pl'>";
	$table .= "<input type=hidden name=user_id value=$user{id}></input>";
	$table .= "<tr><th colspan=2>User Details</th></tr>\n";
	$table .= "<tr><th>Username:</th><td><input type=text name='username' size=30 value='$user{username}'></input></td></tr>\n";
	$table .= "<tr><th>First Name:</th><td><input type=text name='first_name' size=30 value='$user{first_name}'></input></td></tr>\n";
	$table .= "<tr><th>Middle Name:</th><td><input type=text name='middle_name' size=30 value='$user{middle_name}'></input></td></tr>\n";
	$table .= "<tr><th>Surname:</th><td><input type=text name='surname' size=30 value='$user{surname}'></input></td></tr>\n";
	$table .= "<tr><th>Email:</th><td><input type=text name='email' size=30 value='$user{email}'></input></td></tr>\n";
	if (&Admin()) {
		$table .= "<tr><th>Admin:</th><td><select name='admin'>\n";
		if ($user{admin}) {
			$table .= "<option selected value='t'>Yes</option>\n";
			$table .= "<option value='f'>No</option>\n";
		} else {
			$table .= "<option value='t'>Yes</option>\n";
			$table .= "<option selected value='f'>No</option>\n";
		}
		$table .= "</select></td></tr>\n";
	}
	$table .= "<tr><th>New Password:</th><td><input type=password name='password' size=12></input></td></tr>";
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

sub DocTable {
	my $self = shift;
	my $doc_id = shift;
	my %doc = Doc($foo, $doc_id);
	my $doctable = '';
	$doctable .= "<table class='box'>\n";
	$doctable .= "<form method=POST action='document_save.pl' name='edit'>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th colspan=6>Document Details</th>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th align=right>Title:</th><td colspan=5><input type=text name=title size=60 style='width:100%' value='$doc{title}'></td>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th align=right>Filename:</th><td colspan=5><input type=text name=filename size=60 style='width:100%' value='$doc{filename}'></td>\n";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right><a href='$url'>URL</a>:</th><td colspan=5><input type=text name=url size=60 style='width:100%' value='$doc{url}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right><a href='$ref_url'>Home</a>:</th><td colspan=5><input type=text name=ref_url size=60 style='width:100%' value='$doc{ref_url}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Status:</th><td>";
	$doctable .= PubStatusCombo($foo, $doc{pub_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Class:</th><td>\n";
	$doctable .= ClassCombo($foo, $doc{class});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Maintained:</th><td>\n";
	if ($doc{maintained}) {
		$doctable .= 'Yes';
	} else {
		$doctable .= 'No';
	}
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Review Status:</th><td>";
	$doctable .= ReviewStatusCombo($foo, $doc{review_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right>Tech Review:</th><td>";
	$doctable .= TechReviewStatusCombo($foo, $doc{tech_review_status});
	$doctable .= "</td>";
	$doctable .= "<th align=right><a href='/help/license.html'>?</a>&nbsp;License:</th><td>";
	$doctable .= LicenseCombo($foo, $doc{license});
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Published:</th><td><input type=text name=pub_date size=10 value='$doc{pub_date}'></td>";
	$doctable .= "<th align=right>Updated:</th><td><input type=text name=last_update size=10 value='$doc{last_update}'></td>";
	$doctable .= "<th align=right>Version:</th><td><input type=text name=version size=10 value='$doc{version}'></td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Format:</th><td>";
	$doctable .= FormatCombo($foo, $doc{format});
	$doctable .= "</td>";
	$doctable .= "<th align=right>DTD:</th><td>";
	$doctable .= DTDCombo($foo, $doc{dtd});
	$doctable .= "</td>";
	$doctable .= "<th align=right>DTD Version:</th><td>";
	$doctable .= "<input type=text name=dtd_version size=10 value='$doc{dtd_version}'>";
	$doctable .= "</td>";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Tickle Date</th><td><input type=text name=tickle_date size=10 value='$doc{tickle_date}'></td>";
	$doctable .= "<th align=right>ISBN:</th><td><input type=text name=isbn size=14 value='$doc{isbn}'></td>";
	$doctable .= "<th align=right>Rating</th>\n";
	$doctable .= "<td>";
	if ( $doc{rating} > 0 ) {
	  $doctable .= "<table class='bargraph'>\n";
	  for ( $i = 1; $i <= 10; $i++ ) {
	    $doctable .= "<td class='";
	    if ( $doc{rating} >= $i ) { $doctable .= "baron" } else { $doctable .= "baroff" }
	    $doctable .= "'>&nbsp;&nbsp;</td>\n";
	  }
	  $doctable .= "</tr></table>\n";
	}
	else {
	  $doctable .= "Not rated";
	}
	$doctable .= "</td>\n";
	$doctable .= "</tr>\n<tr>\n";
	$doctable .= "<th align=right>Abstract</th>";
	$doctable .= "<td colspan=5><textarea name=abstract rows=6 cols=60 style='width:100%' wrap>$doc{abstract}</textarea></td>\n";
	$doctable .= "</tr>\n";
	$doctable .= "<tr>\n";
	$doctable .= "<th><a href='document_wiki.pl?doc_id=$doc_id'>WikiText</a></th>\n";
	$doctable .= "<td colspan=4>I am working on ways to provide easy online collaborative editing,
	and always for new ways to make writing for the LDP easier.

	<p>&quot;WikiText&quot; is a kind of specially formatted text used in lots of
	WikiWikiWebs. It makes writing extremely simple. I've implemented a very basic
	WikiText-style editing format that can be converted into DocBook.

	<p>For more information, read the <a href='/help/wiki.html'>help page</a>.</td>\n";

	$doctable .= "<td align=right><input type=submit name=save value=Save> <input type=submit name=saveandexit value='Save/Exit'></td>\n";
	$doctable .= "</tr>\n";
	$doctable .= "</form>\n";
	$doctable .= "</table>\n";
	return $doctable;
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
	print "<tr><td><a href='document_list.pl'>Documents</a></td></tr>\n";
	print "<tr><td><a href='topic_list.pl'>Topics</a></td></tr>\n";
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
	print "<tr><td><a href='statistics.pl'>Statistics</a></td></tr>\n";
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

sub NewUser {
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

sub Errors {
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
1;
