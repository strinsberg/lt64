#include "stdlib.h"
#include "stdio.h"
#include "stdbool.h"
#include "string.h"

#ifdef TEST
  const char* INPUT_FILE = "test.vm";
  const bool TESTING = true;
#else
  const char* INPUT_FILE = "input.vm";
  const bool TESTING = false;
#endif

#ifdef DEBUG
  const bool DEBUGGING = true;
#else
  const bool DEBUGGING = false;
#endif
  
// NOTE new OP codes must be added at the end of the enum. The testing program
// will be broken if they are inserted in the middle.

// TODO Finish implementing all of the unsigned operations for dword and qword
// and write tests for them.
// TODO setup an assembler (can use a different langauge). Needs to keep good
// track of sp,pc,ra,fp in order to allow referencing thier values at a given
// time in execution. This should probably already be done for some things like
// labeling etc. so it should not be too much overhead. If it is not easy then
// there has to be OP codes for pushing thier values to the stack, which might
// be convinient anyway.
// TODO Implement dynamic memory if it is possible.
// TODO Bitwise operations could be added, but are annoying as they all
// require 3 versions as well. They are probably useful, but not necessary for
// now. Implement them when you can.
// TODO Add some support for floating point numbers. Can this be done just by
// converting them into a byte/int form on read/assemble and printing them? I
// know it is possible to implement fixed precision floating points where there are
// always x bits before the decimal and y bits after. This might be a good options
// as they can probably easily be represented the way I am currently.
//
// NOTE PUSH, GET, CALL, and RET are all operations that must be given arguments
// in the program because the nature of these instructions is that these values
// will never be dynamic. If you want to push a value you will need to know
// that value (if you know the address of that value it is a load now). GET you
// need to have knowledge of the expected argument layout for the procedure you're
// in. CALL you must know the label of the procedure when the program is written
// or at least assembled. For CALL and RET it is necessary to know the number
// of arguments that you will pass and return when calling or writing the
// procedure.
// All other instructions can operate on data they know nothing about so it must
// be pushed to the stack for them to get. Or like load and store you might
// know the address when writing the program or you might get one at runtime. I.e.
// passing a reference to a procedure.

// Types //
typedef unsigned char BYTE;
typedef unsigned short ADDR;

typedef unsigned char WORD;
typedef unsigned short DWORD;
typedef unsigned int QWORD;

typedef signed char SWORD;
typedef signed short SDWORD;
typedef signed int SQWORD;

// Exit codes //
const size_t EXIT_MEM = 1;
const size_t EXIT_LEN = 2;
const size_t EXIT_FILE = 3;
const size_t EXIT_SOF = 4;
const size_t EXIT_SUF = 5;
const size_t EXIT_POB = 6;
const size_t EXIT_OP = 7;
const size_t EXIT_STR = 8;

// OP codes //////////////////////////////////////////////////////////////////
enum OP{ HALT=0x00,
  PUSH, POP, GET, LOAD, STORE,  // 05
  ADD, SUB, MULT, DIV, DIVU,  // 0A
  EQ, LT, LTU, GT, GTU,  // 0F

  PUSH_D, POP_D, GET_D, LOAD_D, STORE_D,  // 14
  ADD_D, SUB_D, MULT_D, DIV_D, DIV_DU,  // 19
  EQ_D, LT_D, LT_DU, GT_D, GT_DU,  // 1E

  PUSH_Q, POP_Q, GET_Q, LOAD_Q, STORE_Q,  // 23
  ADD_Q, SUB_Q, MULT_Q, DIV_Q, DIV_QU,  // 28
  EQ_Q, LT_Q, LT_QU, GT_Q, GT_QU,  // 2D

  JUMP, JUMP_IM, BRANCH, CALL, RET,  // 32
  SP, FP, PC, RA,  // 36

