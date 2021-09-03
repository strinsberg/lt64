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
const ADDRESS END_RETURN = 0x0777;
const ADDRESS END_STACK = 0x7777; 
const WORD WORD_SIZE = 16;

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

