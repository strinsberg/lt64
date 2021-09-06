#include "ltrun.h"
#include "ltconst.h"
#include "ltio.h"
#include "ltmem.h"
#include "stdio.h"
#include "stdbool.h"
#include "string.h"

size_t execute(WORD* memory, size_t length, WORD* data_stack, WORD* return_stack) {
  ADDRESS dsp, rsp, pc, bfp;
  dsp = 0;
  rsp = 0;
  pc = 0;
  bfp = length + BUFFER_SIZE;

  ADDRESS atemp;
  WORD temp;
  WORDU utemp;
  DWORD dtemp;
  DWORDU udtemp;
  
  bool run = true;
  while (run) {

    switch (memory[pc] & 0xff) {
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
        atemp = data_stack[dsp--];
        data_stack[++dsp] = memory[END_MEMORY - atemp + 1];
        data_stack[++dsp] = memory[END_MEMORY - atemp];
        break;
      case DSTORE:
        atemp = data_stack[dsp--];
        memory[END_MEMORY - atemp] = data_stack[dsp];
        memory[END_MEMORY - atemp + 1] = data_stack[dsp-1];
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
        atemp = data_stack[dsp--] * 2;
        data_stack[dsp+1] = data_stack[dsp - atemp - 1];
        data_stack[dsp+2] = data_stack[dsp - atemp];
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

      /// Word Arithmetic ///
      case ADD:
        data_stack[dsp-1] = data_stack[dsp-1] + data_stack[dsp];
        dsp--;
        break;
      case SUB:
        data_stack[dsp-1] = data_stack[dsp-1] - data_stack[dsp];
        dsp--;
        break;
      case MULT:
        data_stack[dsp-1] = data_stack[dsp-1] * data_stack[dsp];
        dsp--;
        break;
      case DIV:
        data_stack[dsp-1] = data_stack[dsp-1] / data_stack[dsp];
        dsp--;
        break;
      case MOD:
        data_stack[dsp-1] = data_stack[dsp-1] % data_stack[dsp];
        dsp--;
        break;

      /// Signed Comparisson ///
      case EQ:
        data_stack[dsp-1] = data_stack[dsp-1] == data_stack[dsp];
        dsp--;
        break;
      case LT:
        data_stack[dsp-1] = data_stack[dsp-1] < data_stack[dsp];
        dsp--;
        break;
      case GT:
        data_stack[dsp-1] = data_stack[dsp-1] > data_stack[dsp];
        dsp--;
        break;

      /// Unsigned Artihmetic and Comparisson ///
      case MULTU:
        {
          // large signed numbers cast to unsigned dword as 0xffff____
          // so we have to zero those bits before the calculation 
          DWORDU a = (DWORDU)data_stack[dsp-1] & 0xffff;
          DWORDU b = (DWORDU)data_stack[dsp] & 0xffff;
          DWORDU res = a * b;
          data_stack[dsp-1] = res >> 16; 
          data_stack[dsp] = res;
        }
        break;
      case DIVU:
        data_stack[dsp-1] = (WORDU)data_stack[dsp-1] / (WORDU)data_stack[dsp];
        dsp--;
        break;
      case MODU:
        data_stack[dsp-1] = (WORDU)data_stack[dsp-1] % (WORDU)data_stack[dsp];
        dsp--;
        break;
      case LTU:
        data_stack[dsp-1] = (WORDU)data_stack[dsp-1] < (WORDU)data_stack[dsp];
        dsp--;
        break;
      case GTU:
        data_stack[dsp-1] = (WORDU)data_stack[dsp-1] > (WORDU)data_stack[dsp];
        dsp--;
        break;

      /// Double Arithmetic and Comparisson ///
      case DADD:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     + get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DSUB:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     - get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DMULT:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     * get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DDIV:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     / get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DMOD:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     % get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DEQ:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     == get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DLT:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     < get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DGT:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     > get_dword(data_stack, dsp-1));
        dsp-=2;
        break;

      /// Unsigned Double Arithmetic and Comparisson ///
      case DDIVU:
        set_dword(data_stack, dsp-3, (DWORDU)get_dword(data_stack, dsp-3)
                                     / (DWORDU)get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DMODU:
        set_dword(data_stack, dsp-3, (DWORDU)get_dword(data_stack, dsp-3)
                                     % (DWORDU)get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DLTU:
        set_dword(data_stack, dsp-3, (DWORDU)get_dword(data_stack, dsp-3)
                                     < (DWORDU)get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DGTU:
        set_dword(data_stack, dsp-3, (DWORDU)get_dword(data_stack, dsp-3)
                                     > (DWORDU)get_dword(data_stack, dsp-1));
        dsp-=2;
        break;

      /// Bitwise words ///
      case SL:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          data_stack[dsp] = data_stack[dsp] << temp;
        } else {
          data_stack[dsp-1] = data_stack[dsp-1] << data_stack[dsp];
          dsp--;
        }
        break;
      case SR:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          data_stack[dsp] = data_stack[dsp] >> temp;
        } else {
          data_stack[dsp-1] = data_stack[dsp-1] >> data_stack[dsp];
          dsp--;
        }
        break;
      case AND:
        data_stack[dsp-1] = data_stack[dsp-1] & data_stack[dsp];
        dsp--;
        break;
      case OR:
        data_stack[dsp-1] = data_stack[dsp-1] | data_stack[dsp];
        dsp--;
        break;
      case NOT:
        data_stack[dsp] = ~data_stack[dsp];
        break;

      /// Bitwise double words ///
      case DSL:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          set_dword(data_stack, dsp-1, get_dword(data_stack, dsp-1) << temp);
        } else {
          set_dword(data_stack, dsp-2, get_dword(data_stack, dsp-2)
                                       << data_stack[dsp]);
          dsp--;
        }
        break;
      case DSR:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          set_dword(data_stack, dsp-1, get_dword(data_stack, dsp-1) >> temp);
        } else {
          set_dword(data_stack, dsp-2, get_dword(data_stack, dsp-2)
                                       >> data_stack[dsp]);
          dsp--;
        }
        break;
      case DAND:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     & get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DOR:
        set_dword(data_stack, dsp-3, get_dword(data_stack, dsp-3)
                                     | get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case DNOT:
        set_dword(data_stack, dsp-1, ~get_dword(data_stack, dsp-1));
        break;

      /// Movement ///
      case JUMP:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          pc += temp;
        } else {
          pc = data_stack[dsp--];
        }
        continue;
      case BRANCH:
        temp = (memory[pc] >> BYTE_SIZE);
        if (data_stack[dsp--]) {
          if (temp) {
            pc += temp;
          } else {
            pc = data_stack[dsp--];
          }
          continue;
        }
        if (!temp) dsp--;
        break;
      case CALL:
        return_stack[++rsp] = pc + 1;
        pc = data_stack[dsp--];
        continue;
      case RET:
        pc = return_stack[rsp--];
        continue;
      case DSP:
        data_stack[dsp+1] = dsp + (memory[pc] >> BYTE_SIZE);
        dsp++;
        break;
      case PC:
        data_stack[++dsp] = pc + (memory[pc] >> BYTE_SIZE);
        break;
      case BFP:
        data_stack[++dsp] = bfp - (memory[pc] >> BYTE_SIZE);
        break;

      /// Number Printing ///
      case WPRN:
        printf("%hd", data_stack[dsp--]);
        break;
      case DPRN:
        printf("%d", get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case WPRNU:
        printf("%hu", data_stack[dsp--]);
        break;
      case DPRNU:
        printf("%u", get_dword(data_stack, dsp-1));
        dsp-=2;
        break;
      case FPRN:
        printf("%.3lf", (double)get_dword(data_stack, dsp-1)
                        / SCALES[ DEFAULT_SCALE ]);
        dsp-=2;
        break;
      case FPRNSC:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp && temp < SCALE_MAX) {
          dtemp = SCALES[temp];
        } else {
          dtemp = SCALES[ DEFAULT_SCALE ];
          temp = DEFAULT_SCALE;
        }
        printf("%.*lf", temp, (double)get_dword(data_stack, dsp-1) / dtemp);
        dsp-=2;
        break;

      /// Char and String printing ///
      case PRNCH:
        printf("%c", data_stack[dsp--] & 0xff);
        break;
      case PRN:
        // Print from bfp to first null or buffer end
        print_string(memory, bfp, BUFFER_SIZE);
        break;
      case PRNLN:
        // Print from bfp to first null or buffer end with a newline
        print_string(memory, bfp, BUFFER_SIZE);
        printf("\n");
        break;
      case PRNSP:
        // Print from top of stack to first null and remove them
        utemp = print_string(data_stack, dsp, dsp);
        dsp -= utemp;
        break;
      case PRNMEM:
        // Print from memory offset to first null
        atemp = data_stack[dsp--];
        print_string(memory, END_MEMORY - atemp, END_MEMORY - length);
        break;

      /// Reading ///
      case WREAD:
        scanf("%hd", &temp);
        data_stack[++dsp] = temp;
        break;
      case DREAD:
        scanf("%d", &dtemp);
        set_dword(data_stack, dsp + 1, dtemp);
        dsp+=2;
        break;
      case FREAD:
        {
          double x;
          scanf("%lf", &x);
          set_dword(data_stack, dsp + 1, (DWORD)(x * SCALES[ DEFAULT_SCALE ]));
          dsp+=2;
        }
        break;
      case FREADSC:
        {
          temp = (memory[pc] >> BYTE_SIZE);
          if (temp && temp < SCALE_MAX) {
            dtemp = SCALES[temp];
          } else {
            dtemp = SCALES[ DEFAULT_SCALE ];
          }
          double x;
          scanf("%lf", &x);
          set_dword(data_stack, dsp + 1, (DWORD)(x * dtemp));
          dsp+=2;
        }
        break;
      case READCH:
        scanf("%c", &temp);
        data_stack[++dsp] = temp & 0xff;
        break;
      case READLN:
        read_string(memory, bfp, BUFFER_SIZE);
        break;

      /// Buffer and Chars ///
      case BFSTORE:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          memory[bfp - temp + 1] = data_stack[dsp--];
        } else {
          atemp = data_stack[dsp--];
          memory[bfp - atemp] = data_stack[dsp--];
        }
        break;
      case BFLOAD:
        temp = (memory[pc] >> BYTE_SIZE);
        if (temp) {
          data_stack[++dsp] = memory[bfp - temp + 1];
        } else {
          atemp = data_stack[dsp];
          data_stack[dsp] = memory[bfp - atemp];
        }
        break;
      case HIGH:
        data_stack[dsp+1] = (data_stack[dsp] >> BYTE_SIZE) & 0xff;
        dsp++;
        break;
      case LOW:
        data_stack[dsp+1] = data_stack[dsp] & 0xff;
        dsp++;
        break;
      case UNPACK:
        temp = data_stack[dsp];
        data_stack[++dsp] =  (temp >> BYTE_SIZE) & 0xff;
        data_stack[++dsp] = temp & 0xff;
        break;
      case PACK:
        temp = data_stack[dsp--];
        data_stack[dsp] = temp | (data_stack[dsp] << BYTE_SIZE);
        break;

      /// Memory copying ///
      case MEMCOPY:
        exec_memcopy(memory, data_stack, bfp, &dsp,
                     data_stack[dsp--], memory[pc] >> BYTE_SIZE);
        break;
      case STRCOPY:
        exec_strcopy(memory, data_stack, bfp, &dsp, memory[pc] >> BYTE_SIZE);
        break;

      /// Fixed point arithmetic ///
      // only for those operations that cannot be done by dword ops
      case FMULT:
        {
          long long inter = (long long)get_dword(data_stack, dsp-3)
                            * (long long)get_dword(data_stack, dsp-1);
          dsp-=2;
          set_dword(data_stack, dsp-1, inter / SCALES[ DEFAULT_SCALE ]);
        }
        break;
      case FDIV:
        {
          double inter = (double)get_dword(data_stack, dsp-3)
                         / (double)get_dword(data_stack, dsp-1);
          dsp-=2;
          set_dword(data_stack, dsp-1, inter * SCALES[ DEFAULT_SCALE ]);
        }
        break;
      case FMULTSC:
        {
          temp = (memory[pc] >> BYTE_SIZE);
          if (temp && temp < SCALE_MAX) {
            dtemp = SCALES[temp];
          } else {
            dtemp = SCALES[ DEFAULT_SCALE ];
          }
          long long inter = (long long)get_dword(data_stack, dsp-3)
                            * (long long)get_dword(data_stack, dsp-1);
          dsp-=2;
          set_dword(data_stack, dsp-1, inter / dtemp);
        }
        break;
      case FDIVSC:
        {
          temp = (memory[pc] >> BYTE_SIZE);
          if (temp && temp < SCALE_MAX) {
            dtemp = SCALES[temp];
          } else {
            dtemp = SCALES[ DEFAULT_SCALE ];
          }
          double inter = (double)get_dword(data_stack, dsp-3)
                         / (double)get_dword(data_stack, dsp-1);
          dsp-=2;
          set_dword(data_stack, dsp-1, inter * dtemp);
        }
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


