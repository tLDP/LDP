# Makefile for JustForFun Files

# A few variables

CC=gcc
LIBS=-lpanel -lncurses

SRC_DIR=.
EXE_DIR=../demo/exe

EXES = \
	${EXE_DIR}/panel_browse \
	${EXE_DIR}/panel_hide \
	${EXE_DIR}/panel_resize \
	${EXE_DIR}/panel_simple

${EXE_DIR}/%: %.o
	${CC} -o $@ $< ${LIBS}

%.o: ${SRC_DIR}/%.c
	${CC} -o $@ -c $<

all:    ${EXES}


clean:
	@rm -f ${EXES}
