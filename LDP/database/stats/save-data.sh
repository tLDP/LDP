#!/bin/sh
#
psql ldp -f ../tables/save.sql
cp /tmp/ldp_*.txt ../tables/data

