#!/usr/bin/python

"""
Lampadas system

This modules provides HTML functions to help generate the web interface.
"""

__version__ = '0.2'

def start_page(title, cookie) :
    """
    HTML header
    """
    if ($cookie) {
            print $CGI->header(-cookie=>$cookie,-expires=>'now')
            push @errors, "cookie: $cookie" if ($debug)
    } else {
            print $CGI->header(-expires=>'now')
    }

    print "<html><head>\n"
    print "<title>Lampadas || $title</title>\n"
    print "<link rel='stylesheet' href='css/default.css' type='text/css'>\n"
    print "</head>\n"
    print "<body><a name='top'>\n"

    if ($debug) {
            push @errors, "UserID: $currentuser_id"
            push @errors, "UserName: " . $currentuser{username}
    }

    print "<table style='width:100%' class='layout'>\n"
    print "<tr><td colspan=2>\n"
    HeaderBox($foo, $title)
    print "</td></tr>\n"
    if (scalar @errors) {
            print "<tr><td colspan=2>\n"
            ErrorsTable()
            print "</td><tr>\n"
    }
    print "<tr><td valign=top width='200'>\n"
    LoginBox() unless ($currentuser_id)
    AdminBox() if (Maintainer())
    NavBox()
    TopicsBox()
    print "</td><td valign=top>\n"
}

def end_page() :
    """
    HTML footer
    """
    print """</td></tr>
    </table>
    
    <p><hr>
    <p><center>%s</center>
    <br>
    </body>
    </html>""" % Config($foo, 'copyright')

# Combo boxes

def RoleCombo(out, roles, selected=None) :
    """
    Write to out a combo box containing the list of roles
    """
    out.write("<select name='role'>\n")
    for role in roles :
        if role == selected :
            out.write("<option selected>%s</option>\n" % role)
        else :
            out.write("<option>%s</option>\n" % role)
    out.write("</select>\n")


def ClassCombo(self, selected) :
	my %classes = Classes()
	my $classcombo = "<select name='class'>\n"
	foreach $class (sort keys %classes) {
		if ($selected eq $class) {
			$classcombo .= "<option selected>$class</option>\n"
		} else {
			$classcombo .= "<option>$class</option>\n"
		}
	}
	$classcombo .= "</select>\n"
	return $classcombo
}

def PubStatusCombo(self, selected) :
	my %pubstatuses = PubStatuses()
	my $pubstatuscombo = "<select name='pub_status'>\n"
	foreach $pubstatus (sort { $pubstatuses{$a}{name} cmp $pubstatuses{$b}{name} } keys %pubstatuses) {
		if ($selected eq $pubstatus) {
			$pubstatuscombo .= "<option value='$pubstatus' selected>$pubstatuses{$pubstatus}{name}</option>\n"
		} else {
			$pubstatuscombo .= "<option value='$pubstatus'>$pubstatuses{$pubstatus}{name}</option>\n"
		}
	}
	$pubstatuscombo .= "</select>\n"
	return $pubstatuscombo
}

def ReviewStatusCombo(self, selected) :
	my %reviewstatuses = ReviewStatuses()
	my $reviewstatuscombo = "<select name='review_status'>\n"
	$reviewstatuscombo .= "<option></option\n"
	foreach $reviewstatus (sort { $reviewstatuses{$a}{name} cmp $reviewstatuses{$b}{name} } keys %reviewstatuses) {
		if ($selected eq $reviewstatus) {
			$reviewstatuscombo .= "<option value='$reviewstatus' selected>$reviewstatuses{$reviewstatus}{name}</option>\n"
		} else {
			$reviewstatuscombo .= "<option value='$reviewstatus'>$reviewstatuses{$reviewstatus}{name}</option>\n"
		}
	}
	$reviewstatuscombo .= "</select>\n"
	return $reviewstatuscombo
}

def TechReviewStatusCombo(self, selected) :
	my %reviewstatuses = ReviewStatuses()
	my $reviewstatuscombo = "<select name='tech_review_status'>\n"
	$reviewstatuscombo .= "<option></option\n"
	foreach $reviewstatus (sort { $reviewstatuses{$a}{name} cmp $reviewstatuses{$b}{name} } keys %reviewstatuses) {
		if ($selected eq $reviewstatus) {
			$reviewstatuscombo .= "<option value='$reviewstatus' selected>$reviewstatuses{$reviewstatus}{name}</option>\n"
		} else {
			$reviewstatuscombo .= "<option value='$reviewstatus'>$reviewstatuses{$reviewstatus}{name}</option>\n"
		}
	}
	$reviewstatuscombo .= "</select>\n"
	return $reviewstatuscombo
}

def LicenseCombo(self, selected) :
	my %licenses = Licenses()
	my $licensecombo = "<select name='license'>\n"
	$licensecombo .= "<option></option>\n"
	foreach $license (sort keys %licenses) {
		if ($selected eq $license) {
			$licensecombo .= "<option selected>$license</option>\n"
		} else {
			$licensecombo .= "<option>$license</option>\n"
		}
	}
	$licensecombo .= "</select>\n"
	return $licensecombo
}

def TopicCombo(self, selected) :
	my %topics = Topics()
	my $topiccombo = "<select name='topic'>\n"
	foreach $topic (sort { $a <=> $b } keys %topics) {
		if ($selected eq $topic) {
			$topiccombo .= "<option value='$topic' selected>$topics{$topic}{num}. $topics{$topic}{name}</option>\n"
		} else {
			$topiccombo .= "<option value='$topic'>$topics{$topic}{num}. $topics{$topic}{name}</option>\n"
		}
	}
	$topiccombo .= "</select>\n"
	return $topiccombo
}

def SubtopicCombo(self, selected) :
	my %subtopics = Subtopics()
	my $subtopiccombo = "<select name='topic'>\n"
	foreach $subtopic (sort { $subtopics{$a}{topicnum} * 100 + $subtopics{$a}{num} <=> $subtopics{$b}{topicnum} * 100 + $subtopics{$b}{num} } keys %subtopics) {
		if ($selected eq $subtopic) {
			$subtopiccombo .= "<option value='$subtopic' selected>$subtopics{$subtopic}{topicnum}.$subtopics{$subtopic}{num}. $subtopics{$subtopic}{topicname}: $subtopics{$subtopic}{name}</option>\n"
		} else {
			$subtopiccombo .= "<option value='$subtopic'>$subtopics{$subtopic}{topicnum}.$subtopics{$subtopic}{num}. $subtopics{$subtopic}{topicname}: $subtopics{$subtopic}{name}</option>\n"
		}
	}
	$subtopiccombo .= "</select>\n"
	return $subtopiccombo
}

def FormatCombo(self, selected) :
	my %formats = Formats()
	my $formatcombo = "<select name='format'>\n"
	foreach $format (sort keys %formats) {
		if ($selected eq $format) {
			$formatcombo .= "<option selected>$format</option>\n"
		} else {
			$formatcombo .= "<option>$format</option>\n"
		}
	}
	$formatcombo .= "</select>\n"
	return $formatcombo
}

def DTDCombo(self, selected) :
	my %dtds = DTDs()
	my $dtdcombo = "<select name='dtd'>\n"
	foreach $dtd (sort keys %dtds) {
		if ($selected eq $dtd) {
			$dtdcombo .= "<option selected>$dtd</option>\n"
		} else {
			$dtdcombo .= "<option>$dtd</option>\n"
		}
	}
	$dtdcombo .= "</select>\n"
	return $dtdcombo
}

# tables

def UsersTable {
	my $table = "<table class='box'>\n"
	my %users = Users()
	$table .= "<tr><th>Username</th><th>Name</th><th>Email</th><th>Admin</th></tr>\n"
	foreach $key (sort { uc($users{$a}{username}) cmp uc($users{$b}{username}) } keys %users) {
		$table .= "<tr><td>" . a({href=>"user_edit.pl?user_id=$users{$key}{id}"},"$users{$key}{username}") . "</td>"
		$table .= "<td>$users{$key}{name}</td>\n"
		$table .= "<td>$users{$key}{email}</td>\n"
		$table .= "<td>" . bool2yn($users{$key}{admin}) . "</td>\n"
		$table .= "</tr>"
		$count++
	}
	$table .= "</table>\n"
	return $table
}

