/********
>>>Boffuer loading and reading<<<
--Init--
buffer is a constant
open the file
read BUFSIZE bytes into the buffer
close the file

--Loop--
--Buffer scanning and printing--
perform the buffer scanning until the buffer runs
  out of data (newline data)

--File--
open the file

--Seek calculation--
calculate the amount of unused buffer remaining
add BUFSIZE to the point of the file
subtract unused buffer space (a positive integer)
  from the point of the file

--Reading--
read BUFSIZE bytes into the buffer
close the file

--Cleanup--
bufbase reset to the buffer address


>>>Buffer scanning and printing<<<

--Init--
buffer is constant
bufbase reset to the buffer address

--Loop--
--Scan--
bufpt1 pointed to the first '/n' by using bufbase as
  the base address, then incremented past it.
bufpt2 pointed to the second '/n' by using bufpt1 as
  the base address.

--Output--
print out from bufpt1 to bufpt2
print out from bufbase to bufpt1-1

--Increment--
bufbase pointed to the bufpt2 and then incremented past the '/n'

********/


#include <stdio.h>
#include <stdarg.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <error.h>
#include <unistd.h>
#include <iostream.h>
#include <string.h>
#include <errno.h>

#define BUFSIZE 1000

main (int argc, char *argv[])
{
    char buffer[BUFSIZE];
    int infd, bytesread=1;
    size_t stringlength;
    char *bufpt1, *bufpt2, *bufbase, *printstring;
    off_t fileseeker;


    if (argc == 1)
    {
        fprintf(stderr, "\nError: No file specification\n");
        exit(-1);
    }

    infd = open(argv[1], O_RDONLY);
    if (infd == -1)
    {
        perror(strerror(errno));
        exit(-1);
    }
    bytesread = read(infd, buffer, BUFSIZE);
    close(infd);
    cout << "Diag: Done reading the first chunk of the file.\n";
    fileseeker = 0;
    bufbase = buffer;

    do
    {
        do
        {
            bufpt1 = strchr(bufbase, '\n');
            if (bufpt1 == NULL)
            {
		//printf("Diag: bufpt1=%u because no newline was found.", bufpt1);
                break;
            }
            bufpt1++;
            bufpt2 = strchr(bufpt1, '\n');

            stringlength = bufpt2 - bufpt1 + 1;
            printstring = new char [stringlength+1];
            snprintf(printstring, stringlength+1, "%s", bufpt1);
            printstring[stringlength-1] = '\0';
            fprintf(stdout, "%s", printstring);
            delete printstring;

            stringlength = bufpt1 - bufbase;
            printstring = new char [stringlength+1];
            snprintf(printstring, stringlength+1, "%s", bufbase);
            fprintf(stdout, "        %s", printstring);
            delete printstring;

            //printf("Diag: bufbase = %u\n", bufbase);
            bufbase = bufpt2 + 1;
            //printf("Diag: bufbase after increment = %u\n", bufbase);
        } while (bufbase >= buffer + BUFSIZE);

        /* point to the last used character */
        bufbase--;

        infd = open(argv[1], O_RDONLY);
        if (infd == -1)
        {
            perror(strerror(errno));
            exit(-1);
        }
//        printf("Diag: fileseeker=%d bufbase=%u buffer=%u\n", fileseeker, bufbase, buffer);
        fileseeker += BUFSIZE;
        fileseeker -= buffer + BUFSIZE - 1 - bufbase;
//        printf("Diag: fileseeker=%d bufbase=%u buffer=%u\n", fileseeker, bufbase, buffer);
        fileseeker = lseek(infd, fileseeker, SEEK_SET);
        //printf("Diag: fileseeker=%d bufbase=%u buffer=%u\n", fileseeker, bufbase, buffer);
        bytesread = read(infd, buffer, BUFSIZE);
        close(infd);
        bufbase = buffer;

    } while(bytesread != 0);

    exit(0);
}
