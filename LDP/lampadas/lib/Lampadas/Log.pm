#!/usr/bin/perl
# 
# This package provides Perl bindings for the Lampadas database,
# routines for accessing the CGI environment,
# and HTML generators for creating the web front end.
# 
package Lampadas::Log;

use Exporter;
@ISA	= qw(Exporter);
@EXPORT	= qw(
	new,
	Log
);

$debug = 0;			# Set this to 1 to get debugging messages

sub new {
	my $that = shift;
	my $class = ref($that) || $that;
	my $self = {};
	bless $self, $class;
	return $self;
}

sub Log {
	my $self = shift;
	my $message = shift;
}
1;