  PRINT, PRINT_U, PRINT_D, PRINT_DU, PRINT_Q, PRINT_QU,  //  3C
  PRINT_CHAR, PRINT_STR,  // 3E
  READ, READ_D, READ_Q,  //  41
  READ_STR,  // 42

  SL, SR, SLD, SRD, SLQ, SRQ,  // 48
  AND, ANDD, ANDQ,  // 4B
  OR, ORD, ORQ,  // 4E
  NOT, NOTD, NOTQ,  // 51
};

// Memory ////////////////////////////////////////////////////////////////////
const ADDR P_START = 0x00;
const ADDR LAST_ADDR = 0xffff;
const BYTE WORD_SIZE = 8;
const BYTE ADDR_SIZE = 8;
const WORD META_OFF = 5;

static inline ADDR get_address(WORD* mem, ADDR addr) {
  return (mem[addr] << ADDR_SIZE) | mem[addr+1];
}

static inline void set_address(WORD* mem, ADDR at, ADDR val) {
  mem[at] = val >> ADDR_SIZE;
  mem[at+1] = (WORD)val;
}

static inline DWORD get_dword(WORD* mem, ADDR addr) {
  return (mem[addr] << WORD_SIZE) | mem[addr+1];
}

static inline void set_dword(WORD* mem, ADDR addr, DWORD data) {
  mem[addr] = data >> WORD_SIZE;
  mem[addr+1] = (WORD)data;
}

static inline QWORD get_qword(WORD* mem, ADDR addr) {
  return (mem[addr] << WORD_SIZE * 3) | (mem[addr+1] << WORD_SIZE * 2)
         | (mem[addr+2] << WORD_SIZE) | mem[addr+3];
}

static inline void set_qword(WORD* mem, ADDR addr, QWORD data) {
  mem[addr] = data >> WORD_SIZE * 3;
  mem[addr+1] = data >> WORD_SIZE * 2;
  mem[addr+2] = data >> WORD_SIZE;
  mem[addr+3] = (WORD)data;
}

// I/O ///////////////////////////////////////////////////////////////////////
size_t read_program(WORD* mem, const char* filename) {
  FILE* fptr = fopen(filename, "rb");

  fseek(fptr, 0, SEEK_END);
  size_t prog_len = (size_t) ftell(fptr);
  if (prog_len > (size_t)LAST_ADDR) {
    fprintf(stderr, "Error: Program will not fit in memory\n");
    exit(EXIT_LEN);
  }
  rewind(fptr);

  fread(mem + P_START, prog_len, 1, fptr);
  if (ferror(fptr)) {
    fprintf(stderr, "Error: Input file was not read\n");
    exit(EXIT_FILE);
  }
  fclose(fptr);

  return prog_len;
}

void display_range(WORD* mem, ADDR start, ADDR end) {
  for (size_t i = start; i < end; i++) {
    printf("%02x ", mem[i]);
  }
  printf("\n");
}

void debug_memory(WORD* mem, ADDR start, ADDR end) {
  if (DEBUGGING) {
    fprintf(stderr, "Mem Range [0x%04x, 0x%04x): ", start, end);
    for (size_t i = start; i < end; i++) {
      fprintf(stderr, "%02x ", mem[i]);
    }
    fprintf(stderr, "\n");
  }

}

