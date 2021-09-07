#include "ltconst.h"
#include "stdlib.h"
#include "stdbool.h"

#ifdef TEST
  const bool TESTING = true;
#else
  const bool TESTING = false;
#endif
const char* TEST_FILE = "test.vm";

#ifdef DEBUG
  const bool DEBUGGING = true;
#else
  const bool DEBUGGING = false;
#endif

// Sizes for the various memorys
const ADDRESS END_MEMORY = 0xffff;
const ADDRESS END_RETURN = 0x1000;
const ADDRESS END_STACK = 0x1000;

const WORD WORD_SIZE = 16;
const WORD BYTE_SIZE = 8;
const WORD BUFFER_SIZE = 0x0400;

const WORD DEFAULT_SCALE = 3;
const WORDU SCALE_MAX = 10;
const DWORD SCALES[ 10 ] = {
  1, 10, 100, 1000, 10000, 100000,
  1000000, 10000000, 100000000,
  1000000000
};

// Exit codes //
const size_t EXIT_MEM = 1;
const size_t EXIT_LEN = 2;
const size_t EXIT_FILE = 3;
const size_t EXIT_SOF = 4;
const size_t EXIT_SUF = 5;
const size_t EXIT_POB = 6;
const size_t EXIT_OP = 7;
const size_t EXIT_STR = 8;
const size_t EXIT_ARGS = 9;
const size_t EXIT_RSOF = 10;
const size_t EXIT_RSUF = 11;

