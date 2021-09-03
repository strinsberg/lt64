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

  WORD temp;
  
  bool run = true;
  while (run) {

    switch (memory[pc]) {
      case HALT:
        run = false;
        break;

      /// Stack Manipulation ///
      case PUSH:
        data_stack[++dsp] = memory[++pc];
        break;
      case POP:
        dsp--;
        break;
      case LOAD:
        data_stack[dsp] = memory[END_MEMORY - data_stack[dsp]];
        break;
      case STORE:
        memory[END_MEMORY - data_stack[dsp]] = data_stack[dsp-1];
        dsp-=2;
        break;
      case FST:
        data_stack[dsp+1] = data_stack[dsp];
        dsp++;
        break;
      case SEC:
        data_stack[dsp+1] = data_stack[dsp-1];
        dsp++;
        break;
      case NTH:
        data_stack[dsp] = data_stack[dsp - data_stack[dsp] - 1];
        break;
      case SWAP:
        temp = data_stack[dsp];
        data_stack[dsp] = data_stack[dsp-1];
        data_stack[dsp-1] = temp;
        break;
      case ROT:
        temp = data_stack[dsp-2];
        data_stack[dsp-2] = data_stack[dsp-1];
        data_stack[dsp-1] = data_stack[dsp];
        data_stack[dsp] = temp;
        break;
      case RPUSH:
        return_stack[++rsp] = data_stack[dsp--];
        break;
      case RPOP:
        data_stack[++dsp] = return_stack[rsp--];
        break;
      case RGRAB:
        data_stack[++dsp] = return_stack[rsp];
        break;

      /// Double Word Stack Manipulation ///
      case DPUSH:
        data_stack[++dsp] = memory[++pc];
        data_stack[++dsp] = memory[++pc];
        break;
      case DPOP:
        dsp-=2;
        break;
      case DLOAD:
        temp = data_stack[dsp--];
        data_stack[++dsp] = memory[END_MEMORY - temp + 1];
        data_stack[++dsp] = memory[END_MEMORY - temp];
        break;
      case DSTORE:
        temp = data_stack[dsp--];
        memory[END_MEMORY - temp] = data_stack[dsp];
        memory[END_MEMORY - temp + 1] = data_stack[dsp-1];
        dsp-=2;
        break;
      case DFST:
        data_stack[dsp+1] = data_stack[dsp-1];
        data_stack[dsp+2] = data_stack[dsp];
        dsp+=2;
        break;
      case DSEC:
        data_stack[dsp+1] = data_stack[dsp-3];
        data_stack[dsp+2] = data_stack[dsp-2];
        dsp+=2;
        break;
      case DNTH:
        temp = data_stack[dsp--] * 2;
        data_stack[dsp+1] = data_stack[dsp - temp - 1];
        data_stack[dsp+2] = data_stack[dsp - temp];
        dsp+=2;
        break;
      case DSWAP:
        temp = data_stack[dsp];
        data_stack[dsp] = data_stack[dsp-2];
        data_stack[dsp-2] = temp;

        temp = data_stack[dsp-1];
        data_stack[dsp-1] = data_stack[dsp-3];
        data_stack[dsp-3] = temp;
        break;
      case DROT:
        temp = data_stack[dsp-5];
        data_stack[dsp-5] = data_stack[dsp-3];
        data_stack[dsp-3] = data_stack[dsp-1];
        data_stack[dsp-1] = temp;

        temp = data_stack[dsp-4];
        data_stack[dsp-4] = data_stack[dsp-2];
        data_stack[dsp-2] = data_stack[dsp];
        data_stack[dsp] = temp;
        break;
      case DRPUSH:
        return_stack[++rsp] = data_stack[dsp-1];
        return_stack[++rsp] = data_stack[dsp];
        dsp-=2;
        break;
      case DRPOP:
        data_stack[++dsp] = return_stack[rsp-1];
        data_stack[++dsp] = return_stack[rsp];
        rsp-=2;
        break;
      case DRGRAB:
        data_stack[++dsp] = return_stack[rsp-1];
        data_stack[++dsp] = return_stack[rsp];
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
    display_range(data_stack, 0x0001, dsp + 1);
  }

  return EXIT_SUCCESS;
}
