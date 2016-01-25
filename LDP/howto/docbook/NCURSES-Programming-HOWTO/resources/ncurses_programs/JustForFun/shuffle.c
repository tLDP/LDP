#include <curses.h>

#define STARTX 9
#define STARTY 3
#define WIDTH  6
#define HEIGHT 4

#define BLANK 0

typedef struct _tile {
	int x;
	int y;
}tile;

void init_board(int **board, int n, tile *blank);
void board(WINDOW *win, int starty, int startx, int lines, int cols, 
	   int tile_width, int tile_height);
void shuffle_board(int **board, int n);
void move_blank(int direction, int **s_board, int n, tile *blank);
int check_win(int **s_board, int n, tile *blank);

enum { LEFT, RIGHT, UP, DOWN };

int main(int argc, char *argv[])
{	int **s_board;
	int n, i, ch;
	tile blank;

	if(argc != 2)
	{	printf("Usage: %s <shuffle board order>\n", argv[0]);
		exit(1);
	}
	n = atoi(argv[1]);
	
	s_board = (int **)calloc(n, sizeof(int *));
	for(i = 0;i < n; ++i)
		s_board[i] = (int *)calloc(n, sizeof(int));
	init_board(s_board, n, &blank);
	initscr();
	keypad(stdscr, TRUE);
	cbreak();
	shuffle_board(s_board, n);
	while((ch = getch()) != KEY_F(1))
	{	switch(ch)
		{	case KEY_LEFT:
				move_blank(RIGHT, s_board, n, &blank);
				break;
			case KEY_RIGHT:
				move_blank(LEFT, s_board, n, &blank);
				break;
			case KEY_UP:
				move_blank(DOWN, s_board, n, &blank);
				break;
			case KEY_DOWN:
				move_blank(UP, s_board, n, &blank);
				break;
		}
		shuffle_board(s_board, n);
		if(check_win(s_board, n, &blank) == TRUE)
		{	mvprintw(24, 0, "You Win !!!\n");
			refresh();
			break;
		}
	}
	endwin();
	return 0;	
}

void move_blank(int direction, int **s_board, int n, tile *blank)
{	int temp;

	switch(direction)
	{	case LEFT:
		{	if(blank->x != 0)
			{	--blank->x;
				temp = s_board[blank->x][blank->y];
				s_board[blank->x + 1][blank->y] = temp;
				s_board[blank->x][blank->y] = BLANK;
			}
		}
		break;
		case RIGHT:
		{	if(blank->x != n - 1)
			{	++blank->x;
				temp = s_board[blank->x][blank->y];
				s_board[blank->x - 1][blank->y] = temp;
				s_board[blank->x][blank->y] = BLANK;
			}
		}
		break;
		case UP:
		{	if(blank->y != 0)
			{	--blank->y;
				temp = s_board[blank->x][blank->y];
				s_board[blank->x][blank->y + 1] = temp;
				s_board[blank->x][blank->y] = BLANK;
			}
		}
		break;
		case DOWN:
		{	if(blank->y != n - 1)
			{	++blank->y;
				temp = s_board[blank->x][blank->y];
				s_board[blank->x][blank->y - 1] = temp;
				s_board[blank->x][blank->y] = BLANK;
			}
		}
		break;			
	}
}

int check_win(int **s_board, int n, tile *blank)
{	int i, j;

	s_board[blank->x][blank->y] = n * n;
	for(i = 0;i < n; ++i)
		for(j = 0;j < n; ++j)
			if(s_board[i][j] != j * n + i + 1)
			{	s_board[blank->x][blank->y] = BLANK;
				return FALSE;
			}
	
	s_board[blank->x][blank->y] = BLANK;
	return TRUE;	
}

void init_board(int **s_board, int n, tile *blank)
{	int i, j, k;
	int *temp_board;

	temp_board = (int *)calloc(n * n, sizeof(int));
	srand(time(NULL));
	for(i = 0;i < n * n; ++i)
	{    
repeat :
		k = rand() % (n * n);
		for(j = 0;j <= i - 1; ++j)
			if (k == temp_board[j])
				goto repeat;
			else
				temp_board[i] = k;
	}
	k = 0;
	for (i = 0;i < n;++i)
		for(j = 0;j < n; ++j,++k)
		{	if(temp_board[k] == 0)
			{	blank->x = i;
				blank->y = j;
			}
			s_board[i][j] = temp_board[k];
		}
	free(temp_board);
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

void shuffle_board(int **s_board, int n)
{	int i,j, deltax, deltay;
	int startx, starty;

	starty = (LINES - n * HEIGHT) / 2;
	startx = (COLS  - n * WIDTH) / 2;
	clear();
	mvprintw(24, 0, "Press F1 to Exit");
	board(stdscr, starty, startx, n, n, WIDTH, HEIGHT);
	deltay = HEIGHT / 2;
	deltax = WIDTH  / 2;
	for(j = 0; j < n; ++j)
		for(i = 0;i < n; ++i)
			if(s_board[i][j] != BLANK)
				mvprintw(starty + j * HEIGHT + deltay,
					 startx + i * WIDTH  + deltax,
					 "%-2d", s_board[i][j]);
	refresh();
}
	

