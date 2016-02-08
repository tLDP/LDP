# Makefile for JustForFun Files

# A few variables

CC=gcc
LIBS=-lform -lncurses

SRC_DIR=.
EXE_DIR=../demo/exe

EXES = \
	${EXE_DIR}/form_attrib\
	${EXE_DIR}/form_options\
	${EXE_DIR}/form_simple\
	${EXE_DIR}/form_win \

${EXE_DIR}/%: %.o
	${CC} -o $@ $< ${LIBS}

%.o: ${SRC_DIR}/%.c
	${CC} -o $@ -c $<

all:    ${EXES}


clean:
	@rm -f ${EXES}
