#!/usr/bin/perl
#
# This file is for testing the Lampadas object hierarchy. It loads and prints out
# all of the various objects, object sets, and HTML generators.
#
use Lampadas;
$L = new Lampadas;

use Lampadas::Database;
$DB = new Lampadas::Database;

&Topic(1);
#&UserDocs(11);
#&Doc(473);
#&DocUsers(473);
#&DocTopics(471);
#&DocNotes(471);
#&User(11);
#&Roles();
#&Classes();
#&PubStatuses();
#&ReviewStatuses();
#&Licenses();
#&Topics();
#&Subtopics();
#&Formats();
#&DTDs();
#&Users();
#&Docs();
#&Config();
#&NewUser();

#&NavBar();
#&RoleCombo();
#&ClassCombo();
#&PubStatusCombo();
#&ReviewStatusCombo();
#&TechReviewStatusCombo();
#&LicenseCombo();
#&TopicCombo();
#&SubtopicCombo();
#&FormatCombo();
#&DTDCombo();
#&UsersTable();
#&UserTable(11);
#&UserDocsTable(11);
#&DocTable(471);
#&NewDocTable();
#&DocVersionsTable(471);
#&DocUsersTable(471);
#&DocTopicsTable(471);
#&DocNotesTable(471);
#&DocCount();
#&DocCountByClass("'HOWTO'");
#&DocCountByPubStatus("'N'");

sub Topic {
	my $topic_num = shift;
	%topic = $L->Topic($topic_num);
	print "Topic: $topic{num}, $topic{name}, $topic{description}\n\n";
}

sub UserDocs {
	my $user_id = shift;
	%docs = $L->UserDocs($user_id);
	print "Documents for user $user_id:\n";
	foreach $key (keys %docs) {
		print "doc_id: $key, role: $docs{$key}{role}, active: $docs{$key}{active}\n";
	}
	print "\n";
}

sub Doc {
	my $doc_id = shift;
	%doc = $L->Doc($doc_id);
	print "Document $doc_id:\n";
	print "DocID: $doc{id}\n";
	print "Title: $doc{title}\n";
	print "Filename: $doc{filename}\n";
	print "URL: $doc{url}\n";
	print "Ref: $doc{ref_url}\n";
	print "PubStatus: $doc{pub_status}\n";
	print "ReviewStatus: $doc{review_status}\n";
	print "TR Status: $doc{tech_review_status}\n";
	print "License: $doc{license}\n";
	print "Published: $doc{pub_date}\n";
	print "Updated: $doc{last_update}\n";
	print "Version: $doc{version}\n";
	print "Format: $doc{format}\n";
	print "DTD: $doc{dtd}\n";
	print "\n";
}

sub DocUsers {
	my $doc_id = shift;
	%docusers = $L->DocUsers($doc_id);
	print "Users for document $doc_id:\n";
	foreach $key (keys %docusers) {
		print "user_id: $docusers{$key}{id}\n";
		print "username: $docusers{$key}{username}\n";
		print "first_name: $docusers{$key}{first_name}\n";
		print "middle_name: $docusers{$key}{middle_name}\n";
		print "surname: $docusers{$key}{surname}\n";
		print "name: $docusers{$key}{name}\n";
	}
	print "\n";
}

sub DocTopics {
	my $doc_id = shift;
	my %doctopics = $L->DocTopics($doc_id);
	print "Topics for document $doc_id:\n";
	foreach $key (keys %doctopics) {
		print "topic: $doctopics{$key}{topic_num}, ";
		print "$doctopics{$key}{subtopic_num}, ";
		print "$doctopics{$key}{topic_name}, ";
		print "$doctopics{$key}{subtopic_name}\n";
	}
	print "\n";
}

sub DocNotes {
	my $doc_id=shift;
	my %docnotes = $L->DocNotes($doc_id);
	print "Notes for document $doc_id:\n";
	foreach $date_entered (sort keys %docnotes) {
		print "date_entered: $date_entered\n";
		print "username: $docnotes{$date_entered}{username}\n";
		print "notes: $docnotes{$date_entered}{notes}\n";
	}
	print "\n";
}

sub User {
	my $user_id = shift;
	%user = $L->User($user_id);
	print "User $user_id:\n";
	print "UserName: $user{username}\n";
	print "Admin: $user{admin}\n";
	print "Name: $user{name}\n";
	print "Notes: $user{notse}\n";
	print "\n";
}

sub Roles {
	%roles = $L->Roles();
	print "Roles: \n";
	foreach $role (keys %roles) {
		print "$role\n";
	}
	print "Count: " . scalar $roles . "\n";
	print "\n";
}

sub Classes {
	%classes = $L->Classes();
	print "Classes: \n";
	foreach $class (keys %classes) {
		print "$class\n";
	}
	print "Count: " . scalar $classes . "\n";
	print "\n";
}

sub PubStatuses {
	%pubstatuses = $L->PubStatuses();
	print "PubStatuses:\n";
	foreach $pubstatus (keys %pubstatuses) {
		print "$pubstatus: $pubstatuses{$pubstatus}{name}\n";
	}
	print "Count: " . scalar $pubstatuses . "\n";
	print "\n";
}

sub ReviewStatuses {
	%reviewstatuses = $L->ReviewStatuses();
	print "ReviewStatuses:\n";
	foreach $reviewstatus (keys %reviewstatuses) {
		print "$reviewstatus: $reviewstatuses{$reviewstatus}{name}\n";
	}
	print "Count: " . scalar $reviewstatuses . "\n";
	print "\n";
}

