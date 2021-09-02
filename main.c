#include "stdlib.h"
#include "stdio.h"
#include "stdbool.h"
#include "string.h"

#ifdef TEST
  const bool TESTING = true;
#else
  const bool TESTING = false;
#endif
const char* TEST_FILE = "test.vm";

#ifdef DEBUG
  const bool DEBUGGING = true;
#else
  const bool DEBUGGING = false;
#endif

// Macros //

// NOTE these rely on the memory block being named mem and the stack pointer
// being named sp. Also on the functions get/set_dword and get/set_qword and
// the typedefs for signed types SWORD SDWORD SQWORD. All of these are
// currently defined below.
#define OP_ADD +
#define OP_SUB -
#define OP_TIMES *
#define OP_DIV /
#define OP_BIT_AND &
#define OP_BIT_OR |
#define OP_EQ ==
#define OP_GT >
#define OP_LT <

// Word operations
#define BIN_WU_OP(op) \
        mem[sp+1] = mem[sp+1] op mem[sp]; \
        sp++

#define BIN_W_OP(op) \
        mem[sp+1] = (SWORD)mem[sp+1] op (SWORD)mem[sp]; \
        sp++

// DWord operations
#define BIN_D_START(a,b) \
        (a) = get_dword(mem, sp); \
        (b) = get_dword(mem, sp+2); \
        sp+=2

#define BIN_DU_OP(op, a, b) \
        BIN_D_START(a,b); \
        set_dword(mem, sp, ((b) op (a)))

#define BIN_D_OP(op, a, b) \
        BIN_D_START(a,b); \
        set_dword(mem, sp, ((SDWORD)(b) op (SDWORD)(a)))

#define BIN_DU_COMP(op, a, b) \
        BIN_D_START(a,b); \
        mem[++sp] = ((b) op (a))

#define BIN_D_COMP(op, a, b) \
        BIN_D_START(a,b); \
        mem[++sp] = ((SDWORD)(b) op (SDWORD)(a))
        
// QWord operations
#define BIN_Q_START(a,b) \
        (a) = get_qword(mem, sp); \
        (b) = get_qword(mem, sp+4); \
        sp+=4

#define BIN_QU_OP(op, a, b) \
        BIN_Q_START(a,b); \
        set_qword(mem, sp, ((b) op (a)))

#define BIN_Q_OP(op, a, b) \
        BIN_Q_START(a,b); \
        set_qword(mem, sp, ((SQWORD)(b) op (SQWORD)(a)))

#define BIN_QU_COMP(op, a, b) \
        BIN_Q_START(a,b); \
        sp+=3; \
        mem[sp] = ((b) op (a))

#define BIN_Q_COMP(op, a, b) \
        BIN_Q_START(a,b); \
        sp+=3; \
        mem[sp] = ((SQWORD)(b) op (SQWORD)(a))

// Types //
typedef unsigned char BYTE;
typedef unsigned short ADDR;

typedef unsigned char WORD;
typedef unsigned short DWORD;
typedef unsigned int QWORD;
typedef unsigned long long ULL;

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
const size_t EXIT_ARGS = 9;

// OP codes //////////////////////////////////////////////////////////////////
enum OP{ HALT=0x00,
  PUSH, POP, ARG, LOAD, STORE,  // 05
  ADD, SUB, MULT, DIV, DIVU,  // 0A
  EQ, LT, LTU, GT, GTU,  // 0F

  PUSH_D, POP_D, ARG_D, LOAD_D, STORE_D,  // 14
  ADD_D, SUB_D, MULT_D, DIV_D, DIV_DU,  // 19
  EQ_D, LT_D, LT_DU, GT_D, GT_DU,  // 1E

  PUSH_Q, POP_Q, ARG_Q, LOAD_Q, STORE_Q,  // 23
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

  PRG, BRK, BRK_ADD, BRK_DROP, // 55

  // NOTE no unsigned fixed point nums
  ADD_F, SUB_F, MULT_F, DIV_F,  // 59
  EQ_F, LT_F, GT_F,  // 5C
  PRINT_F, READ_F,  // 5E
};

