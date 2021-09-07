#ifndef LT_64_MEM_H
#define LT_64_MEM_H

#include "ltconst.h"

static inline DWORD get_dword(WORD* mem, ADDRESS pos) {
  return (mem[pos] << WORD_SIZE) | (mem[pos+1] & 0xffff);
}

static inline void set_dword(WORD* mem, ADDRESS pos, DWORD val) {
  mem[pos] = val >> WORD_SIZE;
  mem[pos+1] = (WORD)val;
}

static inline DWORD get_rev_dword(WORD* mem, ADDRESS pos) {
  return (mem[pos+1] << WORD_SIZE) | (mem[pos] & 0xffff);
}

static inline void set_rev_dword(WORD* mem, ADDRESS pos, DWORD val) {
  mem[pos+1] = val >> WORD_SIZE;
  mem[pos] = (WORD)val;
}

static inline WORDU string_length(WORD* mem, ADDRESS start) {
  ADDRESS atemp = start;
  while (atemp) {
    if (!mem[atemp]) break;
    atemp--;
  }
  return start - (atemp - 1);
}

#endif