sub Licenses {
	%licenses = $L->Licenses();
	print "Licenses:\n";
	foreach $license (keys %licenses) {
		print "$license\n";
	}
	print "Count: " . scalar $licenses . "\n";
	print "\n";
}

sub Topics {
	%topics = $L->Topics();
	print "Topics:\n";
	foreach $topic (sort { $a <=> $b } keys %topics) {
		print $topics{$topic}{num} . ", " . $topics{$topic}{name} . ", " . $topics{$topic}{description} . "\n";
	}
	print "Count: " . scalar $topics . "\n";
	print "\n";
}

sub Subtopics {
	%subtopics = $L->Subtopics();
	print "Subtopics:\n";
	foreach $subtopic (sort { $a <=> $b } keys %subtopics) {
		print $subtopics{$subtopic}{topicnum} . "." . $subtopics{$subtopic}{num} . " " . $subtopics{$subtopic}{name} . ", " . $subtopics{$subtopic}{description} . "\n";
	}
	print "Count: " . scalar $topics . "\n";
	print "\n";
}

sub Formats {
	%formats = $L->Formats();
	print "Formats:\n";
	foreach $format (sort { $format{$a}{name} <=> $format{$b}{name} } keys %formats) {
		print "$format: $formats{$format}{name}\n";
	}
	print "\n";
}

sub DTDs {
	%dtds = $L->DTDs();
	print "DTDs:\n";
	foreach $dtd (sort { $dtd{$a}{dtd} <=> $dtd{$b}{dtd} } keys %dtds) {
		print "$dtd: $dtds{$dtd}{dtd}\n";
	}
	print "\n";
}

sub Users {
	%users = $L->Users();
	print "Users:\n";
	foreach $key (keys %users) {
		print "user_id: $key, name: $users{$key}{name}\n";
	}
	print "\n";
}

sub Docs {
	%docs = $L->Docs();
	print "Documents:\n";
	foreach $key (sort {uc($docs{$a}{title}) cmp uc($docs{$b}{title})} keys %docs) {
		print "doc_id: $docs{$key}{id}, title: $docs{$key}{title}\n";
	}
	print "\n";
}

sub Config {
	print "Version:" . $L->Config('version') . "\n";
	print "Cookie Domain:" . $L->Config('cookie_domain') . "\n";
	print "\n";
}

sub NewUser {
	%newuser = $L->NewUser('test user', 'test', 'x.', 'user', 'test@example.com', 't', 'password');
	print "New User: " . $newuser{username} . "\n";
	print "\n";
	$DB->Exec("DELETE FROM username WHERE username='test user'");
}

sub NavBar {
	print "NavBar:\n";
	$L->NavBar();
	print "\n";
}

sub RoleCombo {
	print "RoleCombo:\n";
	print $L->RoleCombo("Maintainer");
	print "\n";
}

sub ClassCombo {
	print "ClassCombo:\n";
	print $L->ClassCombo();
	print "\n";
}

sub PubStatusCombo {
	print "PubStatusCombo:\n";
	print $L->PubStatusCombo("D");
	print "\n";
}

sub ReviewStatusCombo {
	print "ReviewStatusCombo:\n";
	print $L->ReviewStatusCombo("P");
	print "\n";
}

sub TechReviewStatusCombo {
	print "TechReviewStatusCombo:\n";
	print $L->TechReviewStatusCombo("P");
	print "\n";
}

sub LicenseCombo {
	print "LicenseCombo:\n";
	print $L->LicenseCombo("GFDL");
	print "\n";
}

sub TopicCombo {
	print "TopicCombo:\n";
	print $L->TopicCombo("5");
	print "\n";
}

sub SubtopicCombo {
	print "SubtopicCombo:\n";
	print $L->SubtopicCombo("5.1");
	print "\n";
}

sub FormatCombo {
	print "FormatCombo:\n";
	print $L->FormatCombo("XML");
	print "\n";
}

sub DTDCombo {
	print "DTDCombo:\n";
	print $L->DTDCombo("DocBook");
	print "\n";
}

sub UsersTable {
	print "UsersTable:\n";
	print $L->UsersTable();
	print "\n";
}

sub UserTable {
	my $user_id = shift;
	print "UserTable:\n";
	print $L->UserTable($user_id);
	print "\n";
}

sub UserDocsTable {
	my $user_id = shift;
	print "UserDocsTable:\n";
	print $L->UserDocsTable($user_id);
	print "\n";
}

sub DocTable {
	my $doc_id = shift;
	print "DocTable:\n";
	print $L->DocTable($doc_id);
	print "\n";
}

sub NewDocTable {
	print "NewDocTable:\n";
	print $L->NewDocTable();
	print "\n";
}

sub DocVersionsTable {
	my $doc_id = shift;
	print "DocVersionsTable:\n";
	print $L->DocVersionsTable($doc_id);
	print "\n";
}

sub DocUsersTable {
	my $doc_id = shift;
	print "DocUsersTable:\n";
	print $L->DocUsersTable($doc_id);
	print "\n";
}

sub DocTopicsTable {
	my $doc_id = shift;
	print "DocTopicsTable:\n";
	print $L->DocTopicsTable($doc_id);
	print "\n";
}

sub DocNotesTable {
	my $doc_id = shift;
	print "DocNotesTable:\n";
	print $L->DocNotesTable($doc_id);
	print "\n";
}

sub DocCount {
	print "Document Count: " . $L->DocCount() . "\n\n";
}

sub DocCountByClass {
	my $class = shift;
	print "Document Count by Class: " . $L->DocCountByClass($class) . "\n\n";
}

sub DocCountByPubStatus {
	my $pub_status = shift;
	print "Document Count by Pub Status: " . $L->DocCountByPubStatus($pub_status) . "\n\n";
}

