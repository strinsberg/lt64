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

extern const WORDU WORD_SIZE;         // number of bytes in a word
extern const WORDU BYTE_SIZE;         // number of bits in a byte
extern const WORDU BUFFER_SIZE;       // number of words in the buffer

extern const WORDU DEFAULT_SCALE;     // index of default scale in scales
extern const WORDU SCALE_MAX;         // length of the scales array
extern const DWORDU SCALES[];         // scaling factors i.e. 10, 100 ...

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
extern const size_t EXIT_RSOF;
extern const size_t EXIT_RSUF;

#endif
