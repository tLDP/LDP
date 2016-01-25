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
cbreak();
keypad(1);

$height = 3;
$width = 10;
$starty = ($LINES - $height) / 2;
$startx = ($COLS - $width) / 2;
printw("Press F1 to exit");
refresh();
$my_win = create_newwin($height, $width, $starty, $startx);

while (($ch = getch()) != KEY_F(1)) {
    if ($ch == KEY_LEFT) {
	destroy_win($my_win);
	$my_win = create_newwin($height, $width, $starty, --$startx);
    }
    elsif ($ch == KEY_RIGHT) {
	destroy_win($my_win);
	$my_win = create_newwin($height, $width, $starty, ++$startx);
    }
    elsif ($ch == KEY_UP) {
	destroy_win($my_win);
	$my_win = create_newwin($height, $width, --$starty, $startx);
    }
    elsif ($ch == KEY_DOWN) {
	destroy_win($my_win);
	$my_win = create_newwin($height, $width, ++$starty, $startx);
    }
}

endwin();

sub create_newwin {
    $local_win = newwin(shift, shift, shift, shift);
    box($local_win, 0, 0);
    refresh($local_win);
    return $local_win;
}

sub destroy_win {
    $local_win = shift;
    border($local_win, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ');
    refresh($local_win);
    delwin($local_win);
}

