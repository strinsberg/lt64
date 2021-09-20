#ifndef LT_64_RUN_H
#define LT_64_RUN_H

#include "ltconst.h"
#include "stddef.h"

/* All op codes for the VM.
 * If new codes are added at this point they MUST be added to the end. The
 * VM will still run fine if they are rearranged, but the tests depend on the
 * current code assignment.
 */
typedef enum op_codes { HALT=0,
  PUSH, POP, LOAD, STORE,  // 04
  FST, SEC, NTH,  // 07
  SWAP, ROT,  // 09
  RPUSH, RPOP, RGRAB,  // 0C

  DPUSH, DPOP, DLOAD, DSTORE,  // 10
  DFST, DSEC, DNTH,  // 13
  DSWAP, DROT,  // 15
  DRPUSH, DRPOP, DRGRAB,  // 18

  ADD, SUB, MULT, DIV, MOD,  // 1D
  EQ, LT, GT,  // 20
  MULTU, DIVU, MODU, LTU, GTU,  // 25

  SL, SR,  // 27
  AND, OR, NOT,  // 2A

  DADD, DSUB, DMULT, DDIV, DMOD,  // 2F
  DEQ, DLT, DGT,  // 32
  DMULTU_unused, DDIVU, DMODU, DLTU, DGTU,  // 37

  DSL, DSR,  // 39
  DAND, DOR, DNOT,  // 3C

  JUMP, BRANCH, CALL, RET,  // 40
  DSP, PC, BFP, FMP,  // 44

  WPRN, DPRN, WPRNU, DPRNU, FPRN, FPRNSC,  // 4A
  PRNCH, PRN, PRNLN, PRNSP_unused, PRNMEM,  // 4F

  WREAD, DREAD, FREAD, FREADSC,  // 53
  READCH, READ_unused, READLN, READSP_unused,  // 57

  BFSTORE, BFLOAD,  // 59
  HIGH, LOW, UNPACK, PACK,  // 5D

  MEMCOPY, STRCOPY,  // 5F
  FMULT, FDIV, FMULTSC, FDIVSC,  // 63

  PRNPK, READCH_BF, STREQ, MEMEQ, // 67
  IS_EOF, RESET_EOF, // 69

  BRKPNT, // 6A

} OP_CODE;

// Some additional codes to track the direction of memory copies
enum copy_codes { MEM_BUF = 0, BUF_MEM };

/* Runs a program starting at position 0 in the given program memory.
 * The length is the length of the program that has been loaded into memory
 * and is used to calculate the positions of buffer and free memory pointers.
 * The data and return stacks are expected to be empty. Any memory loaded into
 * them before running this function will be lost.
 * Returns an exit code based on the result of the program execution.
 */
size_t execute(WORD* memory, size_t length, WORD* data_stack, WORD* return_stack);

#endif
