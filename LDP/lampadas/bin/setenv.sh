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
export LAMPADAS_ROOT="$HOME/cvs/LDP/lampadas"

# used by bin/lampadasdb to initialize the database
# location of create.sql and insert.m4
export LAMPADAS_SQL="$LAMPADAS_ROOT/database/tables"

# use by commands 'insert' and 'update' of bin/lampadasdb
# to locate data files (e.g. EN.m4, DE.m4).
export LAMPADAS_DATA="$LAMPADAS_SQL"

# generated files that are not automatically deleted after use
export LAMPADAS_SPOOL=/tmp

# database name to connect to. see psql(1)
export LAMPADAS_DB=lampadas

# used by bin/lampadasweb to find the file lampadas.conf
export LAMPADAS_ETC="$LAMPADAS_ROOT/conf"

# used by pylib/Makefile.py to locate XSLT stylesheets
export LAMPADAS_XSL="$LAMPADAS_ROOT/xsl"

# used by cron/lampadas to run cron jobs
export LAMPADAS_CRON="$LAMPADAS_ROOT/cron"

# used by cron job to update the CVS tree and mirror it
export LAMPADAS_CVS=/var/cache/lampadas/LDP

# used by cron job to mirror, write makefiles and build outputs
export LAMPADAS_CACHE=/var/cache/lampadas/docs

# used by cron job to locate utilities
export LAMPADAS_BIN="$LAMPADAS_ROOT/bin"

# used by cron job to locate utilities
export LAMPADAS_LIB="$LAMPADAS_ROOT/pylib"

#
# PYTHON
#
export PYTHON=/usr/bin/python
export PYTHONPATH="$PYTHONPATH\:$LAMPADAS_LIB"

#
# DocBook SYSTEM identifiers
#

# http://docbook.org/xml/4.1.2/docbookx.dtd
export LAMPADAS_XML_DTD_412=

# ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN//XML
export LAMPADAS_XML_ISO_NUM=
