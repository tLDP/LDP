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
	Licenses,

	StartPage,
	EndPage,
	NavBar,

	RoleCombo,
	ClassCombo,
	PubStatusCombo,
	LicenseCombo,
	
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
	my $sql = "SELECT user_id, username, admin, first_name, middle_name, surname FROM username";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$user_id = $row[0];
		$users{$user_id}{id}		= $row[0];
		$users{$user_id}{username}	= &trim($row[1]);
		$users{$user_id}{admin}		= &yn2bool($row[2]);
		$users{$user_id}{first_name}	= &trim($row[3]);
		$users{$user_id}{middle_name}	= &trim($row[4]);
		$users{$user_id}{surname}	= &trim($row[5]);
		$users{$user_id}{name}		= &trim(&trim($users{$user_id}{first_name} . ' ' . $users{$user_id}{middle_name}) . ' ' . $users{$user_id}{surname});
	}
	return %users;
}

sub User {
	my $self = shift;
	my $user_id = shift;
	my %user = ();
	my $sql = "SELECT username, admin, first_name, middle_name, surname FROM username WHERE user_id=$user_id";
	my @row = $DB->Row("$sql");
	$user{id}		= $user_id;
	$user{username}		= &trim($row[0]);
	$user{admin}		= &yn2bool($row[1]);
	$user{first_name}	= &trim($row[2]);
	$user{middle_name}	= &trim($row[3]);
	$user{surname}		= &trim($row[4]);
	$user{name}		= &trim(&trim($user{first_name} . ' ' . $user{middle_name}) . ' ' . $user{surname});

	return %user;
}

sub UserDocs {
	my $self = shift;
	my $user_id = shift;
	my %docs = ();
	$sql = "SELECT distinct doc_id, role, active FROM document_user WHERE user_id=$user_id";
	my $recordset = $DB->Recordset($sql);
	while (@row = $recordset->fetchrow) {
		$doc_id			= $row[0];
		$docs{$doc_id}{id}	= $doc_id;
		$docs{$doc_id}{role}	= &trim($row[1]);;
		$docs{$doc_id}{active}	= &yn2bool($row[2]);
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
		print "Loaded role: $role\n";
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
	my $L = shift;
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
	my $L = shift;
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
	$CGI->redirect($url);
	exit;
}

sub Mail {
	use Mail::Sendmail;
	my $L = shift;
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
1;
