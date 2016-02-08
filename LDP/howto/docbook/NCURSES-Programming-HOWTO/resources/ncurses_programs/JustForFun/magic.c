#include <curses.h>
#include <stdlib.h>

#define STARTX 9
#define STARTY 3
#define WIDTH  6
#define HEIGHT 4

#define TRACE_VALUE TRACE_MAXIMUM 

void board(	WINDOW *win, int starty, int startx, int lines, int cols, 
		int tile_width, int tile_height);
void magic(int **, int);
void print(int **, int);
void magic_board(int **a,int n);

int main(int argc, char *argv[])
{	
	
	int **a,n,i;

	if(argc != 2)
	{	printf("Usage: %s <magic sqaure order>\n", argv[0]);
		exit(0);
	}
	n = atoi(argv[1]);
	if(n % 2 == 0)
	{	printf("Sorry !!! I don't know how to create magic square of even order\n");
		printf("The order should be an odd number\n");
		exit(0);
	}
	a = (int **) malloc(n * sizeof(int*));
	for(i = 0;i < n;++i)
		a[i] = (int *)malloc(n * sizeof(int));

	magic(a,n);
	
	initscr();
	curs_set(0);
	noecho();
	magic_board(a,n);
	getch();
	endwin();

	return;
}

void magic(int **a, int n)
{	
	int i,j,k;
	int row,col;
	for(i = 0;i < n;++i)
		for(j = 0;j < n;++j)
			a[i][j] = -1;
	row = 0;
	col = n / 2;

	k = 1;
	a[row][col] = k;
	
	while(k != n * n)
	{	
		if(row == 0 && col != n - 1)
		{	row = n - 1;
			col ++;
			a[row][col] = ++k;
		}
		else if(row != 0 && col != n - 1)
		{	if(a[row - 1][col + 1] == -1)
			{	row --;
				col ++;	
				a[row][col] = ++k;
			}
			else
			{	
				row ++;
				a[row][col] = ++k;
			}
		}
		else if(row != 0 && col == n - 1)
		{	
			row --;
			col = 0;
			a[row][col] = ++k;
		}
		else if(row == 0 && col == n - 1)
		{	row ++;
			a[row][col] = ++k;	
		}
			
	}
	return;
}

void print(int **a,int n)
{	int i,j;
	int x,y;
	x = STARTX;
	y = STARTY;
	mvprintw(1,30,"MAGIC SQUARE");
	for(i = 0;i < n;++i)
	{	for(j = 0;j < n;++j)
		{	mvprintw(y,x,"%d",a[i][j]);
			if(n > 9)
				x += 4;
			else
				x += 6;
		}
		x = STARTX;
		if(n > 7)
			y += 2;
		else
			y += 3;
	}
	refresh();
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

void magic_board(int **a,int n)
{	int i,j, deltax, deltay;
	int startx, starty;

	starty = (LINES - n * HEIGHT) / 2;
	startx = (COLS  - n * WIDTH) / 2;
	board(stdscr, starty, startx, n, n, WIDTH, HEIGHT);
	deltay = HEIGHT / 2;
	deltax = WIDTH  / 2;
	for(i = 0;i < n; ++i)
		for(j = 0; j < n; ++j)
			mvprintw(starty + j * HEIGHT + deltay,
				 startx + i * WIDTH  + deltax,
				 "%d", a[i][j]);
}
