#!/usr/bin/perl -sw
##
## Makefile for the Lampadas Perl module.
##
## Copyright (c) 2000, 2001, 2002, David Merrill. All rights reserved.
## This code is free software; you can redistribute it and/or modify
## it under the same terms as Perl itself.
##

use ExtUtils::MakeMaker;

WriteMakefile(

    NAME          => 'Lampadas',
    AUTHOR        => 'David Merrill <david@lupercalia.net>',
    ABSTRACT      => 'Online collaborative document management system.',
    NOECHO        => '',
    VERSION_FROM  => 'lib/Lampadas.pm',
    EXE_FILES	  => '',
    PREREQ_PM     => { 
                       'Mail::Sendmail'	=> 0,
		       'String::Random'	=> 0,
		       'CGI'		=> 0,
		       'Pg'		=> 0,
		       'FileHandle'	=> 0,
		       'Date::Calc'	=> 0,
		       'Wt2Db'		=> 0,
                     },

);
