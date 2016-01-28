#include <form.h>

#define STARTX 15
#define STARTY 4
#define WIDTH 25

#define N_FIELDS 3

int main()
{	FIELD *field[N_FIELDS];
	FORM  *my_form;
	int ch, i;
	
	/* Initialize curses */
	initscr();
	cbreak();
	noecho();
	keypad(stdscr, TRUE);

	/* Initialize the fields */
	for(i = 0; i < N_FIELDS - 1; ++i)
		field[i] = new_field(1, WIDTH, STARTY + i * 2, STARTX, 0, 0);
	field[N_FIELDS - 1] = NULL;

	/* Set field options */
	set_field_back(field[1], A_UNDERLINE); 	/* Print a line for the option 	*/
	
	field_opts_off(field[0], O_ACTIVE); /* This field is a static label */
	field_opts_off(field[1], O_PUBLIC); /* This filed is like a password field*/
	field_opts_off(field[1], O_AUTOSKIP); /* To avoid entering the same field */
					      /* after last character is entered */
	
	/* Create the form and post it */
	my_form = new_form(field);
	post_form(my_form);
	refresh();
	
	set_field_just(field[0], JUSTIFY_CENTER); /* Center Justification */
	set_field_buffer(field[0], 0, "This is a static Field"); 
						  /* Initialize the field  */
	mvprintw(STARTY, STARTX - 10, "Field 1:");
	mvprintw(STARTY + 2, STARTX - 10, "Field 2:");
	refresh();

	/* Loop through to get user requests */
	while((ch = getch()) != KEY_F(1))
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
