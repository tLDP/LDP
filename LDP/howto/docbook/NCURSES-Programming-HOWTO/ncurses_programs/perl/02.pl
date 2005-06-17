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
raw();
keypad(1);
noecho();

printw("Type any character to see it in bold\n");
$ch = getch();

if ($ch == KEY_F(1)) {
    printw("F1 Key pressed");
}
else {
    printw("The pressed key is ");
    attron(A_BOLD);
    printw($ch);
    attroff(A_BOLD);
}

refresh();
getch();
endwin();