// Simple Memory /////////////////////////////////////////////////////////////
const ADDR NIL = 0xffff;
const ADDR P_START = 0x00;
const ADDR LAST_ADDR = 0xffff;
const BYTE WORD_SIZE = 8;
const BYTE ADDR_SIZE = 8;
const WORD META_OFF = 5;
const DWORD SCALE_FACTOR = 1000;

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
  if (fptr == NULL) {
    fprintf(stderr, "Error: Input file could not be open: %s\n", filename);
    exit(EXIT_FILE);
  }

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
int main( int argc, char *argv[] ) {
  // Some variables we need
  ADDR sp, bp, pc, ra, fp, prog_len, brk;
  WORD* mem;

  // Allocate memory for the VM
  mem = (WORD*) calloc((size_t)LAST_ADDR + 1, sizeof(BYTE));
  if (mem == NULL) {
    fprintf(stderr, "Error: Could not allocate memory for the VM\n");
    exit(EXIT_MEM);
  }

  // Read the program file as bytes into memory starting at PSTART
  if (TESTING) {
    prog_len = (ADDR)read_program(mem, TEST_FILE);
  } else if (argc >= 2) {
    prog_len = (ADDR)read_program(mem, argv[1]);
  } else {
    fprintf(stderr, "Error: File name missing\n");
    fprintf(stderr, "Usage: lt64 <input file name>\n");
    exit(EXIT_ARGS);
  }


  // Set up the address variables
  pc = P_START;
  brk = prog_len;
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
    /// Error Checking ///
    if (pc >= prog_len) {
      fprintf(stderr,
              "Error: Program counter out of bounds: pc=0x%04x, prog_end=0x%04x\n",
              pc, prog_len);
      fprintf(stderr, "Stack: ");
      display_range(mem, sp, bp);
      fprintf(stderr, "\n");
      exit(EXIT_POB);
    } else if (sp > bp) {
      fprintf(stderr, "Error: Stack Underflow: sp=0x%04x, bp=0x%04x\n", sp, bp);
      fprintf(stderr, "Stack: ");
      display_range(mem, sp, bp);
      fprintf(stderr, "\n");
      exit(EXIT_SUF);
    } else if (sp <= prog_len || sp <= brk) {
      fprintf(stderr, "Error: Stack Overflow: sp=0x%04x, brk=0x%04x, prg=0x%04x\n",
              sp, brk, prog_len);
      exit(EXIT_SOF);
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
      case ARG:
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
        BIN_WU_OP(OP_ADD);
        break;
      case SUB:
        BIN_WU_OP(OP_SUB);
        break;
      case MULT:
        BIN_WU_OP(OP_TIMES);
        break;
      case DIV:
        BIN_W_OP(OP_DIV);
        break;
      case DIVU:
        BIN_WU_OP(OP_DIV);
        break;
      case EQ:
        BIN_WU_OP(OP_EQ);
        break;
      case LT:
        BIN_W_OP(OP_LT);
        break;
      case GT:
        BIN_W_OP(OP_GT);
        break;
      case LTU:
        BIN_WU_OP(OP_LT);
        break;
      case GTU:
        BIN_WU_OP(OP_GT);
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
      case ARG_D:
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
        BIN_DU_OP(OP_ADD, a, b);
        break;
      case SUB_D:
        BIN_DU_OP(OP_SUB, a, b);
        break;
      case MULT_D:
        BIN_DU_OP(OP_TIMES, a, b);
        break;
      case DIV_D:
        BIN_D_OP(OP_DIV, a, b);
        break;
      case DIV_DU:
        BIN_DU_OP(OP_DIV, a, b);
        break;
      case EQ_D:
        BIN_DU_COMP(OP_EQ, a, b);
        break;
      case LT_D:
        BIN_D_COMP(OP_LT, a, b);
        break;
      case GT_D:
        BIN_D_COMP(OP_GT, a, b);
        break;
      case LT_DU:
        BIN_DU_COMP(OP_LT, a, b);
        break;
      case GT_DU:
        BIN_DU_COMP(OP_GT, a, b);
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
      case ARG_Q:
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
        BIN_QU_OP(OP_ADD, c, d);
        break;
      case SUB_Q:
        BIN_QU_OP(OP_SUB, c, d);
        break;
      case MULT_Q:
        BIN_QU_OP(OP_TIMES, c, d);
        break;
      case DIV_Q:
        BIN_Q_OP(OP_DIV, c, d);
        break;
      case DIV_QU:
        BIN_QU_OP(OP_DIV, c, d);
        break;
      case EQ_Q:
        BIN_Q_COMP(OP_EQ, c, d);
        break;
      case LT_Q:
        BIN_Q_COMP(OP_LT, c, d);
        break;
      case GT_Q:
        BIN_Q_COMP(OP_GT, c, d);
        break;
      case LT_QU:
        BIN_QU_COMP(OP_LT, c, d);
        break;
      case GT_QU:
        BIN_QU_COMP(OP_GT, c, d);
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
        // Save current return address and frame pointer
        sp-=2;
        set_address(mem, sp, ra);
        sp-=2;
        set_address(mem, sp, fp);
        // get number of params (max 255)
        mem[--sp] = mem[++pc];
        pc++;
        // set new return address and frame pointer
        ra = pc+2;
        fp = sp;
        // get address of function and move pc
        pc = get_address(mem, pc);
        debug_memory(mem, sp, bp);
        continue;
      case RET:
        {
        a = get_address(mem, fp+1);  // saved fp
        b = get_address(mem, fp+3);  // saved ra
        ADDR frame_bottom = fp + META_OFF + mem[fp];  // address top of args
        ADDR ret_sp = frame_bottom - mem[pc+1];  // make room for returns
        memcpy(mem + ret_sp, mem + sp, mem[pc+1]);  // copy returns back
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
        // might be good to have a function for this or at least for the
        // first if case.
        {
          char c; 
          ADDR x = sp;

          while (1) {
            scanf("%c", &c);
            if (c == '\n') {
              mem[--x] = 0x00;

              // string is read in backwards so we reverse it
              size_t i = 0;
              while (x+i < sp-i-1) {
                c = mem[x+i];
                mem[x+i] = mem[sp-i-1];
                mem[sp-i-1] = c;
                i++;
              }

              sp = x;
              break;

            } else if (x <= brk) {
              fprintf(stderr,
                      "Error: String read will not fit in memory: size=%u\n",
                      x);
              exit(EXIT_STR);
            }
            mem[--x] = c;
          }
        }
        break;

      /// SHIFTS ///
      case SL:
        pc++;
        mem[sp] = mem[sp] << mem[pc];
        break;
      case SR:
        pc++;
        mem[sp] = mem[sp] >> mem[pc];
        break;
      case SLD:
        pc++;
        a = get_dword(mem, sp) << mem[pc];
        set_dword(mem, sp, a);
        break;
      case SRD:
        pc++;
        a = get_dword(mem, sp) >> mem[pc];
        set_dword(mem, sp, a);
        break;
      case SLQ:
        pc++;
        c = get_qword(mem, sp) << mem[pc];
        set_qword(mem, sp, c);
        break;
      case SRQ:
        pc++;
        c = get_qword(mem, sp) >> mem[pc];
        set_qword(mem, sp, c);
        break;
      
      /// LOGICAL (BITWISE) ///
      case AND:
        BIN_WU_OP(OP_BIT_AND);
        break;
      case ANDD:
        BIN_DU_OP(OP_BIT_AND, a, b);
        break;
      case ANDQ:
        BIN_QU_OP(OP_BIT_AND, c, d);
        break;
      case OR:
        BIN_WU_OP(OP_BIT_OR);
        break;
      case ORD:
        BIN_DU_OP(OP_BIT_OR, a, b);
        break;
      case ORQ:
        BIN_QU_OP(OP_BIT_OR, c, d);
        break;
      case NOT:
        mem[sp] = ~mem[sp];
        break;
      case NOTD:
        a = get_dword(mem, sp);
        set_dword(mem, sp, ~a);
        break;
      case NOTQ:
        c = get_qword(mem, sp);
        set_qword(mem, sp, ~c);
        break;

      /// Heap ///
      // Very minimal. Give words when requested and remove them when requested
      // as long as this won't go out of bounds with prog_len or sp. User is
      // responsible for how they use this memory. Not quite like dynamic
      // memory given by the os that is tracked on the heap. As this is all the
      // memory available to the programmer they will have to fully manage it
      // themselves, and don't really have to use the add and drop brk movers
      // but can just use end of program and use the memory as they want, knowing
      // that it can be overwritten by the stack if they don't move brk around.
      case PRG:
        sp-=2;
        set_address(mem, sp, prog_len);
        break;
      case BRK:
        sp-=2;
        set_address(mem, sp, brk);
        break;
      case BRK_ADD:
        a = brk;
        b = get_dword(mem, sp);  // amount to add
        if (brk + b < sp && brk + b > brk) {
          brk += b;
        } else {
          a = 0xffff;
        }
        set_address(mem, sp, a);
        break;
      case BRK_DROP:
        b = get_dword(mem, sp);  // amount to drop
        if (brk - b >= prog_len && brk - b < brk) {
          brk -= b;
          set_address(mem, sp, brk);
        } else {
          a = 0xffff;
          set_address(mem, sp, a);
        }
        break;

      /// Fixed Point ///
      case ADD_F:
        BIN_Q_OP(OP_ADD, c, d);
        break;
      case SUB_F:
        BIN_Q_OP(OP_SUB, c, d);
        break;
      case MULT_F:
        {
        ULL x = get_qword(mem, sp);
        ULL y = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, (QWORD)((y * x) / SCALE_FACTOR));
        break;
        }
      case DIV_F:
        {
        double x = (SQWORD)get_qword(mem, sp);
        double y = (SQWORD)get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, (QWORD)((y / x) * SCALE_FACTOR));
        break;
        }
      case EQ_F:
        BIN_Q_COMP(OP_EQ, c, d);
        break;
      case LT_F:
        BIN_Q_COMP(OP_LT, c, d);
        break;
      case GT_F:
        BIN_Q_COMP(OP_GT, c, d);
        break;
      case PRINT_F:
        {
        double x = (SQWORD)get_qword(mem, sp);
        printf("%.3lf",  x / SCALE_FACTOR);
        break;
        }
      case READ_F:
        {
        double x;
        scanf("%lf", &x);
        fprintf(stderr, "%lf\n", x);
        sp-=4;
        set_qword(mem, sp, (QWORD)(x * SCALE_FACTOR));
        break;
        }

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
