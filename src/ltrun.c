#include "ltrun.h"
#include "ltconst.h"
#include "ltio.h"
#include "stdio.h"
#include "stdbool.h"

size_t execute(WORD* memory, size_t length, WORD* data_stack, WORD* return_stack) {
  ADDRESS dsp, rsp, pc;
  dsp = 0;
  rsp = 0;
  pc = 0;
  
  bool run = true;
  while (run) {

    switch (memory[pc]) {
      case HALT:
        run = false;
        break;
      case PUSH:
        data_stack[dsp++] = memory[++pc];
        break;

      /// BAD OP CODE ///
      default:
        fprintf(stderr, "Error: Unknown OP code: 0x%hx\n", memory[pc]);
        exit(EXIT_OP);
    }
    pc++;
  }

  // Test output
  if (TESTING) {
    display_range(data_stack, 0x0000, dsp);
  }

  return EXIT_SUCCESS;
}
