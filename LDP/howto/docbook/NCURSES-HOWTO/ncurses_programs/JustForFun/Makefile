# Makefile for JustForFun Files

# A few variables

CC=gcc
LIBS=-lncurses

SRC_DIR=.
EXE_DIR=../demo/exe

EXES = \
	${EXE_DIR}/hanoi \
	${EXE_DIR}/life\
	${EXE_DIR}/magic \
	${EXE_DIR}/queens \
	${EXE_DIR}/shuffle \
	${EXE_DIR}/tt

${EXE_DIR}/%: %.o
	${CC} -o $@ $< ${LIBS}

%.o: ${SRC_DIR}/%.c
	${CC} -o $@ -c $<

all:    ${EXES}

clean:
	@rm -f ${EXES}
