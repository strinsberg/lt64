#include "stdlib.h"
#include "stdio.h"
#include "stdbool.h"

// TODO Change things so the stack starts at the top and grows down
// it will make it easier to reason about and deal with double and quad word
// addresses because the stack pointer will be at the msb rather than the lsb.
// TODO implement storage to push an value at an address and to store to one
// TODO Add bit operations.
// TODO Add system calls, really just C calls.
// TODO Implement dynamic memory
// TODO setup an assembler (can use a different langauge).

typedef unsigned char BYTE;
typedef unsigned short ADDR;

typedef unsigned char WORD;
typedef unsigned short DWORD;
typedef unsigned int QWORD;

// OP codes //////////////////////////////////////////////////////////////////
enum OP{ HALT=0x00,
  PUSH, POP, ADD, SUB, MULT, DIV, EQ, LT, GT, // 09
  PUSH_D, POP_D, ADD_D, SUB_D, MULT_D, DIV_D, EQ_D, LT_D, GT_D, // 12
  PUSH_Q, POP_Q, ADD_Q, SUB_Q, MULT_Q, DIV_Q, EQ_Q, LT_Q, GT_Q, // 1B
  JUMP, JUMP_S, BRANCH  // 1E
};

// Memory ////////////////////////////////////////////////////////////////////
const ADDR P_START = 0x00;
const ADDR LAST_ADDR = 0xffff;
const BYTE WORD_SIZE = 8;
const BYTE ADDR_SIZE = 8;

ADDR get_address(WORD* mem, ADDR addr) {
  return (mem[addr] << ADDR_SIZE) | mem[addr+1];
}

void set_address(WORD* mem, ADDR at, ADDR val) {
  mem[at] = val >> ADDR_SIZE;
  mem[at+1] = (WORD)val;
}

DWORD get_dword(WORD* mem, ADDR addr) {
  return (mem[addr] << WORD_SIZE) | mem[addr+1];
}

void set_dword(WORD* mem, ADDR addr, DWORD data) {
  mem[addr] = data >> WORD_SIZE;
  mem[addr+1] = (WORD)data;
}

QWORD get_qword(WORD* mem, ADDR addr) {
  return (mem[addr] << WORD_SIZE * 3) | (mem[addr+1] << WORD_SIZE * 2)
         | (mem[addr+2] << WORD_SIZE) | mem[addr+3];
}

void set_qword(WORD* mem, ADDR addr, QWORD data) {
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
  if (prog_len > (size_t)LAST_ADDR - P_START) {
    fprintf(stderr, "Error: Program will not fit in memory\n");
    exit(1);
  }
  rewind(fptr);

  fread(mem + P_START, prog_len, 1, fptr);
  if (ferror(fptr)) {
    fprintf(stderr, "Error: Input file was not read\n");
    exit(1);
  }
  fclose(fptr);

  return prog_len;
}

// Main //////////////////////////////////////////////////////////////////////
int main() {
  // Some variables we need
  size_t sp, bp, pc, fp, prog_len;
  BYTE comp;
  WORD* mem;

  // Allocate memory for the VM
  mem = (WORD*) calloc((size_t)LAST_ADDR + 1, sizeof(BYTE));
  if (mem == NULL) {
    fprintf(stderr, "Error: Could not allocate memory for the VM\n");
    exit(1);
  }

  // Read the program file as bytes into memory starting at PSTART
  // TODO use an argument for the program filename
  prog_len = read_program(mem, "input.vm");

  // Set up the address variables
  pc = (size_t)P_START;
  bp = (size_t)LAST_ADDR - 3;
  sp = bp;

  // Debug info
  mem[bp] = 0xaa;
  mem[bp+1] = 0xbb;
  mem[bp+2] = 0xcc;
  mem[bp+3] = 0xdd;

  printf("PC: %x\n", pc);
  printf("BP: %x\n", bp);
  printf("SP: %x\n", sp);

  printf("\nProgram Size: %x\n", prog_len);
  printf("Program Words: ");
  while (pc < (size_t)P_START + prog_len) {
    printf("%x ", mem[pc++]);
  };
  printf("\n");
  pc = P_START;  // To offset the debugging

  // Execute Program
  // Before this can be done there needs to be an instruction set and
  // some implementation for these instructions.
  printf("\n=== Execute Program ===\n");
  bool run = true;
  DWORD a, b;
  QWORD c, d;

  while (run) {
    if (sp > bp) {
      fprintf(stderr, "Error: Stack Underflow: sp=%x, bp=%x\n", sp, bp);
      exit(1);
    } else if (sp <= prog_len) {
      fprintf(stderr, "Error: Stack Overflow: %x\n", sp);
      exit(1);
    } else if (pc >= prog_len) {
      fprintf(stderr, "Error: Program counter out of bounds: pc=%x, bp=%x\n", pc, bp);
      exit(1);
    }

    printf("OP: %x\n", mem[pc]);
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
      case ADD:
        mem[sp+1] = mem[sp] + mem[sp+1];
        sp++;
        break;
      case SUB:
        mem[sp+1] = mem[sp] - mem[sp+1];
        sp++;
        break;
      case MULT:
        mem[sp+1] = mem[sp] * mem[sp+1];
        sp++;
        break;
      case DIV:
        mem[sp+1] = mem[sp] / mem[sp+1];
        sp++;
        break;
      case EQ:
        mem[sp+1] = mem[sp] == mem[sp+1];
        sp++;
        break;
      case LT:
        mem[sp+1] = mem[sp] < mem[sp+1];
        sp++;
        break;
      case GT:
        mem[sp+1] = mem[sp] > mem[sp+1];
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
      case ADD_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, a + b);
        break;
      case SUB_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, a - b);
        break;
      case MULT_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, a * b);
        break;
      case DIV_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=2;
        set_dword(mem, sp, a / b);
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
        mem[sp] = a < b;
        break;
      case GT_D:
        a = get_dword(mem, sp);
        b = get_dword(mem, sp+2);
        sp+=3;
        mem[sp] = a > b;
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
      case ADD_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, c + d);
        break;
      case SUB_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, c - d);
        break;
      case MULT_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, c * d);
        break;
      case DIV_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=4;
        set_qword(mem, sp, c * d);
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
        mem[sp] = c < d;
        break;
      case GT_Q:
        c = get_qword(mem, sp);
        d = get_qword(mem, sp+4);
        sp+=7;
        mem[sp] = c > d;
        break;

      /// JUMPS ///
      case JUMP:
        pc = get_address(mem, ++pc);
        continue;
      case JUMP_S:
        pc = get_address(mem, sp);
        sp+=2;
        continue;
      case BRANCH:
        if (mem[sp++]) {
          pc = get_address(mem, ++pc);
          continue;
        }
        pc+=2;
        break;

      /// BAD OP CODE ///
      default:
        fprintf(stderr, "Error: Unknown OP code: %x\n", mem[pc]);
        exit(1);
    }
    pc++;
  }

  WORD res = mem[sp];
  DWORD resD = get_dword(mem, sp);
  QWORD resQ = get_qword(mem, sp);
  printf("\nmem[sp] = %x (%d), %x (%d), %x (%d)\n", res, res, resD, resD, resQ, resQ);

  // Free the VM's memory
  free(mem);

  return 0;
}
