#include <curses.h>

#define POSX 10
#define POSY 5
#define DISC_CHAR '*'
#define PEG_CHAR '#'
#define TIME_OUT 300

typedef struct _peg_struct {
	int n_discs;		/* Number of discs at present 	*/
	int bottomx, bottomy;	/* bottom x, bottom y co-ord  	*/
	int *sizes;		/* The disc sizes array		*/
}peg;

void init_pegs(peg *p_my_pegs, int n_discs);
void show_pegs(WINDOW *win, peg *p_my_pegs, int n_discs);
void free_pegs(peg *p_my_pegs, int n_discs);
void solve_hanoi(peg *p_my_pegs, int n, int src, int aux, int dst);
void move_disc(peg *p_my_pegs, int n_discs, int src, int dst);
void print_in_middle(int startx, int starty, int width, char *string, WINDOW *win);
void check_usr_response(peg *p_my_pegs, int n_discs);

int store_n_discs;
char *welcome_string = "Enter the number of discs you want to be solved: ";

int main(int argc, char *argv[])
{	int n_discs;
	peg my_pegs[3];

	initscr();	/* Start curses mode 		*/
	cbreak();	/* Line buffering disabled. Pass on every thing */
	keypad(stdscr, TRUE);
	curs_set(FALSE);
	
	print_in_middle(0, LINES / 2, COLS, welcome_string, NULL);
	scanw("%d", &n_discs);	

	timeout(TIME_OUT);
	noecho();
	store_n_discs = n_discs;

	init_pegs(my_pegs, n_discs);
	show_pegs(stdscr, my_pegs, n_discs);
	solve_hanoi(my_pegs, n_discs, 0, 1, 2);

	free_pegs(my_pegs, n_discs);
	endwin();		/* End curses mode		  */
	return 0;
}

void solve_hanoi(peg *p_my_pegs, int n_discs, int src, int aux, int dst)
{	if(n_discs == 0)
		return;
	solve_hanoi(p_my_pegs, n_discs - 1, src, dst, aux);
	move_disc(p_my_pegs, store_n_discs, src, dst);
	show_pegs(stdscr, p_my_pegs, store_n_discs);
	check_usr_response(p_my_pegs, store_n_discs);
	solve_hanoi(p_my_pegs, n_discs - 1, aux, src, dst);
}

void check_usr_response(peg *p_my_pegs, int n_discs)
{	int ch;

	ch = getch(); /* Waits for TIME_OUT milliseconds */
	if(ch == ERR)
		return;
	else	
		if(ch == KEY_F(1))
		{	free_pegs(p_my_pegs, n_discs);
			endwin();
			exit(0);
		}
}

void move_disc(peg *p_my_pegs, int n_discs, int src, int dst)
{	int temp, index;

	--p_my_pegs[src].n_discs;
	index = 0;
	while(p_my_pegs[src].sizes[index] == 0 && index != n_discs)
		++index;
	temp = p_my_pegs[src].sizes[index];
	p_my_pegs[src].sizes[index] = 0;
	
	index = 0;
	while(p_my_pegs[dst].sizes[index] == 0 && index != n_discs)
		++index;
	--index;
	p_my_pegs[dst].sizes[index] = temp;
	++p_my_pegs[dst].n_discs;
}	

void init_pegs(peg *p_my_pegs, int n_discs)
{	int size, temp, i;

	p_my_pegs[0].n_discs = n_discs;
	
	/* Allocate memory for size array 		
	 * atmost the number of discs on a peg can be n_discs
 	 */
	for(i = 0; i < n_discs; ++i)	
		p_my_pegs[i].sizes = (int *)calloc(n_discs, sizeof(int));
	size = 3;
	for(i = 0;i < n_discs; ++i, size += 2)
		p_my_pegs[0].sizes[i] = size;

	temp = (p_my_pegs[0].sizes[n_discs - 1] / 2);
 	p_my_pegs[0].bottomx = POSX + 1 + temp;
	p_my_pegs[0].bottomy = POSY + 2 + n_discs;
	
 	p_my_pegs[1].bottomx = p_my_pegs[0].bottomx + 2 + 2 * temp;
	p_my_pegs[1].bottomy = POSY + 2 + n_discs;
	
 	p_my_pegs[2].bottomx = p_my_pegs[1].bottomx + 2 + 2 * temp; 
	p_my_pegs[2].bottomy = POSY + 2 + n_discs;
}	    

void show_pegs(WINDOW *win, peg *p_my_pegs, int n_discs)
{	int i, j, k, x, y, size;
	
	wclear(win);
	attron(A_REVERSE);
	mvprintw(24, 0, "Press F1 to Exit");
	attroff(A_REVERSE);
	for(i = 0;i < 3; ++i)
		mvwprintw(	win, p_my_pegs[i].bottomy - n_discs - 1, 
					p_my_pegs[i].bottomx, "%c", PEG_CHAR);
	y = p_my_pegs[0].bottomy - n_discs;
	for(i = 0; i < 3; ++i)	/* For each peg */
	{	for(j = 0; j < n_discs; ++ j)	/* For each row */
		{	if(p_my_pegs[i].sizes[j] != 0)
			{	size = p_my_pegs[i].sizes[j];
				x = p_my_pegs[i].bottomx - (size / 2);
				for(k = 0; k < size; ++k)
					mvwprintw(win, y, x + k, "%c", DISC_CHAR);
			}
			else	
				mvwprintw(win, y, p_my_pegs[i].bottomx, "%c", PEG_CHAR);
			++y;
		}
		y = p_my_pegs[0].bottomy - n_discs;	
	}
	wrefresh(win);
}

void free_pegs(peg *p_my_pegs, int n_discs)
{	int i;

	for(i = 0;i < n_discs; ++i)
    		free(p_my_pegs[i].sizes);
}

/* -------------------------------------------------------------*
 * startx = 0 means at present x 				*
 * starty = 0 means at present y				*
 * win = NULL means take stdscr 				*
 * -------------------------------------------------------------*/

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
