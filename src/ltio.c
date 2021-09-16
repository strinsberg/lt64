#include "ltconst.h"
#include "ltrun.h"
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

void display_range(WORD* mem, ADDRESS start, ADDRESS end, bool debug) {
  if (debug && end - 8 >= start) {
    start = end - 8;
    fprintf(stderr, "... ");
  }

  for (ADDRESS i = start; i < end; i++) {
    if (debug)
      fprintf(stderr, "%hx(%hd) ", mem[i], mem[i]);
    else
      printf("%04hx ", mem[i]);
  }

  if (debug)
    fprintf(stderr, "->\n");
  else
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

    if (ch == '\n') {
      if (first) {
        two_chars = 0;
      } else {
        two_chars &= 0xff;
      }
      mem[atemp] = two_chars;
      mem[atemp + 1] = 0;
      return;

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
  mem[atemp + 1] = 0;
}

// this is formated this way to keep it from taking up 300 lines
void display_op_name(OP_CODE op, FILE* stream) {
  switch (op) {
    case HALT: fprintf(stream, "HALT"); break;
    case PUSH: fprintf(stream, "PUSH"); break;
    case POP: fprintf(stream, "POP"); break;
    case LOAD: fprintf(stream, "LOAD"); break;
    case STORE: fprintf(stream, "STORE"); break;
    case FST: fprintf(stream, "FST"); break;
    case SEC: fprintf(stream, "SEC"); break;
    case NTH: fprintf(stream, "NTH"); break;
    case SWAP: fprintf(stream, "SWAP"); break;
    case ROT: fprintf(stream, "ROT"); break;
    case RPUSH: fprintf(stream, "RPUSH"); break;
    case RPOP: fprintf(stream, "RPOP"); break;
    case RGRAB: fprintf(stream, "RGRAB"); break;
    case DPUSH: fprintf(stream, "DPUSH"); break;
    case DPOP: fprintf(stream, "DPOP"); break;
    case DLOAD: fprintf(stream, "DLOAD"); break;
    case DSTORE: fprintf(stream, "DSTORE"); break;
    case DFST: fprintf(stream, "DFST"); break;
    case DSEC: fprintf(stream, "DSEC"); break;
    case DNTH: fprintf(stream, "DNTH"); break;
    case DSWAP: fprintf(stream, "DSWAP"); break;
    case DROT: fprintf(stream, "DROT"); break;
    case DRPUSH: fprintf(stream, "DRPUSH"); break;
    case DRPOP: fprintf(stream, "DRPOP"); break;
    case DRGRAB: fprintf(stream, "DRGRAB"); break;
    case ADD: fprintf(stream, "ADD"); break;
    case SUB: fprintf(stream, "SUB"); break;
    case MULT: fprintf(stream, "MULT"); break;
    case DIV: fprintf(stream, "DIV"); break;
    case MOD: fprintf(stream, "MOD"); break;
    case EQ: fprintf(stream, "EQ"); break;
    case LT: fprintf(stream, "LT"); break;
    case GT: fprintf(stream, "GT"); break;
    case MULTU: fprintf(stream, "MULTU"); break;
    case DIVU: fprintf(stream, "DIVU"); break;
    case MODU: fprintf(stream, "MODU"); break;
    case LTU: fprintf(stream, "LTU"); break;
    case GTU: fprintf(stream, "GTU"); break;
    case SL: fprintf(stream, "SL"); break;
    case SR: fprintf(stream, "SR"); break;
    case AND: fprintf(stream, "AND"); break;
    case OR: fprintf(stream, "OR"); break;
    case NOT: fprintf(stream, "NOT"); break;
    case DADD: fprintf(stream, "DADD"); break;
    case DSUB: fprintf(stream, "DSUB"); break;
    case DMULT: fprintf(stream, "DMULT"); break;
    case DDIV: fprintf(stream, "DDIV"); break;
    case DMOD: fprintf(stream, "DMOD"); break;
    case DEQ: fprintf(stream, "DEQ"); break;
    case DLT: fprintf(stream, "DLT"); break;
    case DGT: fprintf(stream, "DGT"); break;
    case DMULTU_unused: fprintf(stream, "DMULTU_unused"); break;
    case DDIVU: fprintf(stream, "DDIVU"); break;
    case DMODU: fprintf(stream, "DMODU"); break;
    case DLTU: fprintf(stream, "DLTU"); break;
    case DGTU: fprintf(stream, "DGTU"); break;
    case DSL: fprintf(stream, "DSL"); break;
    case DSR: fprintf(stream, "DSR"); break;
    case DAND: fprintf(stream, "DAND"); break;
    case DOR: fprintf(stream, "DOR"); break;
    case DNOT: fprintf(stream, "DNOT"); break;
    case JUMP: fprintf(stream, "JUMP"); break;
    case BRANCH: fprintf(stream, "BRANCH"); break;
    case CALL: fprintf(stream, "CALL"); break;
    case RET: fprintf(stream, "RET"); break;
    case DSP: fprintf(stream, "DSP"); break;
    case PC: fprintf(stream, "PC"); break;
    case BFP: fprintf(stream, "BFP"); break;
    case FMP: fprintf(stream, "FMP"); break;
    case WPRN: fprintf(stream, "WPRN"); break;
    case DPRN: fprintf(stream, "DPRN"); break;
    case WPRNU: fprintf(stream, "WPRNU"); break;
    case DPRNU: fprintf(stream, "DPRNU"); break;
    case FPRN: fprintf(stream, "FPRN"); break;
    case FPRNSC: fprintf(stream, "FPRNSC"); break;
    case PRNCH: fprintf(stream, "PRNCH"); break;
    case PRN: fprintf(stream, "PRN"); break;
    case PRNLN: fprintf(stream, "PRNLN"); break;
    case PRNSP_unused: fprintf(stream, "PRNSP_unused"); break;
    case PRNMEM: fprintf(stream, "PRNMEM"); break;
    case READCH: fprintf(stream, "READCH"); break;
    case READ_unused: fprintf(stream, "READ_unused"); break;
    case READLN: fprintf(stream, "READLN"); break;
    case READSP_unused: fprintf(stream, "READSP_unused"); break;
    case HIGH: fprintf(stream, "HIGH"); break;
    case LOW: fprintf(stream, "LOW"); break;
    case UNPACK: fprintf(stream, "UNPACK"); break;
    case PACK: fprintf(stream, "PACK"); break;
    case MEMCOPY: fprintf(stream, "MEMCOPY"); break;
    case STRCOPY: fprintf(stream, "STRCOPY"); break;
    case FMULT: fprintf(stream, "FMULT"); break;
    case FDIV: fprintf(stream, "FDIV"); break;
    case FMULTSC: fprintf(stream, "FMULTSC"); break;
    case FDIVSC: fprintf(stream, "FDIVSC"); break;
    case PRNPK: fprintf(stream, "PRNPK"); break;
    default: fprintf(stream, "UNKNOWN=%hx (%hd)", op, op); break;
  }
}

size_t debug_info_display(WORD* data_stack, WORD* return_stack, ADDRESS dsp,
                        ADDRESS rsp, ADDRESS pc, WORD op, size_t skip) {
  // print stacks and pointers
  fprintf(stderr, "Dstack: ");
  display_range(data_stack, 0x0001, dsp + 1, DEBUGGING);
  fprintf(stderr, "Rstack: ");
  display_range(return_stack, 0x0001, rsp + 1, DEBUGGING);
  fprintf(stderr, "PC: %hx (%hu), OP: ", pc, pc);
  display_op_name(op, stderr);
  fprintf(stderr, "\n\n");

  // deal with step
  if (skip != 0) {
    return skip - 1;
  } else {
    char buffer[10];
    int size = 10;

    fprintf(stderr, "*** Enter Step: ");
    if ( fgets(buffer, size, stdin) != NULL ) {
      return atoi(buffer);
    } else {
      return 0;
    }
  }
}