def UserTable(self, user_id) :
	my %user = User($foo, $user_id)
	my $table = ''
	$table .= "<table width='100%' class='box'>\n"
	$table .= "<form name=edit method=POST action='user_save.pl'>"
	$table .= "<input type=hidden name=user_id value=$user{id}></input>"
	$table .= "<tr><th colspan=2>User Details</th><th>Comments</th></tr>\n"
	$table .= "<tr><th>Username</th><td><input type=text name='username' size=20 value='$user{username}'></input></td>\n"
	$table .= "<td rowspan=5 style='width:100%'><textarea name='notes' style='width:100%' rows=10 wrap>$user{notes}</textarea></td>\n"
	$table .= "</tr>\n"
	$table .= "<tr><th>First Name</th><td><input type=text name='first_name' size=20 value='$user{first_name}'></input></td></tr>\n"
	$table .= "<tr><th>Middle Name</th><td><input type=text name='middle_name' size=20 value='$user{middle_name}'></input></td></tr>\n"
	$table .= "<tr><th>Surname</th><td><input type=text name='surname' size=20 value='" . html($user{surname}) . "'></input></td></tr>\n"
	$table .= "<tr><th>Email</th><td><input type=text name='email' size=20 value='$user{email}'></input></td></tr>\n"
	if (&Admin()) {
		$table .= "<tr><th>Admin</th><td><select name='admin'>\n"
		if ($user{admin}) {
			$table .= "<option selected value='t'>Yes</option>\n"
			$table .= "<option value='f'>No</option>\n"
		} else {
			$table .= "<option value='t'>Yes</option>\n"
			$table .= "<option selected value='f'>No</option>\n"
		}
		$table .= "</select></td></tr>\n"
	}
	$table .= "<tr><th>New Password</th><td><input type=password name='password' size=12></input></td></tr>"
	$table .= "<tr><td></td><td><input type=submit value=Save></td></tr>"
	$table .= "</form>"
	$table .= "</table>"
	return $table
}

def NewUserTable() :
    table = """
    <table class='box'>
    <tr><th>New User</th></tr>
    <tr><td>Welcome to the %s Lampadas system.
    
    <p>To create a new user account, fill out this form.
    
    <p><form name='newuser' action='user_add' method='POST'>
    <table>
    <tr>
    <td align='right'>*Username</td>
    <td><input type=text name=username size=20></input></td>
    </tr>
    <tr>
    <td align='right'>*Enter your email address.<br>Your password will be mailed to this address, so it must be valid.</td>
    <td><input type=text name=email size=20></input></td>
    </tr>
    <tr>
    <td align='right'>First Name</td>
    <td><input type=text name=first_name size=20></input></td>
    </tr>
    <tr>
    <td align='right'>Middle Name</td>
    <td><input type=text name=middle_name size=20></input></td>
    </tr>
    <tr>
    <td align='right'>Surname</td>
    <td><input type=text name=surname size=20></input></td>
    </tr>
    <tr>
    <td></td><td><input type=submit value='Create Account!'></td>
    </tr>
    </table
    </form>
    
    <p>*Required Fields
    </td></tr></table>
    """ % Config($foo, 'owner')

    return table


def UserDocsTable {
	my $self = shift
	my $user_id = shift
	my %docs = UserDocs($foo, $user_id)
	my $table = ''
	$table .= "<table class='box'>\n"
	$table .= "<tr><th colspan=6>User Documents</th></tr>\n"
	$table .= "<tr><th>Title</th>"
#	$table .= "<th>Class</th>"
	$table .= "<th>Doc Status</th>"
	$table .= "<th>Role</th>"
	$table .= "<th>Active</th>"
	$table .= "<th>Feedback Email</th></tr>\n"
	foreach $doc (sort { uc($docs{$a}{title}) cmp uc($docs{$b}{title}) } keys %docs) {
		$table .= "<tr>"
		$table .= "<td valign=top>"
		$table .= "<a href='document_edit.pl?doc_id=$docs{$doc}{id}'>" . EditImage() . "</a>"
		if ($docs{$doc}{url}) {
			$table .= "<a href='$docs{$doc}{url}'>$docs{$doc}{title}</a>"
		} else {
			$table .= "$docs{$doc}{title}"
		}
		$table .= "</td>\n"
#		$table .= "<td valign=top>$docs{$doc}{class}</td>\n"
		$table .= "<td valign=top>$docs{$doc}{pub_status_name}</td>\n"
		$table .= "<td valign=top>$docs{$doc}{role}</td>\n"
		$table .= "<td valign=top>" . bool2yn($docs{$doc}{active}) . "</td>\n"
		$table .= "<td valign=top>$docs{$doc}{email}</td>\n"
		$table .= "</tr>\n"
	}
	$table .= "</table>\n"
	return $table
}

def UserNotesTable {
	my ($self, $user_id) = @_
	my %usernotes = UserNotes($foo, $user_id)
	my $table = "<table style='width:100%' class='box'>\n"
	$table .= "<form name=notes method=POST action='user_note_add.pl'>\n"
	$table .= "<tr><th colspan=3>User Notes</th></tr>\n"
	$table .= "<tr><th>Date and Time</th><th>User</th><th>Notes</th></tr>\n"
	foreach $date_entered (sort keys %usernotes) {
		$table .= "<tr>\n"
		$table .= "<td valign=top>$date_entered</td>\n"
		$table .= "<td valign=top>$usernotes{$date_entered}{username}</td>\n"
		$table .= "<td valign=top>$usernotes{$date_entered}{notes}</td>\n"
		$table .= "</tr>\n"
	}
	$table .= "<tr><td colspan=2 align='right'>To add a note, type the note, then click Save.</td>\n"
	$table .= "<td><textarea name=notes style='width:100%' rows=10 wrap></textarea>\n"
	$table .= "<input type=hidden name=user_id value=$user_id>\n"
	$table .= "<input type=submit value='Save'></td>\n"
	$table .= "</tr>"
	$table .= "</table>\n"
	$table .= "</form>"
	return $table
}

