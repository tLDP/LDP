#include <ncurses.h>

int main(int argc, char *argv[])
{ 
    int ch, prev;
    FILE *fp;
    int goto_prev = FALSE, y, x;

    if(argc != 2)
    {   printf("Usage: %s <a c file name>\n", argv[0]);
        exit(1);
    }
    fp = fopen(argv[1], "r");
    if(fp == NULL)
    {   perror("Cannot open input file");
        exit(1);
    }

    initscr();                      /* Start curses mode            */

    prev = EOF;
    while((ch = fgetc(fp)) != EOF)
    {   if(prev == '/' && ch == '*')    /* If it is / and * then olny
                                         * switch bold on */    
        {   attron(A_BOLD);
            goto_prev = TRUE;       /* Go to previous char / and
                                     * print it in BOLD */
        }
        if(goto_prev == TRUE)
        {   getyx(stdscr, y, x);
            move(y, x - 1);
            printw("%c%c", '/', ch); /* The actual printing is done
                                      * here */
            ch = 'a';                /* 'a' is just a dummy
                                      * character to prevent */
                                     // "/*/" comments.
            goto_prev = FALSE;      /* Set it to FALSE or every 
                                     * thing from here will be / */
        } else
            printw("%c", ch);
        refresh();
        if(prev == '*' && ch == '/')
                attroff(A_BOLD);        /* Switch it off once we got *
                                           and then / */
        prev = ch;
    }
    getch();
    endwin();                       /* End curses mode                */
    return 0;
}
