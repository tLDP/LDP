#!/usr/bin/perl
#
# Copyright (C) 2003 by Virtusa Corporation
# http://www.virtusa.com
#
# Anuradha Ratnaweera
# http://www.linux.lk/~anuradha/
#

use Curses;

$width = 30;
$height = 10;
$startx = 0;
$starty = 0;

@choices = (
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Exit"
);

$n_choices = @choices;

$highlight = 1;
$choice = 0;

initscr();
clear();
noecho();
cbreak();
$startx = ($COLS - $width) / 2;
$starty = ($LINES - $height) / 2;

$menu_win = newwin($height, $width, $starty, $startx);
keypad(1);
keypad($menu_win, 1);
addstr(0, 0, "Use arrow keys to go up and down, Press enter to select a choice");
refresh();
print_menu($menu_win, $highlight);

while (1) {
    $c = getch($menu_win);
    if ($c == KEY_UP) {
	if ($highlight == 1) {
	    $highlight = $n_choices;
	}
	else {
	    $highlight--;
	}
    }
    elsif ($c == KEY_DOWN) {
	if ($highlight == $n_choices) {
	    $highlight = 1;
	}
	else {
	    $highlight++;
	}
    }
    elsif ($c == '\n') {
	$choice = $highlight;
    }
    else {
	addstr($LINES - 2, 0, "Character pressed is $c");
	refresh();
    }
    print_menu($menu_win, $highlight);
    last if ($choice);
}

addstr($LINES - 2, 0, "You chose choice $choice with choice string $choices[$choice-1]");
clrtoeol();
refresh();
endwin();

sub print_menu {
    $menu_win = shift;
    $highlight = shift;

    $x = 2;
    $y = 2;
    box($menu_win, 0, 0);
    for ($i = 0; $i < $n_choices; $i++) {
	if ($highlight == $i + 1) {
	    attron($menu_win, A_REVERSE);
	    addstr($menu_win, $y, $x, $choices[$i]);
	    attroff($menu_win, A_REVERSE);
	}
	else {
	    addstr($menu_win, $y, $x, $choices[$i]);
	}
	$y++;
    }
    refresh($menu_win);
}

