#!/usr/bin/perl -sw
##
## Makefile for the db2omf Perl utility.
##
## Copyright (c) 2001, Greg Ferguson. All rights reserved.
## This code is Free Software; you can redistribute it and/or modify
## it under the GNU General Public License. See COPYING for details.
##

use ExtUtils::MakeMaker;

WriteMakefile(

    NAME            => 'db2omf',
    AUTHOR          => 'Greg Ferguson <gferg@metalab.unc.edu',
    ABSTRACT        => 'Extracts OMF meta-data from DocBook documents.',
    NOECHO          => '',
    VERSION_FROM    => 'db2omf',
    EXE_FILES	    => [ qw( db2omf ) ],
    PREREQ_PM       => { 
                         'Text::Wrap'	=> 0,
                       },
    MAN1PODS        => {
                         "doc/db2omf.pod"  => 'blib/man1/db2omf.1',
                       },
);
