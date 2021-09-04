#include "ltconst.h"
#include "stdlib.h"
#include "stdio.h"

size_t read_program(WORD* mem, const char* filename) {
  // Open file
  FILE* fptr = fopen(filename, "rb");
  if (fptr == NULL) {
    fprintf(stderr, "Error: Input file could not be open: %s\n", filename);
    return 0;
  }

  // Find program size
  fseek(fptr, 0, SEEK_END);
  size_t length = (size_t) ftell(fptr);
  if (length > (size_t) END_MEMORY) {
    fprintf(stderr, "Error: Program will not fit in memory\n");
    return 0;
  }
  rewind(fptr);

  // Read the bytes of the program into memory
  fread(mem, length, 1, fptr);
  if (ferror(fptr)) {
    fprintf(stderr, "Error: Input file was not read\n");
    return 0;
  }
  fclose(fptr);

  // Give back the number of words in the program
  return length / sizeof(WORD);
}

void display_range(WORD* mem, ADDRESS start, ADDRESS end) {
  fprintf(stderr, "%hx, %hx\n", start, end);
  for (ADDRESS i = start; i < end; i++) {
    printf("%04hx ", mem[i]);
  }
  printf("\n");
}
