#include "ltconst.h"
#include "ltio.h"
#include "ltrun.h"
#include "stdlib.h"
#include "stdio.h"

int main( int argc, char *argv[] ) {
  // VM memory pointers
  WORD* data_stack;
  WORD* return_stack;
  WORD* memory;

  // Allocate memory for the Data Stack
  data_stack = (WORD*) calloc((size_t)END_STACK + 1, sizeof(WORD));
  if (data_stack == NULL) {
    fprintf(stderr, "Error: Could not allocate the Data Stack\n");
    exit(EXIT_MEM);
  }

  // Allocate memory for the Return Stack
  return_stack = (WORD*) calloc((size_t)END_RETURN + 1, sizeof(WORD));
  if (return_stack == NULL) {
    fprintf(stderr, "Error: Could not allocate the Return Stack\n");
    exit(EXIT_MEM);
  }

  // Allocate memory for the Main Memory
  memory = (WORD*) calloc((size_t)END_MEMORY + 1, sizeof(WORD));
  if (memory == NULL) {
    fprintf(stderr, "Error: Could not allocate Main Program Memory\n");
    exit(EXIT_MEM);
  }

  // Read the program file as bytes into memory
  size_t length = 0;
  if (TESTING) {
    length = (ADDRESS)read_program(memory, TEST_FILE);
  } else if (argc >= 2) {
    length = (ADDRESS)read_program(memory, argv[1]);
  } else {
    fprintf(stderr, "Error: File name missing\n");
    fprintf(stderr, "Usage: lt64 <input file name>\n");
    exit(EXIT_ARGS);
  }

  if (!length) exit(EXIT_LEN);

  // Run program
  size_t result = execute(memory, length, data_stack, return_stack);

  // clean up
  free(memory);
  free(data_stack);
  free(return_stack);

  return result;
}
