#include "ltconst.h"
#include "stdlib.h"
#include "stdio.h"
#include "stdbool.h"

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

void print_string(WORD* mem, ADDRESS start, ADDRESS max) {
  ADDRESS atemp = start;
  while (atemp < max) {
    WORD chars = mem[atemp];
    WORD low = chars & 0xff;
    WORD high = chars >> BYTE_SIZE;

    if (!low) break;
    printf("%c", low);

    if (!high) break;
    printf("%c", high);

    atemp++;
  }
}

void read_string(WORD* mem, ADDRESS start, ADDRESS max) {
  ADDRESS atemp = start;
  bool first = true;
  WORDU two_chars = 0;

  while (atemp < max - 1) {
    char ch;
    scanf("%c", &ch);
    fprintf(stderr, "%c", ch);

    if (ch == '\n') {
      if (first) {
        two_chars = 0;
      } else {
        two_chars &= 0xff;
      }
      mem[atemp] = two_chars;
      mem[atemp + 1] = 0;
      break;

    } else {
      if (first) {
        first = false;
        two_chars = ch & 0xff;
      } else {
        first = true;
        two_chars |= (ch << BYTE_SIZE);
        mem[atemp++] = two_chars;
      }
    }
  }
}

