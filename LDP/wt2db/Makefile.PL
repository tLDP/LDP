#!/usr/bin/perl -sw
##
## Makefile for the wt2db Perl module.
##
## Copyright (c) 2001, 2002, David Merrill. All rights reserved.
## This code is free software; you can redistribute it and/or modify
## it under the same terms as Perl itself.
##

use ExtUtils::MakeMaker;

WriteMakefile(

    NAME          => 'Wt2Db',
    AUTHOR        => 'David Merrill <david@lupercalia.net>',
    ABSTRACT      => 'Converts WikiText documents into DocBook XML.',
    NOECHO        => '',
    VERSION_FROM  => 'lib/Wt2Db.pm',
    EXE_FILES	  => 'wt2db',
    PREREQ_PM     => { 
                       'File::Basename'	=> 0,
		       'HTML::Entities'	=> 0,
		       'FileHandle'	=> 0,
                     },

);
