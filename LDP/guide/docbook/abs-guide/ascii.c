/*********************************************/
/* ascii.c                                   */
/* Generate ASCII table                      */
/* To build: gcc -O2 ascii.c -o ascii-table  */
/*                                           */
/* This utterly trivial program written by   */
/* Mendel Cooper, 04/07                      */
/* I'm not proud of it, but it does the job. */
/* License: Public Domain                    */
/*********************************************/

#include &lt;stdio.h&gt;

#define MAX 255                /* FF hex       */
#define FILENAME "ASCII.txt"   /* Outfile name */

int main()
  {
  int i;
  FILE *fp;

  fp = fopen (FILENAME, "a" );

  for( i = 1; i <= MAX; i++ ) {
     fprintf( fp, "%5d  ", i );
     fputc( i, fp );
     fprintf( fp, "     " );
     if ( i % 5 == 0 )
        fprintf( fp, "\n" );
     }

     fprintf( fp, "\n" );

  return (0);
  } /* Outfile needs a bit of hand-editing for tidying up. */

/* Try rewriting this as a shell script. */
/* Not so easy, huh?                     */
