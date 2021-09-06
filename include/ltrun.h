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
  DSP, PC, BFP, FRP_unused,  // 44

  WPRN, DPRN, WPRNU, DPRNU, FPRN, FPRNSC,  // 4A
  PRNCH, PRN, PRNLN, PRNSP, PRNMEM,  // 4F

  WREAD, DREAD, FREAD, FREADSC,  // 53
  READCH, READ_unused, READLN, READSP_unused,  // 57

  BFSTORE, BFLOAD,  // 59
  HIGH, LOW, UNPACK, PACK,  // 5D

  MEMCOPY, STRCOPY,  // 5F
  FMULT, FDIV, FMULTSC, FDIVSC,  // 63
};

enum copy_codes {
  MEM_BUF = 0, MEM_DS,
  BUF_MEM, BUF_DS,
  DS_MEM, DS_BUF,
};


size_t execute(WORD* memory, size_t length, WORD* data_stack, WORD* return_stack);
void exec_memcopy(WORD* memory, WORD* data_stack,
                  ADDRESS bfp, ADDRESS* dsp,
                  WORDU size, WORD code);
void exec_strcopy(WORD* memory, WORD* data_stack,
                  ADDRESS bfp, ADDRESS* dsp, WORD code);

#endif