def DocsTable(self) :
	my %docs = Docs()
	my %userdocs = UserDocs($foo, CurrentUserID())
	my %classes = Classes()
	my %pubstatuses = PubStatuses()
	my %reviewstatuses = ReviewStatuses()

	my $mypub_status = Param($foo,'strSTATUS')
	$mypub_status = "N" unless ($mypub_status)
	my %myclasses = ()
	foreach $class (keys %classes) {
		$param = "chk" . $class
		if (Param($foo, "$param") eq 'on') {
			$myclasses{$class} = 1
		}
	}

	# Optional Fields
	#
	$chkSTATUS       = Param($foo, 'chkSTATUS')
	$chkCLASS        = Param($foo,'chkCLASS')
	$chkFORMAT       = Param($foo,'chkFORMAT')
	$chkDTD          = Param($foo,'chkDTD')
	$chkPUBDATE      = Param($foo,'chkPUBDATE')
	$chkLASTUPDATE   = Param($foo,'chkLASTUPDATE')
	$chkTICKLEDATE   = Param($foo,'chkTICKLEDATE')
	$chkREVIEWSTATUS = Param($foo,'chkREVIEWSTATUS')
	$chkTECHSTATUS   = Param($foo,'chkTECHSTATUS')
	$chkURL          = Param($foo,'chkURL')
	$chkMAINTAINED   = Param($foo,'chkMAINTAINED')
	$chkLICENSE      = Param($foo,'chkLICENSE')
	$chkVERSION      = Param($foo,'chkVERSION')
	$chkFILENAME     = Param($foo,'chkFILENAME')
	$chkRATING       = Param($foo,'chkRATING')

	$SORT	= Param($foo,'strSORT')
	$SORT	= "title" unless ($SORT)

	$strSTATUS = Param($foo,'strSTATUS')

	# if we're not reloading, or aren't a maintainer, the default is to show only Active ('N') documents.
	unless (($reload eq 'Reload') or (Maintainer())) {
		$strSTATUS = 'N'
	}

	$reload = Param($foo,'Reload')

	$STATUS = ""
	$CLASS = ""
	$FORMAT = ""
	$DTD = ""
	$PUBDATE = ""
	$LASTUPDATE = ""
	$TICKLEDATE = ""
	$REVIEWSTATUS = ""
	$TECHSTATUS = ""
	$URL = ""
	$MAINTAINED = ""
	$LICENSE = ""
	$VERSION = ""
	$FILENAME = ""
	$RATING = ""

	if ( $chkSTATUS eq "on" ) { $STATUS = "checked " }
	if ( $chkCLASS eq "on" ) { $CLASS = "checked " }
	if ( $chkFORMAT eq "on" ) { $FORMAT = "checked " }
	if ( $chkDTD eq "on" ) { $DTD = "checked " }
	if ( $chkPUBDATE eq "on" ) { $PUBDATE = "checked " }
	if ( $chkLASTUPDATE eq "on" ) { $LASTUPDATE = "checked " }
	if ( $chkTICKLEDATE eq "on" ) { $TICKLEDATE = "checked " }
	if ( $chkREVIEWSTATUS eq "on" ) { $REVIEWSTATUS = "checked " }
	if ( $chkTECHSTATUS eq "on" ) { $TECHSTATUS = "checked " }
	if ( $chkURL eq "on" ) { $URL = "checked " }
	if ( $chkMAINTAINED eq "on" ) { $MAINTAINED = "checked " }
	if ( $chkLICENSE eq "on" ) { $LICENSE = "checked " }
	if ( $chkVERSION eq "on" ) { $VERSION = "checked " }
	if ( $chkFILENAME eq "on" ) { $FILENAME = "checked " }
	if ( $chkRATING eq "on" ) { $RATING = "checked " }

	my $table = ''

	$table .= "<table style='width:100%' class='box'>\n"
	$table .= "<form name=filter method=POST action='document_list.pl'>"
	$table .= "<tr><th>Classes</th><th>Optional Fields</th><th>Sort By</th>"
	$table .= "<th>Status</th>" if (Maintainer())
	$table .= "</tr>"
	$table .= "<tr><td align=center valign=top>\n"
	$table .= "<table><tr><td>"
	foreach $class (sort keys %classes) {
		my $name = 'chk' . $class
		my $value = Param($foo, $name)
		if ($value eq 'on') {
			$table .= "<input type='checkbox' checked name='$name'>$class<br>\n"
		} else {
			$table .= "<input type='checkbox' name='$name'>$class<br>\n"
		}
	}
	$table .= "</td></tr></table>\n"
	$table .= "</td>\n"

	$table .= "<td align=center valign=top>\n"
	$table .= "<table><tr><td valign=top>\n"
	$table .= "<input type=checkbox $STATUS name=chkSTATUS>Status<br>\n" if (Maintainer())
	$table .= "<input type=checkbox $CLASS name=chkCLASS>Class<br>\n"
	$table .= "<input type=checkbox $URL name=chkURL>URL<br>\n"
	$table .= "<input type=checkbox $RATING name=chkRATING>Rating<br>\n"
	if (Maintainer()) {
		$table .= "<input type=checkbox $FORMAT name=chkFORMAT>Format<br>\n"
		$table .= "<input type=checkbox $DTD name=chkDTD>DTD<br>\n"
		$table .= "<input type=checkbox $PUBDATE name=chkPUBDATE>Pub Date<br>\n"
		$table .= "<input type=checkbox $LASTUPDATE name=chkLASTUPDATE>Last Update<br>\n"
		$table .= "</td><td valign=top>\n"
		$table .= "<input type=checkbox $TICKLEDATE name=chkTICKLEDATE>Tickle Date<br>\n"
		$table .= "<input type=checkbox $REVIEWSTATUS name=chkREVIEWSTATUS>Review Status<br>\n"
		$table .= "<input type=checkbox $TECHSTATUS name=chkTECHSTATUS>Tech Status<br>\n"
		$table .= "<input type=checkbox $MAINTAINED name=chkMAINTAINED>Maintained<br>\n"
		$table .= "<input type=checkbox $LICENSE name=chkLICENSE>License<br>\n"
		$table .= "<input type=checkbox $VERSION name=chkVERSION>Version<br>\n"
		$table .= "<input type=checkbox $FILENAME name=chkFILENAME>Filename<br>\n"
	}
	$table .= "</td></tr></table>\n"
	$table .= "</td>\n"

	$table .= "<td align=center valign=top>\n"
	$table .= "<table><tr><td valign=top>\n"
	$table .= "<select name=strSORT>\n"
	if ( $SORT eq "title" ) { $table .= '<option selected value="title">Title</option>' } else { $table .= '<option value="title">Title</option>' }
	if ( $SORT eq "class" ) { $table .= '<option selected value="class">Class</option>' } else { $table .= '<option value="class">Class</option>' }
	if ( $SORT eq "rating" ) { $table .= '<option selected value="rating">Rating</option>' } else { $table .= '<option value="rating">Rating</option>' }
	if (Maintainer()) {
		if ( $SORT eq "document.pub_status" ) { $table .= '<option selected value="document.pub_status">Status</option>' } else { $table .= '<option value="document.pub_status">Status</option>' }
		if ( $SORT eq "review_status_name" ) { $table .= '<option selected value="review_status_name">Review Status</option>' } else { $table .= '<option value="review_status_name">Review Status</option>' }
		if ( $SORT eq "tech_review_status_name" ) { $table .= '<option selected value="tech_review_status_name">Tech Status</option>' } else { $table .= '<option value="tech_review_status_name">Tech Status</option>' }
		if ( $SORT eq "format" ) { $table .= '<option selected value="format">Format</option>' } else { $table .= '<option value="format">Format</option>' }
		if ( $SORT eq "dtd" ) { $table .= '<option selected value="dtd">DTD</option>' } else { $table .= '<option value="dtd">DTD</option>' }
		if ( $SORT eq "pub_date" ) { $table .= '<option selected value="pub_date">Pub Date</option>' } else { $table .= '<option value="pub_date">Pub Date</option>' }
		if ( $SORT eq "last_update" ) { $table .= '<option selected value="last_update">Last Update</option>' } else { $table .= '<option value="last_update">Last Update</option>' }
		if ( $SORT eq "tickle_date" ) { $table .= '<option selected value="tickle_date">Tickle Date</option>' } else { $table .= '<option value="tickle_date">Tickle Date</option>' }
		if ( $SORT eq "url" ) { $table .= '<option selected value="url">URL</option>' } else { $table .= '<option value="url">URL</option>' }
		if ( $SORT eq "maintained" ) { $table .= '<option selected value="maintained">Maintained</option>' } else { $table .= '<option value="maintained">Maintained</option>' }
		if ( $SORT eq "license" ) { $table .= '<option selected value="license">License</option>' } else { $table .= '<option value="license">License</option>' }
	}
	$table .= "</select><br>"
	$table .= "</td></tr></table>\n"
	$table .= "</td>\n"

	if (Maintainer()) {
		$table .= "<td align=center valign=top>\n"
		$table .= "<table><tr><td valign=top>\n"
		$table .= "<select name=strSTATUS>\n"
		$table .= "<option></option>\n"
		if ( $strSTATUS eq "N" ) { $table .= '<option selected value="N">Active</option>' } else { $table .= '<option value="N">Active</option>' }
		if ( $strSTATUS eq "?" ) { $table .= '<option selected value="?">Unknown</option>' } else { $table .= '<option value="?">Unknown</option>' }
		if ( $strSTATUS eq "A" ) { $table .= '<option selected value="A">Archived</option>' } else { $table .= '<option value="A">Archived</option>' }
		if ( $strSTATUS eq "D" ) { $table .= '<option selected value="D">Deleted</option>' } else { $table .= '<option value="D">Deleted</option>' }
		if ( $strSTATUS eq "O" ) { $table .= '<option selected value="O">Offsite</option>' } else { $table .= '<option value="O">Offsite</option>' }
		if ( $strSTATUS eq "P" ) { $table .= '<option selected value="P">Pending</option>' } else { $table .= '<option value="P">Pending</option>' }
		if ( $strSTATUS eq "R" ) { $table .= '<option selected value="R">Replaced</option>' } else { $table .= '<option value="R">Replaced</option>' }
		if ( $strSTATUS eq "W" ) { $table .= '<option selected value="W">Wishlist</option>' } else { $table .= '<option value="W">Wishlist</option>' }
		if ( $strSTATUS eq "C" ) { $table .= '<option selected value="C">Cancelled</option>' } else { $table .= '<option value="C">Cancelled</option>' }
		$table .= "</select>\n"
		$table .= "</td></tr></table>\n"
		$table .= "</td>\n"
	}
	$table .= "</tr>\n"
	$table .= "<tr><td colspan=4>\n"
	$table .= "<input type=submit name=Reload value=Reload>\n"
	$table .= "</td></tr>\n"
	$table .= "</form>\n"
	$table .= "</table>\n"

	# Documents
	#
	$table .= "<table class='box'>\n"

	$table .= "<tr><th colspan='2'>Title</th>"
	$table .= "<th>Status</th>" if (Param($foo, chkSTATUS))
	$table .= "<th>Review</th>" if (Param($foo, chkREVIEWSTATUS))
	$table .= "<th>Tech Status</th>" if (Param($foo, chkTECHSTATUS))
	$table .= "<th>Rating</th>" if (Param($foo, chkRATING))
	$table .= "<th>Maintained</th>" if (Param($foo, chkMAINTAINED))
	$table .= "<th>License</th>" if (Param($foo, chkLICENSE))
	$table .= "<th>Version</th>" if (Param($foo, chkVERSION))
	$table .= "<th>Filename</th>" if (Param($foo, chkFILENAME))
	$table .= "<th>Class</th>" if (Param($foo, chkCLASS))
	$table .= "<th>Format</th>" if (Param($foo, chkFORMAT))
	$table .= "<th>DTD</th>" if (Param($foo, chkDTD))
	$table .= "<th>Pub Date</th>" if (Param($foo, chkPUBDATE))
	$table .= "<th>Last Update</th>" if (Param($foo, chkLASTUPDATE))
	$table .= "<th>Tickle Date</th>" if (Param($foo, chkTICKLEDATE))
	$table .= "<th>URL</th>" if (Param($foo, chkURL))
	
	my $sort = Param($foo, strSORT)
	if ($sort eq 'class') {
		@docids = sort { $docs{$a}{class} cmp $docs{$b}{class} } keys %docs
	} elif ($sort eq 'rating') {
		@docids = sort { $docs{$a}{rating} <=> $docs{$b}{rating} } keys %docs
	} elif ($sort eq 'pub_status') {
		@docids = sort { $docs{$a}{pub_status} cmp $docs{$b}{pub_status} } keys %docs
	} elif ($sort eq 'review_status_name') {
		@docids = sort { $reviewstatuses{$docs{$a}{review_status}}{name} cmp $reviewstatuses{$docs{$b}{review_status}}{name} } keys %docs
	} elif ($sort eq 'tech_review_status_name') {
		@docids = sort { $reviewstatuses{$docs{$a}{tech_review_status}}{name} cmp $reviewstatuses{$docs{$b}{tech_review_status}}{name} } keys %docs
	} elif ($sort eq 'format') {
		@docids = sort { $docs{$a}{format} cmp $docs{$b}{format} } keys %docs
	} elif ($sort eq 'dtd') {
		@docids = sort { $docs{$a}{dtd} cmp $docs{$b}{dtd} } keys %docs
	} elif ($sort eq 'pub_date') {
		@docids = sort { $docs{$a}{pub_date} cmp $docs{$b}{pub_date} } keys %docs
	} elif ($sort eq 'last_update') {
		@docids = sort { $docs{$a}{last_update} cmp $docs{$b}{last_update} } keys %docs
	} elif ($sort eq 'tickle_date') {
		@docids = sort { $docs{$a}{tickle_date} cmp $docs{$b}{tickle_date} } keys %docs
	} elif ($sort eq 'url') {
		@docids = sort { $docs{$a}{url} cmp $docs{$b}{url} } keys %docs
	} elif ($sort eq 'maintained') {
		@docids = sort { $docs{$a}{maintained} cmp $docs{$b}{maintained} } keys %docs
	} elif ($sort eq 'license') {
		@docids = sort { $docs{$a}{license} cmp $docs{$b}{license} } keys %docs
	} else {
		@docids = sort { &sortTitle($docs{$a}{title}) cmp &sortTitle($docs{$b}{title}) } keys %docs
	}
	
	foreach $doc_id (@docids) {

		$classok = 1
		foreach $class (keys %myclasses) {
			$classok = 0
			if ($docs{$doc_id}{class} eq $class) {
				$classok = 1
			}
		}
		next unless ($classok)

		my $pub_statusok = 1
		if ($mypub_status) {
			$pub_statusok = 0
			if ($docs{$doc_id}{pub_status} eq $mypub_status) {
				$pub_statusok = 1
			}
		}
		next unless ($pub_statusok)

		next unless (($docs{$doc_id}{url}) or Admin() or (exists $userdocs{$doc_id}))

		$table .= "<tr>"
		if (Maintainer()) {
			$table .= "<td>"
			if (Admin() or ($userdocs{$doc_id}{active})) {
				$table .= "<a href='document_edit.pl?doc_id=$doc_id'>" . EditImage() . "</a>"
			}
			$table .= "</td>"

			$table .= "<td>"
			if ($docs{$doc_id}{url}) {
				$table .= "<a href='$docs{$doc_id}{url}'>$docs{$doc_id}{title}</a>"
			} else {
				$table .= $docs{$doc_id}{title}
			}
			$table .= "</td>\n"
		} elif ($docs{$doc_id}{url}) {
			$table .= "<td>"
			$table .= "<a href='$docs{$doc_id}{url}'>$docs{$doc_id}{title}</a>"
			$table .= "</td>\n"
		} else {
			next
		}
		$table .= "<td>$pubstatuses{$docs{$doc_id}{pub_status}}{name}</td>" if (Param($foo, chkSTATUS))
		$table .= "<td>$reviewstatuses{$docs{$doc_id}{review_status}}{name}</td>" if (Param($foo, chkREVIEWSTATUS))
		$table .= "<td>$reviewstatuses{$docs{$doc_id}{tech_review_status}}{name}</td>" if (Param($foo, chkTECHSTATUS))
		$table .= "<td>$docs{$doc_id}{rating}</td>" if (Param($foo, chkRATING))
		$table .= "<td>$docs{$doc_id}{maintained}</td>" if (Param($foo, chkMAINTAINED))
		$table .= "<td>$docs{$doc_id}{license}</td>" if (Param($foo, chkLICENSE))
		$table .= "<td>$docs{$doc_id}{version}</td>" if (Param($foo, chkVERSION))
		$table .= "<td>$docs{$doc_id}{class}</td>" if (Param($foo, chkCLASS))
		$table .= "<td>$docs{$doc_id}{format}</td>" if (Param($foo, chkFORMAT))
		$table .= "<td>$docs{$doc_id}{dtd}</td>" if (Param($foo, chkDTD))
		$table .= "<td>$docs{$doc_id}{pub_date}</td>" if (Param($foo, chkPUBDATE))
		$table .= "<td>$docs{$doc_id}{last_update}</td>" if (Param($foo, chkLASTUPDATE))
		if (Param($foo, chkTICKLEDATE)) {
			$tickle_date = $docs{$doc_id}{tickle_date}
			$date = `date -I`
			if ($date gt $tickle_date) {
				$table .= "<td><font color=red>$tickle_date</font></td>"
			} else {
				$table .= "<td>$tickle_date</td>"
			}
		}
	
		$table .= "<td>$docs{$doc_id}{url}</td>" if (Param($foo, chkURL))
		$table .= "</tr>\n"
	}
	$table .= "</table>\n"
	return $table
}

