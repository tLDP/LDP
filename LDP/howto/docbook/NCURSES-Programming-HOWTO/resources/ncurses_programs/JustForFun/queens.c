#include <stdio.h>
#include <curses.h>

#define QUEEN_CHAR '*'

int *nqueens(int num);
int place(int current, int *position);
int print(int *positions, int num_queens);
void board(WINDOW *win, int starty, int startx, int lines, int cols, 
	   int tile_width, int tile_height);

int main(int argc, char *argv[])
{
	int num_queens, *positions, count;
	
	if(argc != 2)
	{	printf("Usage: %s <number of queens (chess board order)>\n", argv[0]);
		exit(1);
	}

	num_queens = atoi(argv[1]);
	initscr();
	cbreak();
	keypad(stdscr, TRUE);
	positions = nqueens(num_queens);
	free(positions);
	endwin();
	return 0;
}

int *nqueens(int num)
{
	int current, *position, num_solutions = 0;
	
	position = (int *) calloc(num + 1, sizeof(int));

	position[1] = 0; 
	current = 1;	/* current queen is being checked	*/
				/* position[current] is the coloumn*/
	while(current > 0){
		position[current] += 1;
		while(position[current] <= num && !place(current, position) )
			position[current] += 1;
		if(position[current] <= num){
			if(current == num)	{
				++num_solutions;
				print(position, num);
			}	
			else {
				current += 1;
				position[current] = 0;
			}
		}
		else current -= 1;		/*	backtrack		*/
	}
	printf("Total Number of Solutions : %d\n", num_solutions);
	return(position);
}

int place(int current, int *position)
{
	int i;
	if(current == 1) return(1);
	for(i = 1; i < current; ++i)
		if(position[i] == position[current]) return(0);
		else if(abs(position[i] - position[current]) ==
			abs(i - current))
			return(0);
	
	return(1);
}
		
int print(int *positions, int num_queens)
{	int count;
	int y = 2, x = 2, w = 4, h = 2;
	static int solution = 1;

	mvprintw(0, 0, "Solution No: %d", solution++);
	board(stdscr, y, x, num_queens, num_queens, w, h);
	for(count = 1; count <= num_queens; ++count)
	{	int tempy = y + (count - 1) * h + h / 2;
		int tempx = x + (positions[count] - 1) * w + w / 2;
		mvaddch(tempy, tempx, QUEEN_CHAR);
	}
	refresh();
	mvprintw(LINES - 2, 0, "Press Any Key to See next solution (F1 to Exit)");
	if(getch() == KEY_F(1))
	{	endwin();
		exit(0);
	}
	clear();
}

void board(WINDOW *win, int starty, int startx, int lines, int cols, 
	   int tile_width, int tile_height)
{	int endy, endx, i, j;
	
	endy = starty + lines * tile_height;
	endx = startx + cols  * tile_width;
	
	for(j = starty; j <= endy; j += tile_height)
		for(i = startx; i <= endx; ++i)
			mvwaddch(win, j, i, ACS_HLINE);
	for(i = startx; i <= endx; i += tile_width)
		for(j = starty; j <= endy; ++j)
			mvwaddch(win, j, i, ACS_VLINE);
	mvwaddch(win, starty, startx, ACS_ULCORNER);
	mvwaddch(win, endy, startx, ACS_LLCORNER);
	mvwaddch(win, starty, endx, ACS_URCORNER);
	mvwaddch(win, 	endy, endx, ACS_LRCORNER);
	for(j = starty + tile_height; j <= endy - tile_height; j += tile_height)
	{	mvwaddch(win, j, startx, ACS_LTEE);
		mvwaddch(win, j, endx, ACS_RTEE);	
		for(i = startx + tile_width; i <= endx - tile_width; i += tile_width)
			mvwaddch(win, j, i, ACS_PLUS);
	}
	for(i = startx + tile_width; i <= endx - tile_width; i += tile_width)
	{	mvwaddch(win, starty, i, ACS_TTEE);
		mvwaddch(win, endy, i, ACS_BTEE);
	}
	wrefresh(win);
}
