#include <curses.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define HSIZE 60
#define LENGTH 75
#define WIDTH 10
#define STARTX 1
#define STARTY 5
#define STATUSX 1
#define STATUSY 25

#define KEY_F1 265

int print_menu();
void print_byebye();
void create_test_string();
void print_time(time_t startt, time_t endt, int mistakes);
void print_in_middle(int startx, int starty, int width, char *string, WINDOW *win);

char *groups[] = {  "`123456" ,
					"7890-="  ,
					"~!@#$%^" ,
					"&*()_+"  ,
					"<>?" 	  , 	 
					",./\\"	  ,
					"asdfg",
					"jkl;'",
					"qwer",
					"uiop",
					"tyur",
					"zxcv",
					"bnm",
				  };
int n_groups;

int main()
{	int choice, i;
	char *test_array;
	int ch = KEY_F1;
	int mistakes;
	int x, y;
	time_t start_t, end_t;
	WINDOW *typing_win;
	char string[80];
	
	string[0] = '\0';
						
	initscr();
	cbreak();
	noecho();
	keypad(stdscr, TRUE);
	intrflush(stdscr, FALSE);
	
	srandom(time(NULL));
	n_groups = sizeof(groups) / sizeof(char *);
	test_array = (char *)calloc(HSIZE + 1, sizeof(char));
	
	while(1)
	{		
		if(ch == KEY_F1)
		{	choice = print_menu();
			choice -= 1;
			if(choice == n_groups)
			{	print_byebye();
				free(test_array);
				endwin();
				exit(0);
			}
		}
		clear();
		strcpy(string, "Typing window");
		print_in_middle(STARTX, STARTY - 2, LENGTH, string, NULL);
		attron(A_REVERSE);
		mvprintw(STATUSY, STATUSX, "Press F1 to Main Menu");
		refresh();
		attroff(A_REVERSE);

		create_test_string(test_array, choice);
		typing_win = newwin(WIDTH, LENGTH, STARTY, STARTX);
		keypad(typing_win, TRUE);
		intrflush(typing_win, FALSE);
		box(typing_win, 0, 0);
	
		x = 1;
		y = 1;
		mvwprintw(typing_win, y, x, "%s", test_array);
		wrefresh(typing_win);
		y += 1;
	
		mistakes = 0;
		i = 0;
		time(&start_t);
		wmove(typing_win, y, x);
		wrefresh(typing_win);
		ch = 0;
		while(ch != KEY_F1 && i != HSIZE + 1)
		{	ch = wgetch(typing_win);
			mvwprintw(typing_win, y, x, "%c", ch);
			wrefresh(typing_win);
			++x;
			if(ch == test_array[i])
			{	++i;
				continue;
			}
			else
			{	++mistakes;
				++i;
			}
		}
	
		time(&end_t);
		print_time(start_t, end_t, mistakes);
	}
	free(test_array);
	endwin();
	return 0;
}
		

int print_menu()
{	int choice, i;
	
	choice = 0;
	while(1)
	{	clear();
		printw("\n\n");
		print_in_middle(1, 1, 0, "* * *   Welcome to typing practice (Version 1.0) * * * ", NULL);
		printw("\n\n\n");
		for(i = 0;i <= n_groups - 1; ++i)
			printw("\t%3d: \tPractice %s\n", i + 1, groups[i]);
		printw("\t%3d: \tExit\n", i + 1);
	
		printw("\n\n\tChoice: ");
		refresh();
		echo();
		scanw("%d", &choice);
		noecho();
	
		if(choice >= 1 && choice <= n_groups + 1)
			break;
		else
		{	attron(A_REVERSE);
			mvprintw(STATUSY, STATUSX, "Wrong choice\tPress any key to continue");
			attroff(A_REVERSE);
			getch();
		}
	}
	return choice;
}

void create_test_string(char *test_array, int choice)
{	int i, index, length;
	
	length = strlen(groups[choice]);
	for(i = 0;i <= HSIZE - 1; ++i)
	{	if(i%5 == 0)
			test_array[i] = ' ';
		else
		{	index = (int)(random() % length);
			test_array[i] = groups[choice][index];
		}
	}
	test_array[i] = '\0';
}	
	
void print_byebye()
{	printw("\n");
	print_in_middle(0,0,0,"Thank you for using my typing tutor\n", NULL);
	print_in_middle(0,0,0,"Bye Bye ! ! !\n", NULL);
	refresh();
}
		
void print_time(time_t start_t, time_t end_t, int mistakes)
{	long int diff;
	int h,m,s;
	float wpm;

	diff = end_t - start_t;
	wpm = ((HSIZE / 5)/(double)diff)*60;

	h = (int)(diff / 3600);
    diff -= h * 3600;
	m = (int)(diff / 60);
	diff -= m * 60;
	s = (int)diff; 
	
	attron(A_REVERSE);
	mvprintw(STATUSY, STATUSX, "Mistakes made : %d time taken: %d:%d:%d WPM : %.2f    Press any Key to continue", mistakes, h, m, s, wpm);
	attroff(A_REVERSE);

	refresh();
	getch();

}

/* ---------------------------------------------------------------- *
 * startx = 0 means at present x 									*
 * starty = 0 means at present y									*
 * win = NULL means take stdscr 									*
 * ---------------------------------------------------------------- */

void print_in_middle(int startx, int starty, int width, char *string, WINDOW *win)
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
	mvwprintw(win, y, x, "%s", string);
	refresh();
}