def sortTitle(title) :
	my $oldtitle
	$title = uc($title)
	while ($title ne $oldtitle) { 
		$oldtitle = $title
		$title =~ s/^LINUX\b\s*//
		$title =~ s/^THE\s+//
		$title =~ s/^A\s+//
		$title =~ s/^AND\s+//
		$title =~ s/^\+\s*//
		$title =~ s/^\-\s*//
		$title =~ s/^\/\s*//
		$title =~ s/^\s*//
	}
	return $title
}

def DocTable {
	my ($self, $doc_id) = @_
	if ($doc_id) {
		my %doc = Doc($foo, $doc_id)
	} else {
		my %doc = ()
		$doc{dtd} = "DocBook"
		$doc{format} = "XML"
	}
	my $doctable = ''
	$doctable .= "<table style='width:100%' class='box'>\n"
	if ($doc_id) {
		$doctable .= "<form method=POST action='document_save.pl' name='document'>\n"
	} else {
		$doctable .= "<form method=POST action='document_add.pl' name='document'>\n"
	}
	$doctable .= "<input name='doc_id' type=hidden value=$doc_id>\n"
	$doctable .= "<tr>\n"
	$doctable .= "<th colspan=6>Document Details</th>\n"
	$doctable .= "</tr>\n"
	$doctable .= "<tr>\n"
	$doctable .= "<th align='right'>Title</th><td colspan=5><input type=text name=title size=60 style='width:100%' value='$doc{title}'></td>\n"
	$doctable .= "</tr>\n"
	$doctable .= "<tr>\n"
	$doctable .= "<th align='right'><a href='$doc{url}'>URL</a></th><td colspan=5><input type=text name=url size=60 style='width:100%' value='$doc{url}'></td>"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'><a href='$ref_url'>Home URL</a></th><td colspan=5><input type=text name=ref_url size=60 style='width:100%' value='$doc{ref_url}'></td>"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'>Status</th><td>"
	$doctable .= PubStatusCombo($foo, $doc{pub_status})
	$doctable .= "</td>"
	$doctable .= "<th align='right'>Class</th><td>\n"
	$doctable .= ClassCombo($foo, $doc{class})
	$doctable .= "</td>"
	$doctable .= "<th align='right'>Maintained</th><td>\n"
	if ($doc{maintained}) {
		$doctable .= 'Yes'
	} else {
		$doctable .= 'No'
	}
	$doctable .= "</td>"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'>Review Status</th><td>"
	$doctable .= ReviewStatusCombo($foo, $doc{review_status})
	$doctable .= "</td>"
	$doctable .= "<th align='right'>Tech Review</th><td>"
	$doctable .= TechReviewStatusCombo($foo, $doc{tech_review_status})
	$doctable .= "</td>"
	$doctable .= "<th align='right'>License</th><td>"
	$doctable .= LicenseCombo($foo, $doc{license})
	$doctable .= "</td>"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'>Published</th><td><input type=text name=pub_date size=10 value='$doc{pub_date}'></td>"
	$doctable .= "<th align='right'>Updated</th><td><input type=text name=last_update size=10 value='$doc{last_update}'></td>"
	$doctable .= "<th align='right'>Version</th><td><input type=text name=version size=10 value='$doc{version}'></td>"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'>Format</th><td>"
	$doctable .= FormatCombo($foo, $doc{format})
	$doctable .= "</td>"
	$doctable .= "<th align='right'>DTD</th><td>"
	$doctable .= DTDCombo($foo, $doc{dtd})
	$doctable .= "</td>"
	$doctable .= "<th align='right'>DTD Version</th><td>"
	$doctable .= "<input type=text name=dtd_version size=10 value='$doc{dtd_version}'>"
	$doctable .= "</td>"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'>Tickle Date</th><td><input type=text name=tickle_date size=10 value='$doc{tickle_date}'></td>"
	$doctable .= "<th align='right'>ISBN</th><td><input type=text name=isbn size=14 value='$doc{isbn}'></td>"
	$doctable .= "<th align='right'>Rating</th>\n"
	$doctable .= "<td>"
	$doctable .= BarGraphTable($foo, $doc{rating})
	$doctable .= "</td>\n"
	$doctable .= "</tr>\n<tr>\n"
	$doctable .= "<th align='right'>Abstract</th>"
	$doctable .= "<td colspan=5><textarea name=abstract rows=6 cols=40 style='width:100%' wrap>$doc{abstract}</textarea></td>\n"
	$doctable .= "</tr>\n"
	$doctable .= "<tr><td></td><td><input type=submit name=save value=Save></td></tr>\n"
	$doctable .= "</form>\n"
	$doctable .= "</table>\n"
	return $doctable
}

