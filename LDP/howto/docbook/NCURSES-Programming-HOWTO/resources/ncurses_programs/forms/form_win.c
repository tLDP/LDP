#include <form.h>

void print_in_middle(WINDOW *win, int starty, int startx, int width, char *string, chtype color);

int main()
{
	FIELD *field[3];
	FORM  *my_form;
	WINDOW *my_form_win;
	int ch, rows, cols;
	
	/* Initialize curses */
	initscr();
	start_color();
	cbreak();
	noecho();
	keypad(stdscr, TRUE);

	/* Initialize few color pairs */
   	init_pair(1, COLOR_RED, COLOR_BLACK);

	/* Initialize the fields */
	field[0] = new_field(1, 10, 6, 1, 0, 0);
	field[1] = new_field(1, 10, 8, 1, 0, 0);
	field[2] = NULL;

	/* Set field options */
	set_field_back(field[0], A_UNDERLINE);
	field_opts_off(field[0], O_AUTOSKIP); /* Don't go to next field when this */
					      /* Field is filled up 		*/
	set_field_back(field[1], A_UNDERLINE); 
	field_opts_off(field[1], O_AUTOSKIP);
	
	/* Create the form and post it */
	my_form = new_form(field);
	
	/* Calculate the area required for the form */
	scale_form(my_form, &rows, &cols);

	/* Create the window to be associated with the form */
        my_form_win = newwin(rows + 4, cols + 4, 4, 4);
        keypad(my_form_win, TRUE);

	/* Set main window and sub window */
        set_form_win(my_form, my_form_win);
        set_form_sub(my_form, derwin(my_form_win, rows, cols, 2, 2));

	/* Print a border around the main window and print a title */
        box(my_form_win, 0, 0);
	print_in_middle(my_form_win, 1, 0, cols + 4, "My Form", COLOR_PAIR(1));
	
	post_form(my_form);
	wrefresh(my_form_win);

	mvprintw(LINES - 2, 0, "Use UP, DOWN arrow keys to switch between fields");
	refresh();

	/* Loop through to get user requests */
	while((ch = wgetch(my_form_win)) != KEY_F(1))
	{	switch(ch)
		{	case KEY_DOWN:
				/* Go to next field */
				form_driver(my_form, REQ_NEXT_FIELD);
				/* Go to the end of the present buffer */
				/* Leaves nicely at the last character */
				form_driver(my_form, REQ_END_LINE);
				break;
			case KEY_UP:
				/* Go to previous field */
				form_driver(my_form, REQ_PREV_FIELD);
				form_driver(my_form, REQ_END_LINE);
				break;
			default:
				/* If this is a normal character, it gets */
				/* Printed				  */	
				form_driver(my_form, ch);
				break;
		}
	}

	/* Un post form and free the memory */
	unpost_form(my_form);
	free_form(my_form);
	free_field(field[0]);
	free_field(field[1]); 

	endwin();
	return 0;
}

void print_in_middle(WINDOW *win, int starty, int startx, int width, char *string, chtype color)
{	int length, x, y;
	float temp;

	if(win == NULL)
		win = stdscr;
	getyx(win, y, x);
	if(startx != 0)
		x = startx;
	if(starty != 0)
		y = starty;
	if(width == 0)
		width = 80;

	length = strlen(string);
	temp = (width - length)/ 2;
	x = startx + (int)temp;
	wattron(win, color);
	mvwprintw(win, y, x, "%s", string);
	wattroff(win, color);
	refresh();
}
