#!/bin/sh
#
# First level of configuration
#
# Adapt this file to your needs. For a typical installation you
# have to change only one variable, LAMPADAS_ROOT.
#
# Include this file in your ~/.bashrc (e.g. with ". bin/setenv.sh")
# Users of csh should convert the syntax with
# 
#     sed -e 's/^export/setenv/' -e 's/=/ /' setenv.sh > setenv.csh
#
# and then include setenv.csh in their .cshrc (e.g. "source bin/setenv.csh")

# directory you unpacked lampadas to
export LAMPADAS_ROOT=$HOME/cvs/LDP/lampadas

# used by bin/lampadasdb to initialize the database
export LAMPADAS_SQL=$LAMPADAS_ROOT/database/tables

# generated files that are not automatically deleted after use
export LAMPADAS_SPOOL=/tmp

# used by bin/lampadasweb to find the file lampadas.conf
export LAMPADAS_ETC=$LAMPADAS_ROOT/conf

# used by pylib/Makefile.py to locate XSLT stylesheets
export LAMPADAS_XSL=$LAMPADAS_ROOT/xsl
