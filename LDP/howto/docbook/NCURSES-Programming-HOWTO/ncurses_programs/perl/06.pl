#!/usr/bin/perl
#
# Copyright (C) 2003 by Virtusa Corporation
# http://www.virtusa.com
#
# Anuradha Ratnaweera
# http://www.linux.lk/~anuradha/
#

use Curses;

initscr();
start_color();

init_pair(1, COLOR_CYAN, COLOR_BLACK);
printw("A Big string which i didn't care to type fully ");
chgat(0, 0, -1, A_BLINK, 1, NULL);

refresh();
getch();
endwin();

