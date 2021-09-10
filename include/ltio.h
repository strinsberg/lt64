#ifndef LT_64_IO_H
#define LT_64_IO_H

#include "ltconst.h"
#include "stddef.h"

size_t read_program(WORD* mem, const char* filename);
void display_range(WORD* mem, ADDRESS start, ADDRESS end, bool debug);
void print_string(WORD* mem, ADDRESS start, ADDRESS max);
void read_string(WORD* mem, ADDRESS start, ADDRESS max);

#endif
