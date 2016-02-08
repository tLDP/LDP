#!/usr/bin/perl
#
# Copyright (C) 2003 by Virtusa Corporation
# http://www.virtusa.com
#
# Anuradha Ratnaweera
# http://www.linux.lk/~anuradha/
#

# We use %win hash to store window parameters

use Curses;

initscr();
start_color();
cbreak();

keypad(1);
noecho();
init_pair(1, COLOR_CYAN, COLOR_BLACK);

%win = ();
init_win_params(\%win);
print_win_params(\%win);

attron(COLOR_PAIR(1));
printw("Press F1 to exit");
refresh();
attroff(COLOR_PAIR(1));

create_box(\%win, 1);

while (($ch = getch()) != KEY_F(1)) {
    if ($ch == KEY_LEFT) {
	create_box(\%win, 0);
	$win{'startx'}--;
	create_box(\%win, 1);
    }
    elsif ($ch == KEY_RIGHT) {
	create_box(\%win, 0);
	$win{'startx'}++;
	create_box(\%win, 1);
    }
    elsif ($ch == KEY_UP) {
	create_box(\%win, 0);
	$win{'starty'}--;
	create_box(\%win, 1);
    }
    elsif ($ch == KEY_DOWN) {
	create_box(\%win, 0);
	$win{'starty'}++;
	create_box(\%win, 1);
    }
}

endwin();

sub init_win_params {
    $p_win = shift;

    $$p_win{'height'} = 3;
    $$p_win{'width'} = 10;
    $$p_win{'starty'} = ($LINES - $p_win{'height'}) / 2;
    $$p_win{'startx'} = ($COLS - $p_win{'width'}) / 2;
    $$p_win{'ls'} = '|';
    $$p_win{'rs'} = '|';
    $$p_win{'ts'} = '-';
    $$p_win{'bs'} = '-';
    $$p_win{'tl'} = '+';
    $$p_win{'tr'} = '+';
    $$p_win{'bl'} = '+';
    $$p_win{'br'} = '+';
}

sub print_win_params {
    if ($_DEBUG) {
	$p_win = shift;
	addstr(25, 0,
	    "$$p_win{startx} $$p_win{starty} $$p_win{width} $$p_win{height}");
	refresh();
    }
}

sub create_box {
    $p_win = shift;
    $bool = shift;

    $x = $$p_win{'startx'};
    $y = $$p_win{'starty'};
    $w = $$p_win{'width'};
    $h = $$p_win{'height'};

    if ($bool) {
	addch($y, $x, $$p_win{'tl'});
	addch($y, $x + $w, $$p_win{'tr'});
	addch($y + $h, $x, $$p_win{'bl'});
	addch($y + $h, $x + $w, $$p_win{'br'});
	hline($y, $x + 1, $$p_win{'ts'}, $w - 1);
	hline($y + $h, $x + 1, $$p_win{'bs'}, $w - 1);
	vline($y + 1, $x, $$p_win{'ls'}, $h - 1);
	vline($y + 1, $x + $w, $$p_win{'rs'}, $h - 1);
    }
    else {
	for ($j = $y; $j <= $y + $h; $j++) {
	    for ($i = $x; $i <= $x + $w; $i++) {
		addch($j, $i, ' ');
	    }
	}
    }
    refresh();
}

