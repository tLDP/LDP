#!/usr/bin/perl
#
# This file is for testing the Lampadas object hierarchy. It loads and prints out
# all of the various objects, object sets, and HTML generators.
#
use Lampadas;
$L = new Lampadas;

use Lampadas::Database;
$DB = new Lampadas::Database;

&UserDocs(11);
&Doc(473);
&DocUsers(473);
&User(11);
&Roles();
&Classes();
&PubStatuses();
&Users();
&Docs();
&Config();
&NewUser();

&NavBar();
&RoleCombo();
&ClassCombo();
&PubStatusCombo();
&LicenseCombo();

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

sub User {
	my $user_id = shift;
	%user = $L->User($user_id);
	print "User $user_id:\n";
	print "UserName: $user{username}\n";
	print "Admin: $user{admin}\n";
	print "Name: $user{name}\n";
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
	$pubstatuses = $L->PubStatuses();
	print "PubStatuses:\n";
	foreach $pubstatus (keys %pubstatuses) {
		print "$pubstatus\n";
	}
	print "Count: " . scalar $pubstatuses . "\n";
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

sub LicenseCombo {
	print "LicenseCombo:\n";
	print $L->LicenseCombo("BOILERPLATE");
	print "\n";
}
