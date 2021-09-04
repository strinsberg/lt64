#ifndef LT_64_CONST_H
#define LT_64_CONST_H

#include "stdlib.h"
#include "stdbool.h"

typedef short WORD;
typedef unsigned short ADDRESS;
typedef ADDRESS WORDU;
typedef int DWORD;
typedef unsigned int DWORDU;

// Testing vars
extern const bool TESTING;
extern const char* TEST_FILE;
extern const bool DEBUGGING;

// Sizes for the various memorys
extern const ADDRESS END_MEMORY;
extern const ADDRESS END_RETURN;
extern const ADDRESS END_STACK;
extern const WORD WORD_SIZE;
extern const WORD BYTE_SIZE;
extern const WORD BUFFER_SIZE;
extern const WORD DEFAULT_SCALE;
extern const WORDU SCALE_MAX;
extern const DWORD SCALES[];

// Exit codes //
extern const size_t EXIT_MEM;
extern const size_t EXIT_LEN;
extern const size_t EXIT_FILE;
extern const size_t EXIT_SOF;
extern const size_t EXIT_SUF;
extern const size_t EXIT_POB;
extern const size_t EXIT_OP;
extern const size_t EXIT_STR;
extern const size_t EXIT_ARGS;

#endif