def PubStatusStatsTable{
	my $document_total = DocCount()
	my $sql = "SELECT pub_status_name, COUNT(*) FROM pub_status, document WHERE pub_status.pub_status = document.pub_status GROUP BY pub_status_name"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>Publication Status Statistics</th></tr>\n"
	$table .= "<tr><th>Status</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n"
		$table .= "<th>" . $row[0] . "</th>\n"
		$table .= "<td align='right'>" . $row[1] . "</td>\n"
		$pct = sprintf( '%3.2f', $row[1] / $document_total * 100 )
		$table .= "<td align='right'>" . $pct . "%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $row[1]
	}
	$table .= "<tr><th>Total</th><td align='right'>$total</td></tr>"
	$table .= "</table>\n"
	return $table
}

def LicenseStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT license, COUNT(*) FROM document WHERE pub_status = 'N' GROUP BY license"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>License Statistics</th></tr>\n"
	$table .= "<tr><th>License</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$license = $row[0]
		$license =~ s/\s+$//
		$count   = $row[1]
		$table .= "<tr>\n"
		$table .= "<th>$license</th>\n"
		$table .= "<td align='right'>$count</td>\n"
		$pct = sprintf( '%3.2f', $count / $active_count * 100 )
		$table .= "<td align='right'>$pct%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $count
	}
	$table .= "<tr><th>Total</th><td align='right'>$total</td></tr>"
	$table .= "</table>\n"
	return $table
}

def FreeNonfreeStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT l.free, COUNT(*) FROM document d, license l WHERE d.license = l.license GROUP BY free"
	my $recordset = $DB->Recordset($sql)
	while (@row = $recordset->fetchrow) {
		if ($row[0] eq 't') {
			$free_count = $row[1]
		} else {
			$nonfree_count = $row[1]
		}
	}
	my $unknown_count = $DB->Value("SELECT COUNT(*) FROM document WHERE license IS NULL OR license=''")
	my $free_pct = sprintf( '%3.2f', $free_count / $active_count * 100 )
	my $nonfree_pct = sprintf( '%3.2f', $nonfree_count / $active_count * 100 )
	my $unknown_pct = sprintf( '%3.2f', $unknown_count / $active_count * 100 )
	
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>Free/NonFree Statistics</th></tr>\n"
	$table .= "<tr><th>Type</th><th align='right'>Count</th><th align='right'>Percent</th></tr>\n"
	$table .= "<tr><th>Free*</th><td align='right'>$free_count</td><td align='right'>$free_pct</td></tr>\n"
	$table .= "<tr><th>Non-Free</th><td align='right'>$nonfree_count</td><td align='right'>$nonfree_pct</td></tr>\n"
	$table .= "<tr><th>Unknown</th><td align='right'>$unknown_count</td><td align='right'>$unknown_pct</td></tr>\n"
	$table .= "<tr><th>Total</th><td align='right'>$active_count</td></tr>"
	$table .= "</table>\n"
	return $table
}

def ClassStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT class_name, count(*) FROM class, document WHERE pub_status = 'N' and class.class = document.class group by class_name"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>Classes</th></tr>\n"
	$table .= "<tr><th>Class</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n"
		$table .= "<th>" . $row[0] . "</th>\n"
		$table .= "<td align='right'>" . $row[1] . "</td>\n"
		$pct = sprintf( '%3.2f', $row[1] / $active_count * 100 )
		$table .= "<td align='right'>" . $pct . "%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $row[1]
	}
	$table .= "<tr><th>Total</th><td align='right'>" . $total . "</td></tr>"
	$table .= "</table>\n"
	return $table
}

def FormatStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT format, count(*) FROM document WHERE pub_status = 'N' group by format"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>Format Statistics</th></tr>\n"
	$table .= "<tr><th>Format</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n"
		$table .= "<th>" . $row[0] . "</th>\n"
		$table .= "<td align='right'>" . $row[1] . "</td>\n"
		$pct = sprintf( '%3.2f', $row[1] / $active_count * 100 )
		$table .= "<td align='right'>" . $pct . "%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $row[1]
	}
	$table .= "<tr><th>Total</th><td align='right'>" . $total . "</td></tr>"
	$table .= "</table>\n"
	return $table
}

def DTDStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT dtd, count(*) FROM document WHERE pub_status = 'N' group by dtd"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>DTD Statistics</th></tr>\n"
	$table .= "<tr><th>DTD</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n"
		$table .= "<th>" . $row[0] . "</th>\n"
		$table .= "<td align='right'>" . $row[1] . "</td>\n"
		$pct = sprintf( '%3.2f', $row[1] / $active_count * 100 )
		$table .= "<td align='right'>" . $pct . "%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $row[1]
	}
	$table .= "<tr><th>Total</th><td align='right'>" . $total . "</td></tr>"
	$table .= "</table>\n"
	return $table
}

def FormatDTDStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT format, dtd, count(*) FROM document WHERE pub_status = 'N' group by format, dtd"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=4>Format and DTD Statistics</th></tr>\n"
	$table .= "<tr><th>Format</th><th>DTD</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$format = $row[0]
		$dtd    = $row[1]
		$count  = $row[2]
		$pct = sprintf( '%3.2f', $count / $active_count * 100 )
		$table .= "<tr>\n"
		$table .= "<th>$format</th>\n"
		$table .= "<th>$dtd</th>\n"
		$table .= "<td align='right'>$count</td>\n"
		$table .= "<td align='right'>" . $pct . "%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $count
	}
	$table .= "<tr><th colspan=2>Total</th><td align='right'>" . $total . "</td></tr>"
	$table .= "</table>\n"
	return $table
}

def DetailedStatsTable {
	my $active_count = DocCountByPubStatus($foo, "'N'")
	my $sql = "SELECT class, dtd, format, count(*) FROM document WHERE pub_status = 'N' group by class, dtd, format"
	my $recordset = $DB->Recordset($sql)
	my $total = 0
	my $table .= "<table class='box'>\n"
	$table .= "<tr><th colspan=5>Detailed Statistics</th></tr>\n"
	$table .= "<tr><th>Class</th><th>DTD</th><th>Format</th><th>Count</th><th>Percent</th></tr>"
	while (@row = $recordset->fetchrow) {
		$table .= "<tr>\n"
		$table .= "<th>" . $row[0] . "</th>\n"
		$table .= "<th>" . $row[1] . "</th>\n"
		$table .= "<th>" . $row[2] . "</th>\n"
		$table .= "<td align='right'>" . $row[3] . "</td>\n"
		$pct = sprintf( '%3.2f', $row[3] / $active_count * 100 )
		$table .= "<td align='right'>" . $pct . "%</td>\n"
		$table .= "</tr>\n"
		$total = $total + $row[3]
	}
	$table .= "<tr><th colspan=3>Total</th><td align='right'>" . $total . "</td></tr>"
	$table .= "</table>\n"
	return $table
}

def MiscStatsTable {
	use Date::Calc qw(:all)
	my $sql = "SELECT last_update FROM document WHERE pub_status='N'"
	my $recordset = $DB->Recordset($sql)
	my $count = 0
	my $avg_age   = 0
	my ($year2, $month2, $day2) = Today()
	while (@row = $recordset->fetchrow) {
		my $last_update = $row[0]
		if (($last_update) && ($last_update ne "1970-01-01" )) {
			my $year1 = substr($last_update,0,4)
			my $month1 = substr($last_update,5,2)
			my $day1 = substr($last_update,8,2)
			my $age = Delta_Days($year1, $month1, $day1, $year2, $month2, $day2)
			if ($count) {
				$avg_age = (($avg_age * ($count - 1)) + $age) / $count
			} else {
				$avg_age = $age
			}
			$count++
		}
	}
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=2>Miscellaneous Statistics</th></tr>"
	$table .= "<tr><th>Statistic</th><th>Value</th></tr>"
	$table .= "<tr><th>Average Age Since Last Update</th><td>&nbsp"
	$table .= sprintf("%i", $avg_age)
	$table .= " days</td></tr>"
	$table .= "</table>\n"
	return $table
}

def BarGraphTable {
	my ($self, $value) = @_
	my $graph = ''
	if ($value) {
		$graph .= "<table class='bargraph'>\n"
		for ( $i = 1 $i <= 10 $i++ ) {
			$graph .= "<td class='"
			if ( $value >= $i ) { $graph .= "baron" } else { $graph .= "baroff" }
			$graph .= "'>&nbsp</td>\n"
		}
		$graph .= "</tr></table>\n"
	} else {
		$graph .= "Not rated"
	}
	return $graph
}

def DocVersionsTable {
	my ($self, $doc_id) = @_
	my $table = ''
	my %docversions = DocVersions($foo, $doc_id)
	
	$table .= "<table style='width:100%' class='box'>\n"
	$table .= "<tr><th colspan=6>Document Versions</th></tr>\n"
	$table .= "<tr><th>Version</th><th>Date</th><th>Initials</th><th>Notes</th></tr>"
	foreach $key (sort { $docversions{$a}{pub_date} cmp $docversions{$b}{pub_date} } keys %docversions) {
		$table .= "<tr>"
		$table .= "<form method=POST action='document_rev_save.pl'>"
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>"
		$table .= "<input type=hidden name=rev_id value=$docversions{$key}{rev_id}>"
		$table .= "<input type=hidden name=doc_id value=$doc_id>"
		$table .= "<td valign=top><input type=text name=version width=12 size=12 value='$docversions{$key}{version}'></input></td>\n"
		$table .= "<td valign=top><input type=text name=pub_date width=12 size=12 value='$docversions{$key}{pub_date}'></input></td>\n"
		$table .= "<td valign=top><input type=text name=initials width=5 size=5 value='$docversions{$key}{initials}'></input></td>\n"
		$table .= "<td><textarea name=notes rows=3 style='width:100%' wrap>$docversions{$key}{notes}</textarea>\n"
		$table .= "<td valign=top><input type=checkbox name=chkDel>Del</td>"
		$table .= "<td valign=top><input type=submit value=Save></td>\n"
		$table .= "</form>"
		$table .= "</tr>\n"
	}

	$table .= "<tr>"
	$table .= "<form method=POST action='document_rev_add.pl'>"
	$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>"
	$table .= "<input type=hidden name=doc_id value=$doc_id>"

	$table .= "<td valign=top><input type=text name=version width=12 size=12></input></td>\n"
	$table .= "<td valign=top><input type=text name=pub_date width=12 size=12></input></td>\n"
	$table .= "<td valign=top><input type=text name=initials width=5 size=5></input></td>\n"
	$table .= "<td><textarea name=notes rows=3 style='width:100%' wrap></textarea>\n"

	$table .= "<td valign=top></td>\n"
	$table .= "<td valign=top><input type=submit value=Add></td>\n"
	$table .= "</form>"
	$table .= "</tr>\n"

	$table .= "</table>\n"
	return $table
}

def DocFilesTable {
	my ($self, $doc_id) = @_
	my %docfiles = DocFiles($foo, $doc_id)
	my $table = ''
	$table .= "<table class='box'>\n"
	$table .= "<tr><th colspan=3>Document Files</th></tr>\n"
	foreach $filename (sort keys %docfiles) {
		$table .= "<tr><td>\n"
		$table .= "<form method=POST action='document_file_save.pl'>"
		$table .= "<input type=hidden name=doc_id value=$doc_id>"
		$table .= "<input type=hidden name='oldfilename' value=" . wsq($filename) . "</input>\n"
		$table .= "<input type=text name='filename' size=40 style='width:100%' value='$filename'></input>\n"
		$table .= "</td>\n"
		$table .= "<td valign=top><input type=checkbox name='chkDel'>Del</td>\n"
		$table .= "<td><input type=submit value=Save></td>\n"
		$table .= "</form></td></tr>\n"
	}
	$table .= "<tr><td>\n"
	$table .= "<form method=POST action='document_file_add.pl'>"
	$table .= "<input type=hidden name=doc_id value=$doc_id>"
	$table .= "<input type=text name='filename' size=40 style='width:100%'></input>\n"
	$table .= "</td>\n"
	$table .= "<td></td>\n"
	$table .= "<td><input type=submit value=Add></td>\n"
	$table .= "</tr>\n"
	$table .= "</table>\n"
	return $table	
}

