#ifndef LT_64_IO_H
#define LT_64_IO_H

#include "ltconst.h"

size_t read_program(WORD* mem, const char* filename);
void display_mem_range(WORD* mem, ADDRESS start, ADDRESS end);

#endif