void exec_memcopy(WORD* memory, WORD* data_stack,
                  ADDRESS bfp, ADDRESS* dsp,
                  WORDU size, WORD code) {
  switch (code) {
    ADDRESS start;
    case MEM_BUF:
      start = data_stack[(*dsp)--];
      memcpy(memory + (bfp - (size - 1)),
             memory + ((END_MEMORY - start) - (size - 1)),
             size * 2);
      break;
    case MEM_DS:
      start = data_stack[(*dsp)--];
      memcpy(data_stack + *dsp + 1,
             memory + ((END_MEMORY - start) - (size - 1)),
             size * 2);
      (*dsp) += size;
      break;
    case BUF_MEM:
      start = data_stack[(*dsp)--];
      memcpy(memory + ((END_MEMORY - start) - (size - 1)),
             memory + (bfp - (size - 1)),
             size * 2);
      break;
    case BUF_DS:
      memcpy(data_stack + *dsp + 1,
             memory + (bfp - (size - 1)),
             size * 2);
      (*dsp) += size;
      break;
    case DS_MEM:
      start = data_stack[(*dsp)--];
      memcpy(memory + ((END_MEMORY - start) - (size - 1)),
             data_stack + (*dsp - (size - 1)),
             size * 2);
      (*dsp) -= size;
      break;
    case DS_BUF:
      memcpy(memory + (bfp - (size - 1)),
             data_stack + (*dsp - (size - 1)),
             size * 2);
      (*dsp) -= size;
      break;
  }
}

