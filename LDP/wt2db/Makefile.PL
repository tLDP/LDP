#!/usr/bin/perl -sw
##
## Makefile for the wt2db Perl module.
##
## Copyright (c) 2001, 2002, 2003 David Merrill <david@lupercalia.net>.
## All rights reserved.
##
## This code is Free Software; you can redistribute it and/or modify
## it under the GNU General Public License. See COPYING for details.
##

use ExtUtils::MakeMaker;

WriteMakefile(

    NAME            => 'Wt2Db',
    AUTHOR          => 'David Merrill <david@lupercalia.net>',
    ABSTRACT        => 'Converts WikiText documents into DocBook XML/SGML.',
    NOECHO          => '',
    VERSION_FROM    => 'wt2db',
    EXE_FILES	    => [ qw( wt2db ) ],
    PREREQ_PM       => { 
                         'File::Basename'	=> 0,
                         'HTML::Entities'	=> 0,
                         'FileHandle'		=> 0,
                       },
    MAN1PODS        => {
                         "doc/wt2db.pod"  => 'blib/man1/wt2db.1',
                       },
);

