#!/usr/bin/perl
#
# Copyright (C) 2003 by Virtusa Corporation
# http://www.virtusa.com
#
# Anuradha Ratnaweera
# http://www.linux.lk/~anuradha/
#

# We first read all the input into an array and join
# it to a single string with newlines.

use Curses;

initscr();

@lines = <>;
$lines = join "", @lines;

while ($lines =~ /\G(.*?)(\/\*.*?\*\/)?/gs) {
    addstr($1);
    if ($2) {
	attron(A_BOLD);
	addstr($2);
	attroff(A_BOLD);
    }
}

refresh();
getch();
endwin();