void exec_strcopy(WORD* memory, WORD* data_stack,
                  ADDRESS bfp, ADDRESS* dsp, WORD code) {
  switch (code) {
    ADDRESS start, size;
    case MEM_BUF:
      start = data_stack[(*dsp)--];
      size = string_length(memory, END_MEMORY - start);
      memcpy(memory + (bfp - (size - 1)),
             memory + ((END_MEMORY - start) - (size - 1)),
             size * 2);
      break;
    case MEM_DS:
      start = data_stack[(*dsp)--];
      size = string_length(memory, END_MEMORY - start);
      memcpy(data_stack + *dsp + 1,
             memory + ((END_MEMORY - start) - (size - 1)),
             size * 2);
      (*dsp) += size;
      break;
    case BUF_MEM:
      start = data_stack[(*dsp)--];
      size = string_length(memory, bfp);
      memcpy(memory + ((END_MEMORY - start) - (size - 1)),
             memory + (bfp - (size - 1)),
             size * 2);
      break;
    case BUF_DS:
      size = string_length(memory, bfp);
      memcpy(data_stack + *dsp + 1,
             memory + (bfp - (size - 1)),
             size * 2);
      (*dsp) += size;
      break;
    case DS_MEM:
      start = data_stack[(*dsp)--];
      size = string_length(memory, (*dsp));
      memcpy(memory + ((END_MEMORY - start) - (size - 1)),
             data_stack + (*dsp - (size - 1)),
             size * 2);
      (*dsp) -= size;
      break;
    case DS_BUF:
      size = string_length(memory, (*dsp));
      memcpy(memory + (bfp - (size - 1)),
             data_stack + (*dsp - (size - 1)),
             size * 2);
      (*dsp) -= size;
      break;
  }
}
