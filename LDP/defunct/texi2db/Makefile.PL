#!/usr/bin/perl -sw
##
## Makefile for the texi2db utility.
##
## Copyright (c) 2002, 2003 David Merrill <david@lupercalia.net.
## All rights reserved.
##
## This code is Free Software; you can redistribute it and/or modify
## it under the GNU General Public License. See COPYING for details.
##

use ExtUtils::MakeMaker;

WriteMakefile(

    NAME            => 'texi2db',
    AUTHOR          => 'David Merrill <david@lupercalia.net>',
    ABSTRACT        => 'Converts Texinfo documents into DocBook XML.',
    NOECHO          => '',
    VERSION_FROM    => 'texi2db',
    EXE_FILES	    => [ qw( texi2db ) ],
    PREREQ_PM       => { 
                         'File::Basename'	=> 0,
		         'HTML::Entities'	=> 0,
		         'FileHandle'	=> 0,
                       },
    MAN1PODS        => {
                         "doc/texi2db.pod"  => 'blib/man1/texi2db.1',
                       },
);