// Main //////////////////////////////////////////////////////////////////////
int main() {
  // Some variables we need
  ADDR sp, bp, pc, ra, fp, prog_len;
  WORD* mem;

  // Allocate memory for the VM
  mem = (WORD*) calloc((size_t)LAST_ADDR + 1, sizeof(BYTE));
  if (mem == NULL) {
    fprintf(stderr, "Error: Could not allocate memory for the VM\n");
    exit(EXIT_MEM);
  }

  // Read the program file as bytes into memory starting at PSTART
  // TODO use an argument for the program filename
  prog_len = (ADDR)read_program(mem, INPUT_FILE);

  // Set up the address variables
  pc = P_START;
  ra = pc;
  bp = LAST_ADDR - 3;
  fp = bp;
  sp = bp;

  // To help keep track if memory in this offset is accidentaly accessed
  mem[bp] = 0xaa;
  mem[bp+1] = 0xbb;
  mem[bp+2] = 0xcc;
  mem[bp+3] = 0x00;

  // Debug info
  if (DEBUGGING) {
    fprintf(stderr, "PC: 0x%04x\n", pc);
    fprintf(stderr, "RA: 0x%04x\n", pc);
    fprintf(stderr, "BP: 0x%04x\n", bp);
    fprintf(stderr, "FP: 0x%04x\n", fp);
    fprintf(stderr, "SP: 0x%04x\n", sp);
    debug_memory(mem, pc, prog_len);

    fprintf(stderr, "\n=== Execute Program ===\n");
  }

  // Execute Program
  bool run = true;
  int i;
  unsigned int ui;
  DWORD a, b;
  QWORD c, d;

  while (run) {
    if (sp > bp) {
      fprintf(stderr, "Error: Stack Underflow: sp=0x%04x, bp=0x%04x\n", sp, bp);
      fprintf(stderr, "Stack: ");
      display_range(mem, sp, bp);
      fprintf(stderr, "\n");
      exit(EXIT_SUF);
    } else if (sp <= prog_len) {
      fprintf(stderr, "Error: Stack Overflow: sp=0x%04x, prog_end=0x%04x\n",
              sp, prog_len);
      exit(EXIT_SOF);
    } else if (pc >= prog_len) {
      fprintf(stderr,
              "Error: Program counter out of bounds: pc=0x%04x, prog_end=0x%04x\n",
              pc, prog_len);
      fprintf(stderr, "Stack: ");
      display_range(mem, sp, bp);
      fprintf(stderr, "\n");
      exit(EXIT_POB);
    }

    if (DEBUGGING) {
      fprintf(stderr, "OP: %04x, SP: %04x, PC: %04x\n", mem[pc], sp, pc);
    }

    /// OP SWITCH ///
    switch (mem[pc]) {
      case HALT:
        run = false;
        break;

      /// WORDS ///
      case PUSH:
        mem[--sp] = mem[++pc];
        break;
      case POP:
        sp++;
        break;
      case GET:
        mem[--sp] = mem[fp + META_OFF + mem[++pc]];
        break;
      case LOAD:
        a = get_address(mem, sp);
        mem[++sp] = mem[a];
        break;
      case STORE:
        a = get_address(mem, sp);
        sp+=2;
        mem[a] = mem[sp++];
        break;
      case ADD:
        mem[sp+1] = mem[sp+1] + mem[sp];
        sp++;
        break;
      case SUB:
        mem[sp+1] = mem[sp+1] - mem[sp];
        sp++;
        break;
      case MULT:
        mem[sp+1] = mem[sp+1] * mem[sp];
        sp++;
        break;
      case DIV:
        mem[sp+1] = (signed char)mem[sp+1] / (signed char)mem[sp];
        sp++;
        break;
      case DIVU:
        mem[sp+1] = mem[sp+1] / mem[sp];
        sp++;
        break;
      case EQ:
        mem[sp+1] = mem[sp+1] == mem[sp];
        sp++;
        break;
      case LT:
        mem[sp+1] = (signed char)mem[sp+1] < (signed char)mem[sp];
        sp++;
        break;
      case GT:
        mem[sp+1] = (signed char)mem[sp+1] > (signed char)mem[sp];
        sp++;
        break;
      case LTU:
        mem[sp+1] = mem[sp+1] < mem[sp];
        sp++;
        break;
      case GTU:
        mem[sp+1] = mem[sp+1] > mem[sp];
        sp++;
        break;

      /// DOUBLE WORDS ///
      case PUSH_D:
        pc++;
        mem[--sp] = mem[pc+1];
        mem[--sp] = mem[pc];
        pc++;
        break;
      case POP_D:
        sp+=2;
        break;
      case GET_D:
        pc++;
        mem[--sp] = mem[fp + META_OFF + mem[pc] + 1];
        mem[--sp] = mem[fp + META_OFF + mem[pc]];
        break;
      case LOAD_D:
        a = get_address(mem, sp);
        mem[sp+1] = mem[a+1];
        mem[sp] = mem[a];
        break;
      case STORE_D:
        a = get_address(mem, sp);
        sp+=2;
        mem[a+1] = mem[sp+1];
        mem[a] = mem[sp];
        sp+=2;
        break;
      case ADD_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, b + a);
        break;
      case SUB_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, b - a);
        break;
      case MULT_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, b * a);
        break;
      case DIV_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, (SDWORD)b / (SDWORD)a);
        break;
      case DIV_DU:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, b / a);
        break;
      case EQ_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=3;
        mem[sp] = a == b;
        break;
      case LT_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=3;
        mem[sp] = (SDWORD)b < (SDWORD)a;
        break;
      case GT_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=3;
        mem[sp] = (SDWORD)b > (SDWORD)a;
        break;
      case LT_DU:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=3;
        mem[sp] = b < a;
        break;
      case GT_DU:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=3;
        mem[sp] = b > a;
        break;

      /// QUAD WORDS ///
      case PUSH_Q:
        pc++;
        mem[--sp] = mem[pc+3];
        mem[--sp] = mem[pc+2];
        mem[--sp] = mem[pc+1];
        mem[--sp] = mem[pc];
        pc+=3;
        break;
      case POP_Q:
        sp+=4;
        break;
      case GET_Q:
        pc++;
        mem[--sp] = mem[fp + META_OFF + mem[pc] + 3];
        mem[--sp] = mem[fp + META_OFF + mem[pc] + 2];
        mem[--sp] = mem[fp + META_OFF + mem[pc] + 1];
        mem[--sp] = mem[fp + META_OFF + mem[pc]];
        break;
      case LOAD_Q:
        a = get_address(mem, sp);
        sp-=2;
        mem[sp+3] = mem[a+3];
        mem[sp+2] = mem[a+2];
        mem[sp+1] = mem[a+1];
        mem[sp] = mem[a];
        break;
      case STORE_Q:
        a = get_address(mem, sp);
        sp+=2;
        mem[a+3] = mem[sp+3];
        mem[a+2] = mem[sp+2];
        mem[a+1] = mem[sp+1];
        mem[a] = mem[sp];
        sp+=4;
        break;
      case ADD_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, d + c);
        break;
      case SUB_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, d - c);
        break;
      case MULT_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, d * c);
        break;
      case DIV_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, (SQWORD)d / (SQWORD)c);
        break;
      case DIV_QU:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, d / c);
        break;
      case EQ_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=7;
        mem[sp] = c == d;
        break;
      case LT_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=7;
        mem[sp] = (SQWORD)d < (SQWORD)c;
        break;
      case GT_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=7;
        mem[sp] = (SQWORD)d > (SQWORD)c;
        break;
      case LT_QU:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=7;
        mem[sp] = d < c;
        break;
      case GT_QU:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=7;
        mem[sp] = d > c;
        break;

      /// JUMPS ///
      case JUMP:
        pc = get_address(mem, sp);
        sp+=2;
        continue;
      case JUMP_IM:
        pc = get_address(mem, ++pc);
        continue;
      case BRANCH:
        if (mem[sp++]) {
          pc = get_address(mem, ++pc);
          continue;
        }
        pc+=2;
        break;
      case CALL:
        sp-=2;
        set_address(mem, sp, ra);
        sp-=2;
        set_address(mem, sp, fp);
        mem[--sp] = mem[++pc];
        pc++;
        ra = pc+2;
        fp = sp;
        pc = get_address(mem, pc);
        debug_memory(mem, sp, bp);
        continue;
      case RET:
        {
        a = get_address(mem, fp+1);  // saved fp
        b = get_address(mem, fp+3);  // saved ra
        ADDR frame_bottom = fp + META_OFF + mem[fp];
        ADDR ret_sp = frame_bottom - mem[pc+1];
        memcpy(mem + ret_sp, mem + sp, mem[pc+1]);
        sp = ret_sp;
        pc = ra;
        fp = a;
        ra = b;
        debug_memory(mem, sp, bp);
        continue;
        }
      case SP:
        a = sp;
        sp-=2;
        set_address(mem, sp, a);
        break;
      case FP:
        sp-=2;
        set_address(mem, sp, fp);
        break;
      case PC:
        sp-=2;
        set_address(mem, sp, pc);
        break;
      case RA:
        sp-=2;
        set_address(mem, sp, ra);
        break;

      /// Print Numbers ///
      case PRINT:
        printf("%d", (SWORD)mem[sp]);
        break;
      case PRINT_U:
        printf("%u", mem[sp]);
        break;
      case PRINT_D:
        printf("%d", (SDWORD)get_dword(mem, sp));
        break;
      case PRINT_DU:
        printf("%u", get_dword(mem, sp));
        break;
      case PRINT_Q:
        printf("%d", (SQWORD)get_qword(mem, sp));
        break;
      case PRINT_QU:
        printf("%u", get_qword(mem, sp));
        break;

      /// Print Chars and Strings ///
      case PRINT_CHAR:
        printf("%c", mem[sp]);
        break;
      case PRINT_STR:
        a = get_dword(mem, sp);
        sp += 2;
        ADDR end = a;
        while (mem[end] != 0) {
          end++;
        }
        fwrite(mem + a, sizeof(char), end - a, stdout);
        break;

      /// Read Numbers ///
      case READ:
        scanf("%d", &i);
        sp -= 1;
        mem[sp] = i;
        break;
      case READ_D:
        scanf("%d", &i);
        sp-=2;
        set_dword(mem, sp, i);
        break;
      case READ_Q:
        scanf("%d", &i);
        sp-=4;
        set_qword(mem, sp, i);
        break;

      /// Read Strings ///
      case READ_STR:
        {
          char c; 
          ADDR x = prog_len;
          while (1) {
            scanf("%c", &c);
            if (c == '\n') {
              mem[x++] = 0x00;
              sp -= x - prog_len;
              memcpy(mem + sp, mem + prog_len, (size_t)x - prog_len);
              break;
            } else if (x >= sp) {
              fprintf(stderr,
                      "Error: String read will not fit in memory: size=%u",
                      x);
              exit(EXIT_STR);
            }
            mem[x++] = c;
          }
        }
        break;

      /// SHIFTS ///
      case SL:
        break;
      case SR:
        break;
      case SLD:
        break;
      case SRD:
        break;
      case SLQ:
        break;
      case SRQ:
        break;
      
      /// LOGICAL (BITWISE) ///
      case AND:
        break;
      case ANDD:
        break;
      case ANDQ:
        break;
      case OR:
        break;
      case ORD:
        break;
      case ORQ:
        break;
      case NOT:
        break;
      case NOTD:
        break;
      case NOTQ:
        break;

      /// BAD OP CODE ///
      default:
        fprintf(stderr, "Error: Unknown OP code: 0x%02x\n", mem[pc]);
        exit(EXIT_OP);
    }
    pc++;
    debug_memory(mem, sp, bp);
  }

  if (DEBUGGING) {
    WORD res = mem[sp];
    DWORD resD = get_dword(mem, sp);
    QWORD resQ = get_qword(mem, sp);
    fprintf(stderr, "\nmem[sp] = 0x%02x (%d), 0x%04x (%d), 0x%08x (%d)\n\n",
            res, res, resD, resD, resQ, resQ);
  }

  // Print the stack to stdout so program results can be seen
  if (TESTING) {
    display_range(mem, sp, bp);
  }

  // Free the VM's memory
  free(mem);

  return 0;
}
