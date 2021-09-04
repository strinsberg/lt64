#ifndef LT_64_RUN_H
#define LT_64_RUN_H

#include "ltconst.h"
#include "stddef.h"

enum op_codes { HALT=0,
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
  DSP, PC, RSP_unused,  // 43

  PRN, DPRN, PRNU, DPRNU, FPRN,  // 48
  PRNCH, PRNSTR,  // 4A

  READ, DREAD, FREAD, READCH,  // 4E
  READSTR, READLN,  // 50

  FMULT, FDIV,  // 52
};

size_t execute(WORD* memory, size_t length, WORD* data_stack, WORD* return_stack);

#endif
