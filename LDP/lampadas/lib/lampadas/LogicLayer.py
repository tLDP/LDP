#!/usr/bin/python

"""
Lampadas system

This modules provides functions implementing some application logic,
like login/logout, adding/updating/removing users, etc.
"""

__version__ = '0.2'

def login(username, password) :
    """
    Logs in a user
    """

    # if username does not exists in database :
    #    raise UnknownUserException
    # if password not ok :
    #    raise BadPasswordException
    #
    # if user has session_id :
    #    reuse it
    # else :
    #    generate a new one and write it down in DB


def generate_cookie() :
    """
    Return a generated cookie
    """
    # $cookie_domain = Config($foo, 'cookie_domain')
    # $cookie = string::random
    # cookie_name = 'lampadas_session'
    # cookie_value = session_id
    # cookie_epxires = '+1M'
    pass

def logout() :
    """
    Log out
    """
    # cookie_value = ''
    # session_id = ''

def add_user() :
    """
    Add a new user
    """
    # my ($self, $username, $first_name, $middle_name, $surname, $email, $admin, $password, $notes) = @_

    # if username or missing missing :
    #   raise MissingInfoException
    # if username exists :
    #   raise DuplicateAccountException
    # if email exists :
    #   raise DuplicateAccountException
    #
    # add user to DB

def update_user() :
    """
    Update user information

    XXXFIXME: duplicate with Database.update_user() ?
    """
    # UPDATE username SET username=" . wsq($username) . ", first_name=" . wsq($first_name) . ", middle_name=" . wsq($middle_name) . ", surname=" . wsq($surname) . ", email=" . wsq($email) . ", admin=" . wsq($admin) . ", notes=" . wsq($notes) . " WHERE user_id=$user_id")
    pass

def redirect(url) :
    """
    Redirect to another URL
    """
	my $url = shift
	unless ($url =~ /http/) {
		my $hostname = Config($foo, 'hostname')
		my $rootdir = Config($foo, 'root_dir')
		$url = 'http://' . $hostname . $rootdir . $url
	}
	print $CGI->redirect($url)
	exit

def Mail() :
    """
    Send an e-mail
    """
	use Mail::Sendmail
	my $self = shift
	my ($to, $subject, $message) = @_
	my $from = Config($foo, 'local_email')
	my $smtp = Config($foo, 'smtp_server')
	my %mail = (to		=> $to,
		    from	=> $from,
		    subject	=> $subject,
		    message	=> $message,
		    smtp	=> $smtp)
	unless (&Mail::Sendmail::sendmail(%mail)) {
		push @errors, "Error sending mail"
	}