def DocUsersTable {
	my ($self, $doc_id) = @_
	my $table = ''
	my %docusers = DocUsers($foo, $doc_id)
	
	$table .= "<table class='box'>\n"
	$table .= "<tr><th colspan=6>Document Contributors</th></tr>\n"
	$table .= "<tr><th>Status</th><th>Role</th><th>Name</th><th>Feedback Email</th><th colspan=2>Action</th></tr>"
	foreach $key (sort keys %docusers) {
		$table .= "<tr>"
		$table .= "<form method=POST action='document_user_save.pl'>"
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>"
		$table .= "<input type=hidden name=doc_id value=$doc_id>"
		$table .= "<input type=hidden name=user_id value=$docusers{$key}{id}>"

		$table .= '<td valign=top><select name="active">'
		if ($docusers{$key}{active}) {
			$table .= '<option selected value="t">Active</option>'
			$table .= '<option value="f">Inactive</option>'
		} else {
			$table .= '<option value="t">Active</option>'
			$table .= '<option selected value="f">Inactive</option>'
		}
		$table .= "</select></td>"

		$table .= "<td valign=top>"
		$table .= RoleCombo($foo, $docusers{$key}{role})
		$table .= "</td>\n"

		$table .= "<td valign=top><a href='user_edit.pl?user_id=$docusers{$key}{id}'>$docusers{$key}{name}</a></td>\n"
		$table .= "<td valign=top><input type=text name=email width=20 size=20 value='$docusers{$key}{email}'></input></td>\n"
		$table .= "<td valign=top><input type=checkbox name=chkDel>Del</td>"
		$table .= "<td valign=top><input type=submit value=Save></td>\n"
		$table .= "</form>"
		$table .= "</tr>\n"
	}

	# For assigning a new contributor
	$table .= "<tr>"
	$table .= "<form method=POST action='document_user_add.pl'>"
	$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>"
	$table .= "<input type=hidden name=doc_id value=$doc_id>"

	$table .= '<td valign=top><select name="active">'
	$table .= '<option value="t">Active</option>'
	$table .= '<option value="f">Inactive</option>'
	$table .= "</select></td>"

	$table .= "<td valign=top>"
	$table .= RoleCombo()
	$table .= "</td>\n"

	$table .= "<td valign=top>"

	$sql = "SELECT user_id, first_name, middle_name, surname FROM username ORDER BY first_name, middle_name, surname"
	$authors_result = $DB->Recordset($sql)

	$table .= "<select name=user_id\n"
	$table .= "<option>\n"
	while (@row = $authors_result->fetchrow) {
		$user_id = $row[0]
		$first_name	= strip($row[1])
		$middle_name	= strip($row[2])
		$surname	= strip($row[3])
		$name = strip(strip("$first_name $middle_name") . " " . $surname)
		$table .= "<option value=$user_id>$name</option>\n"
	}
	$table .= "</select>\n"
	$table .= "</td>\n"

	$table .= "<td valign=top><input type=text name=email width=20 size=20></td>\n"
	$table .= "<td valign=top></td>\n"
	$table .= "<td valign=top><input type=submit value=Add></td>\n"
	$table .= "</form>"
	$table .= "</tr>\n"

	$table .= "<tr><td colspan=5><small>Note: Deleting a record here doesn't delete the user. It only deletes the association between the user and this document.</small></td></tr>\n"
	$table .= "</table>\n"
}

def DocTopicsTable {
	my ($self, $doc_id) = @_
	my %doctopics = DocTopics($foo, $doc_id)
	my $table = "<table class='box'>"
	$table .= "<tr><th colspan=2>Document Topics</th></tr>\n"
	$table .= "<tr><th>Topic</th><th>Action</th></tr>\n"
	foreach $key (keys %doctopics) {
  		$table .= "<tr>\n"
		$table .= "<form method=POST action='document_topic_del.pl'>\n"
		$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>"
		$table .= "<input type=hidden name=doc_id value=$doc_id>"
		$table .= "<input type=hidden name=topic_num value=$doctopics{$key}{topic_num}>"
		$table .= "<input type=hidden name=subtopic_num value=$doctopics{$key}{subtopic_num}>"
		$table .= "<td><a href='topic_list.pl#$key'>$doctopics{$key}{topic_num}.$doctopics{$key}{subtopic_num} $doctopics{$key}{topic_name}: $doctopics{$key}{subtopic_name}</td>"
		$table .= "<td valign=top><input type=submit value=Delete></td>\n"
		$table .= "</form>\n"
		$table .= "</tr>\n"
	}
	$table .= "<tr>"
	$table .= "<form method=POST action='document_topic_add.pl'>"
	$table .= "<input type=hidden name=caller value='document_edit.pl?doc_id=$doc_id'>"
	$table .= "<input type=hidden name=doc_id value=$doc_id>"
	$table .= "<td valign=top>\n"
	$table .= SubtopicCombo()
	$table .= "</td>\n"
	$table .= "<td valign=top><input type=submit value=Add></td>\n"
	$table .= "</form>\n"
	$table .= "</tr></table>\n"
	return $table
}

def DocRatingTable {
	my ($self, $doc_id) = @_
	my $vote_count	= $DB->Value("SELECT COUNT(*) FROM doc_vote WHERE doc_id=$doc_id")
	my $vote	= $DB->Value("SELECT vote FROM doc_vote WHERE doc_id=$doc_id AND user_id=" . CurrentUserID())
	$table .= "<table class='box'><tr><th colspan=3>Document Rating</th></tr>\n"
	$table .= "<form action='document_vote_save.pl' method=POST>\n"
	$table .= "<input type=hidden name=doc_id value=$doc_id>\n"
	$table .= "<tr><th>Ratings</th><td>$vote_count</td>\n"
	$table .= "<td rowspan=3>\n"
	$table .= "You can rate each document on a scale from 1 to 10, where 1 is very poor and 10 is excellent.\n"
	$table .= "Your vote is averaged with the votes of others to obtain a rating for the document.\n"
	$table .= "</td>\n"
	$table .= "</tr>\n"
	$table .= "<tr><th>Average</th><td>" . BarGraphTable($foo, $doc{rating}) . "</td></tr>\n"
	$table .= "<tr><th>Your Rating</th><td><input name=vote type=text size=2 width=2 value=$vote></input>\n"
	$table .= "<input type=submit value='Rate'></td>\n"
	$table .= "</form>"
	$table .= "</tr></table>"
	return $table	
}

def DocNotesTable {
	my ($self, $doc_id) = @_
	my %docnotes = DocNotes($foo, $doc_id)
	my $table = "<table style='width:100%' class='box'>\n"
	$table .= "<form name=notes method=POST action='document_note_add.pl'>\n"
	$table .= "<tr><th colspan=3>Document Notes</th></tr>\n"
	$table .= "<tr><th>Date and Time</th><th>User</th><th>Notes</th></tr>\n"
	foreach $date_entered (sort keys %docnotes) {
		$table .= "<tr>\n"
		$table .= "<td valign=top>$date_entered</td>\n"
		$table .= "<td valign=top>$docnotes{$date_entered}{username}</td>\n"
		$table .= "<td valign=top>$docnotes{$date_entered}{notes}</td>\n"
		$table .= "</tr>\n"
	}
	$table .= "<tr><td colspan=2 align='right'>To add a note, type the note, then click Save.</td>\n"
	$table .= "<td><textarea name=notes rows=10 wrap></textarea>\n"
	$table .= "<input type=hidden name=doc_id value=$doc_id>\n"
	$table .= "<input type=submit value='Save'></td>\n"
	$table .= "</tr>"
	$table .= "</table>\n"
	$table .= "</form>"
	return $table
}

def TopicsTable {
	my $self = shift
	my %topics = Topics()
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>Topics</th></tr>\n"
	foreach $topic_num (sort { $a <=> $b } keys %topics) {
		$table .= "<tr><td align='right'>" . $topics{$topic_num}{num} . "</td>\n"
		$table .= "<td><a href='subtopic_list.pl?topic_num=$topic_num'>$topics{$topic_num}{name}</a></td>\n"
		$table .= "<td>$topics{$topic_num}{description}</td></tr>\n"
	}
	$table .= "</table>\n"
	return $table
}

def TopicTable {
	my ($self, $topic_num) = @_
	my %topics = Topics()
	my $table = "<table style='width:100%' class='box'>\n"
	$table .= "<form name=topic method=POST action='topic_save.pl'>\n"
	$table .= "<input type=hidden name='topic_num' value='$topic_num'></input>\n"
	$table .= "<tr><th colspan=2>Topic Details</th></tr>\n"
	$table .= "<tr><th>Topic Num</th><td>$topic_num</td></tr>\n"
	$table .= "<tr><th>Topic</th><td><input type=text name='topic_name' value='$topics{$topic_num}{name}'></input></td></tr>\n"
	$table .= "<tr><th>Description</th><td><textarea cols=40 rows=5 style='width:100%' name='topic_description' wrap>$topics{$topic_num}{description}</textarea></td></tr>\n"
	$table .= "<tr><td></td><td><input type=submit value='Save'></td></tr>\n"
	$table .= "</form>\n"
	$table .= "</table>\n"
	return $table
}

def SubtopicsTable {
	my ($self, $subtopic_num) = @_
	my %subtopics = Subtopics($foo, $topic_num)
	my %topic = Topic($foo, $topic_num)
	my $table = "<table class='box'>\n"
	$table .= "<tr><th colspan=3>$topic{name}</th></tr>\n"
	foreach $subtopic_num (sort { $subtopics{$a}{num} <=> $subtopics{$b}{num} } keys %subtopics) {
		$table .= "<tr><td align='right'>" . $subtopics{$subtopic_num}{num} . '</td><td>' . $subtopics{$subtopic_num}{name} . "</td>\n"
		$table .= "<td>$subtopics{$subtopic_num}{description}</td></tr>\n"
	}
	$table .= "</table>\n"
	return $table
}

def SubtopicTable {
	my ($self, $subtopic_id) = @_
	my %subtopics = Subtopics()
	my $table = "<table class='box'>\n"
	$table .= "<form name=subtopic method=POST action='subtopic_save.pl'>\n"
	$table .= "<input type=hidden name='topic_num' value='$subtopics{$subtopic_id}{topicnum}'></input>\n"
	$table .= "<input type=hidden name='subtopic_num' value='$subtopics{$subtopic_id}{num}'></input>\n"
	$table .= "<tr><th colspan=2>Subtopic Details</th></tr>\n"
	$table .= "<tr><th>Topic Num</th><td>$subtopics{$subtopic_id}{topicnum}</td></tr>\n"
	$table .= "<tr><th>Subtopic Num</th><td>$subtopics{$subtopic_id}{num}</td></tr>\n"
	$table .= "<tr><th>Subtopic</th><td><input type=text name='subtopic_name' value='$subtopics{$subtopic_id}{name}'></input></td></tr>\n"
	$table .= "<tr><th>Description</th><td><textarea cols=40 rows=5 style='width:100%' name='subtopic_description' wrap>$subtopics{$subtopic_id}{description}</textarea></td></tr>\n"
	$table .= "<tr><td></td><td><input type=submit value='Save'></td></tr>\n"
	$table .= "</form>\n"
	$table .= "</table>\n"
	return $table

def TopicDocsTable {
	my %docs = Docs()
	my %userdocs = UserDocs($foo, CurrentUserID())
	my $sql = "SELECT topic.topic_num, topic.topic_name, subtopic.subtopic_num, subtopic.subtopic_name, document.doc_id, document.title, topic_description, subtopic_description, url "
	$sql .= "FROM topic, subtopic, document_topic, document "
	$sql .= "WHERE topic.topic_num = subtopic.topic_num and topic.topic_num = document_topic.topic_num and subtopic.subtopic_num = document_topic.subtopic_num and document_topic.doc_id = document.doc_id AND document.pub_status='N' "
	$sql .= "ORDER BY topic_num, subtopic_num, title"
	$recordset=$DB->Recordset($sql)

	$last_topic_num = 0
	$last_subtopic_num = 0
	my $table = "<table><tr><td>\n"
	while (@row = $recordset->fetchrow) {
		$topic_num		= $row[0]
		$topic_name		= strip($row[1])
		$subtopic_num		= $row[2]
		$subtopic_name		= strip($row[3])
		$doc_id			= $row[4]
		$title			= strip($row[5])
		$topic_description	= strip($row[6])
		$subtopic_description	= strip($row[7])
		$url			= strip($row[8])
		if ($topic_num != $last_topic_num) {
			$table .= "<a name='$topic_num'>"
			$table .= "<h2>"
			$table .= "<a href='topic_edit.pl?topic_num=$topic_num'>" . EditImage() . "</a>" if (Admin())
			$table .= "$topic_num $topic_name"
			$table .= "</h2>"
			$table .= "<blockquote>$topic_description</blockquote>\n"
		}
		if ($subtopic_num != $last_subtopic_num) {
			$table .= "<a name='$topic_num.$subtopic_num'>"
			$table .= "<h3>"
			$table .= "<a href='subtopic_edit.pl?subtopic_id=$topic_num.$subtopic_num'>" . EditImage() . "</a>" if (Admin())
			$table .= "$topic_num.$subtopic_num $subtopic_name"
			$table .= "</h3>"
			$table .= "<blockquote>$subtopic_description</blockquote>\n"
		}
		if (Admin() or (exists $userdocs{$doc_id})) {
			$table .= "<a href='document_edit.pl?doc_id=$doc_id'>" . EditImage() . "</a>"
		}
		if ($url) {
			$table .= "<a href='$url'>$title</a>"
		}
		
		$table .= "<br>\n"

		$last_topic_num = $topic_num
		$last_subtopic_num = $subtopic_num
	}
	$table .= "</td></tr></table>\n"
	return $table
}

def ErrorsTable {
	my $message = ''
	if (scalar @errors) {
		print "<table><tr><td>\n"
		while (scalar @errors) {
			my $error = pop @errors
			$message = $error . "<p>" . $message
		}
		print "<p>$message\n"
		print "</td></tr></table>\n"
	}
}

def NavBar {
	print "<table class='navbar'><tr>\n"
	print "<th><a href='document_list.pl'>Documents</a></th>\n"
	print "<th><a href='topic_list.pl'>Topics</a></th> \n"
	print "</tr>\n"
	print "</table>\n"
}

def NavBox {
	print "<table class='navbox'>\n"
	print "<tr><th>Menu</th></tr>\n"
	print "<tr><td><a href='document_list.pl'>Document Table</a></td></tr>\n"
	print "<tr><td><a href='topic_list.pl'>Topics List</a></td></tr>\n"
	print "<tr><td><a href='statistics.pl'>Statistics</a></td></tr>\n"
	print "</table>\n"
}

def TopicsBox {
	my %topics = Topics()
	my %subtopics = Subtopics()
	print "<table class='navbox'>\n"
	print "<tr><th>Topics</th></tr>\n"
	print "<tr><td>\n"
	foreach $topic_num (sort { $a <=> $b } keys %topics) {
		print "<p>" if ($topic_num != 1)
		print "<a href='topic_list.pl#$topic_num'>$topics{$topic_num}{name}</a><br>\n"
		foreach $subtopic_num (sort { $subtopics{$a}{num} <=> $subtopics{$b}{num} } keys %subtopics) {
			if ($subtopics{$subtopic_num}{topicnum} == $topic_num) {
				print "&nbsp&nbsp<a href='topic_list.pl#$subtopic_num'>$subtopics{$subtopic_num}{name}</a><br>\n"
			}
		}
	}
	print "</td></tr>\n"
	print "</table>\n"
}

def HeaderBox {
	my ($foo, $title) = @_
	my $project = Config($foo, project)
	my $table = "<table class = 'header'><tr>\n"
	$table .= "<th>$project Lampadas System</th>"
	$table .= "</tr></table>\n"
	
	$table .= "<table class='title' style='width:100%'><tr>\n"
	$table .= "<td><h1>$title</h1></td>\n"
	$table .= "<td align='right'>\n"
	if ($currentuser_id) {
		$table .= "<a href='user_edit.pl?user_id=$currentuser{id}'>$currentuser{name}</a> "
		if (Admin()) {
			$table .= "(Administrator) "
		} elif (Maintainer()) {
			$table .= "(Maintainer) "
		}
		$table .= "<br><a href='logout.pl'>Log out</a>\n"
	}
	$table .= "</td>"
	$table .= "</tr></table>\n"
	print $table
}

def LoginBox() :
    print """<table class='navbox'>
    <form name='login' action='login.pl' method='POST'>
    <tr><th colspan='2'>Log In</th></tr>
    <tr>
    <td colspan='2' align='center'>
    <a href='newuser.pl'>Create Account</a>
    </td>
    
    <tr>
    <td align='right'>Username</td>
    <td><input type=text size=12 name=username></input></td>
    </tr>
    <tr>
    <td align='right'>Password</td>
    <td><input type=password size=12 name=password></input></td>
    </tr>
    <tr>
    <td colspan=2 align=center>
    <input type=submit name='login' value='Login'>
    <input type=submit name='mailpass' value='Mail Password'>
    </td>
    </tr>
    </form>
    </table>"""

def AdminBox() :
	return unless Admin()
	print "<p><table class='navbox'>\n"
	print "<tr><th>Admin Tools</th></tr>\n"
	print "<tr><td><a href='user_list.pl'>Manage User Accounts</a></t></tr>\n"
	print "<tr><td><a href='document_new.pl'>Add a Document</a></td></tr>\n"
	print "</td></tr></table>\n"
}

def EditImage {
	return "<img src='images/edit.png' alt='Edit' height='20' width='20' border='0' hspace='5' vspace='0' align='top'>"
}




