# Lieutenant 64

A simple 16 bit stack based byte code virtual machine.

The companion assembler can be found in another [repository](https://github.com/strinsberg/lt64-asm).

# Purpose

The purpose of this project was mostly for fun, but also to learn a little
about low level programming. What better way to think about some of the things
that are important at the machine level than to build your own machine level.
There are obvious differences between the things that can be done in hardware
and what can be done in software, but considering the operations to implement
and their efficiency it is easier to see these things.

I also just love to program and it is fun to find a project that is not so big
that it will take years to complete. A couple tries to get something basic
working only took a couple weeks. Plus a VM can be used as a target for an
assembler and assembly language. It could also be the target for some custom
toy compilers to practice generating assembly or machine code without having
to learn a specific architecture. And lots of widely used programming languages
have VMs or byte code interpreters, so implementing one can help one gain I
sight into those tools.

## Notes

- The name was meant to be cheeky homage to the Commodore 64. It was more
  appropriate for the first version where the VM had a total memory size of
  64kb. Changes to the architecture have made the memory size larger, but the
  name is still fun (to me).
- While I put some effort into efficiency, this is essentially a "toy" VM.
  There will be trade offs between efficiency and things like minimal error
  handling or ease of implementation.
- I am NOT a C programmer so do not expect my C code to be an example of how
  to program in C.
- I have written a small test suite in python. It tests the basic
  functionality of each operation, but may not test all edge cases. Mostly it
  is just hard to test things when one has to write programs in hex (at least for me).
- There are some choices inspired by, or copied from, Forth. However, this is
  not a Forth implementation. Forth is just a really great implementation of
  stack based computing and it would be silly to ignore it when building
  something like this.

# Usage

## Building

The VM is written in plain C. It does not use any special libraries. It uses a
simple Makefile with `gcc` and some simple compiler flags like `-O3` for
release builds and `-D <var_to_define>` for debug and test builds. It is
probably possible to compile it with other C compilers, but I have not tested
this.

```bash
$ git clone https://github.com/strinsberg/lieutenant-64.git
$ cd lieutenant-64

# Make lt64 release executable
$ make release
# Make lt64-debug executable
$ make debug
```

## Running

```bash
# To run release
$ lt64 path_to_file
# To run debug version
$ lt64-debug path_to_file
```

The VM reads the bytes of a file so it is necessary to either edit a file in a
hex editor with the hex values of each operation and argument, which is not
ideal, or use the assembler to produce a binary file for the VM to run. The
second option should be preferred, but if using the first option consult one
of the test files to see how the bytes are expected to be ordered.

### Debug Mode

The debug version of the VM will produce a few lines of output **before**
executing each operation. The debug output includes the current stack contents
(from bottom to top), the value of the current operation, and the program
counter to see where in program memory the operation is located.
The stack contents will list the hex value of each word on the stack, with the
decimal in brackets. The reason for using both is that if the contents are,
for example, 2 characters packed into a single word the decimal number is not
useful.

The debug mode allows stepping through the execution. Before each operation
it provides a prompt `***Step: `. To just execute the next operation press
`Return`. This makes it easy to step through single operations quickly without
skipping any. To run multiple operations before pausing again enter a positive
integer. I.e. `***Step: 19` would run the next `19` operations before asking
for another step. If you don't want to pause at all enter a really high number
and unless your program is really long it should run till it is finished.

Note that due to some idiosyncrasies in C io, when the program asks for input
and does not read a newline the step prompt will read the newline. This means
that after a `:wread` or similar operation the next step will automatically
be skipped. It is not a huge problem as this just immediately shows the result
of the read, but it may not be expected. Also, program output should occur
directly under the `PC: ...` line and have a single newline between it and
`***Step:`.

```
Dstack: 0(0) 2(2) 0(0) 1(1) 0(0) 40(64) ->
Rstack: ->                                             
PC: 10 (16), Next OP: DPUSH

***Step: 
```

In the above example the stack has 6 words on it, the return stack is empty,
the program is at address `0x10`, and the operation that will be performed
for the next step is **dpush**.

## Test Suite

The VM has a collection of simple tests to ensure the bulk of the functionality
works as expected. The test program and tests are written in Python 3 so
Python 3.6+ is required to run the tests.
```
$ make tests
```
Test output shows the title of each test suite run followed by a numbered list
of each test run. Each test line shows it's name and the result. 

```
# Sample truncated passing test output
...
...
======== Handles errors ========
1:  Bad OP code                                                           [PASS]
2:  Stack overflow                                                        [PASS]
3:  Stack underflow                                                       [PASS]
4:  Pc out of bounds                                                      [PASS]
5:  Return stack overflow                                                 [PASS]
6:  Return stack underflow                                                [PASS]


**** 162 Tests Passed ****
```

Failing tests will be reprinted at the bottom of the output with more detailed information including the exit code of the program and and error text if the program exited with an error, and followed by the expected and actual output. When compile with `-D TEST` the VM prints the contents of the stack to *stdout* with each words hex value. Most tests compare this with an expected list of stack contents from stack bottom to top. However, any other program output, i.e. printing strings, will be printed before the stack contents. Tests that expect program output usually pop the contents of the stack so that the only output is the program output.

```
# Sample truncated output with failing test
...
...
======== Handles errors ========
1:  Bad OP code                                                           [PASS]
2:  Stack overflow                                                        [PASS]
3:  Stack underflow                                                       [PASS]
4:  Pc out of bounds                                                      [PASS]
5:  Return stack overflow                                                 [PASS]
6:  Return stack underflow                                                [PASS]


**** Failed Test Results ****

7:  Duplicate stack top - 1                                               [FAIL]
EXPECTED: aabb ccdd aabb
ACTUAL:   aabb ccdd 0000

Tests Failed: 1
```

**NOTE:** The output uses *ansi* color codes in the output to color PASS and
FAIL as well as a couple other things. If your terminal does not support
these the test output will be hard to read. Because the testing "framework"
is homemade it does not support running without these codes.

# Assembler

The assembler for this project is available in another
[repository](https://github.com/strinsberg/lt64-asm). It uses a LISP style
syntax and is written in Clojure. The assembler makes it possible to specify
labeled static program data that can be initialized with optional values or
just declared to make space for use in the program. It also supports writing
subroutines in separate module files and including them in a program or module.
More detailed information can be found in the assembler's repository.

# Architecture

Below is some information on the VM architecture. This includes a discussion
of the data size, instruction format, stack usage, memory layout, and how data
is represented in memory.

## Word Size

This is a 16 bit VM. This means it has a 16 bit word size. Instructions are
encoded as 16 bits even though they only need 8 or less. This means some space
is wasted in the program. In the future non-push operations will pack two
operations into a word. However, in order to keep things simple this has not
been implemented yet. If the VM was intended for real world use it would
probably be necessary, but currently the size of the program in memory is
not an issue.

Another issue with 16 bit words is that 32 bit integers require 2 words to
store. The VM has many operations on double words for integers and fixed point
decimals. This works well, but requires extra work to shift bytes around to get
double words into and out of memory. There is no support for 64 bit numbers
or standard floating point numbers. So this is not a VM that will have high
performance for large number calculations, but of course that is not really its
purpose.

## The Stack(s)

As the name and the mentions in the previous section would suggest, this is a
stack based machine. At first the program, stack, and free memory were all in a
single array of words (originally 8 bit words), but this felt a little too
restrictive after some thought. After reading a little bit about actual
[stack based CPUs](https://users.ece.cmu.edu/~koopman/stack_computers/index.html)
and the [Forth](https://www.forth.com/starting-forth/) language two separate
stacks were added. One data stack to hold values for computation and a second
return stack to hold return addresses for subroutine calls and temporary
values. This makes the operation set require some different things like
duplication of stack elements and swaps, but it also makes the general
operations of the program very simple.

All computation is done on the stack. When adding two numbers they need to be
pushed onto the stack, or left there as the result of previous computation,
then the add operation will pop them and push the result. Other operations
like branching will look on top of the stack for a condition result and an
address to jump to if the condition is true (non-zero). The only operations
that take arguments directly following them in the program memory are push
operations. Everything else gets an argument from the stack or encoded in its
second byte. In the future support could be added either in the VM or the
assembler to specify arguments for ops like jump, call, and branch following
the op rather than having to push them explicitly, but it works well for now.

The return stack is mostly for storing return addresses for subroutine calls.
When the call instruction is executed the address of the next instruction is
pushed onto the return stack before the program counter is set to the address
of the subroutine. When the return operation is executed the top value of the
return stack is assigned to the program counter to return to the correct
instruction.

This is not the only function of the return stack. During a subroutine call
it may be desirable to store some local/temp values somewhere. Instead of
storing them in memory at a given address they can be pushed onto the return
stack. They **MUST** be popped before a subroutine returns though or the
resulting return jump will not go to the intended address and the program
will go into an undefined state or crash.

The other consequence/benefit of the stack based architecture is that there
are no registers available to the programmer for storing values. There are
some pseudo registers for keeping track of different parts of memory, the
program counter, and the stack pointers. These can be read to find their
address values, but not directly mutated.

## Program Memory

The use of 16 bit words means there can be roughly 65k addresses. This gives
128kb of memory for the program and its non-stack data storage. This program
memory is split into 3 parts.

The first is the program instructions. This portion of memory stores the
loaded program, and if using the assembler it also stores static program data
declared in the assembly program. The program pointer points to the current
instruction and execution stops when it executes the halt operation (`0x00`).
This portion of memory is not limited in its size and as long as the program
fits in memory it will be loaded and start running. However if a very large
program uses any free memory then it may crash or have instructions overwritten
with store ops.

Directly after the program instructions is a buffer. This area
(currently 1024 words) is a temporary chunk of memory for reading in string or
manipulating and printing strings. It is not strictly necessary but operations
on it pack two *ascii* characters into each word and there are some ops for
printing null terminated string from the buffer easily. Strings can be copied
to or from the buffer to memory. They can also have individual words copies to
the stack for manipulation and then have them copied back. The buffer is
addressed from 0 to 1023 for its operations to make working on it simpler.
However the buffer pointer can be accessed to get the address of the start of
the buffer if desired. When not being used for strings the buffer can also
be used as temporary storage, but if any read instructions are used before the
data stored is no longer needed it will be lost.

After the buffer the rest of memory is free memory. If the programmer wants
to store data during the program run the can with the load and store
operations. Like the buffer a convenience is provided to allow these
operations to be addressed from 0 so that the programmer does not have to
know where free memory start. With a variable length program the position of
the free pointer is not fixed for every program. However, the **fmp**
address is accessible and if a large portion of free memory will be used it
may be desirable to know where the **fmp** is and how much memory is available.
Free memory is for longer lasting values that are not declared in static memory
in an assembly program and should not be left on the stack for a long time.
Though many simple, and possibly some complex, programs may get by easily with
static memory blocks or just the stack.

## Data Types and Storage

### Signs

As mentioned above all data is stored in 16 bit words. Internally the VM uses
the C `short` type. This is a signed type and there for all operations default
to working with signed values. Of course the bit representation does not change
either way. Where it is necessary unsigned operations are provided to treat the
values as unsigned. Operations that may have unexpected results because of this
will explain in their description below.

### Double words

Double words are stored in two 16 bit memory cells to represent 32 bit values.
In memory the most significant 16 bits are stored in the lower addressed cell
and the least significant 16 bits directly above them. For example `0xaabbccdd`
will be stored on the stack from bottom to top as `[0xaabb, 0xccdd]`.

### Fixed point values

The VM has no floating point numbers. This is because it is easier to represent
and work with fixed point numbers. Fixed point numbers are by default stored
with a scaling factor of `1000` which means calculations will be accurate to
3 decimal places, with some caveats for integer division of the stored
representation. There are some operations that allow using a custom scaling
factor from 1 to 9 significant digits. They are stored in a double word to
give enough size for reasonable usage and they are always treated as signed
numbers. The max size for default scaled numbers is then the same as C's max
`int` value divided by the scaling factor. The internal storage is then just
the floating point number read in, or entered in the assembler, multiplied by
the scaling factor and stored as an integer, discarding any decimal digits
after the multiplication (not rounding).

Because of the internal representation many fixed point operations can be done
with double word operations. Where this would not work special fixed point
operations are provided. When internally an operation would have a larger
representation for intermediate values a larger size is used to prevent
unexpected rounding. I.e. multiplying two integers where the first 3 digits
are for the decimal places will give a result that would have the first 6
digits as decimal places. So the number may be up to 3 digits larger than
could be stored in a double word before it is scaled back down to have 3
digits of decimal precision. This extra size is handled appropriately
internally. So multiplications will only overflow if the result would overflow.

### Characters

Characters are stored in the buffer as two 8 bit *ascii* characters per word. The characters will be in order in the way they are read in with the first character in the top 8 bits and the second character in the bottom 8 bits. I.e. reading in "AB" will store `0x6565` in the first word of the buffer. There are several operations such as read or print that will use/expect this encoding. Other operations are discussed below that allow working with this representation on the stack more easily.

### Overflow and Underflow

All arithmetic operations can overflow and underflow. Word calculations wrap around like C `short` types do and double word calculations wrap around like `int` types do. The storage for addresses uses a single word as an unsigned value which means that rather than go out of bounds when addressing program memory operations on addresses will wrap around to the other end of memory. Because the stacks are smaller they can detect over and underflow with potential addresses, but the program memory cannot. This must be kept in mind when doing calculations on addresses for accessing program memory. On one hand it is nice that you cannot access memory out of bounds, hopefully preventing `SEGFAULT`, but if calculations wrap an address around it could produce very unexpected results.

# VM Operations

Any operation preceded with a **d** is a double word version of the operation. I.e. **push** for 16 bit values and **dpush** for 32 bit values.Where double word operations would not work on fixed point values operations preceded with an **f** are provided. I.e. **mult** for fixed point is **fmult**.

Any ending in a **u** is an unsigned operation. Unsigned operations are available only where the resulting bytes will be different for signed vs unsigned. I.e. **lt** says `0xff` is less than `0x00` when signed, but the same values with **ltu** have `0xff` greater than `0x00` when unsigned.

**NOTE:** OP codes are not included with the operations, though the names are the same as those used internally in the `op_code` enum which can be found in `run.h`. The enum has some comments with the hex values of some of the codes to make it easier to find which operations use which codes, necessary for reading and writing the tests. However, if the assembler is used to write programs no knowledge of the opcodes in necessary.

## Stack Manipulation

These operations help to move values on or off the stack. There are also some Forth operations that help manage values on the stack and their order.

### push, dpush

These operations move data specified in the program onto the top of the stack. This can be addresses, numbers, double numbers, and in the assembler labels that are converted to addresses. Pushing a value adds it above any current values and increments the data stack pointer (**dsp**) to point to the new value.

### load, dload, store, dstore

These operations move values between the stack and program memory. By default they treat the address on top of the stack as an offset from the free memory pointer (**fmp**). This allows storing values at runtime easier to keep track of in free memory. However, if the top byte of the ops word is `0x01` then the will treat the value on top of the stack as a plain address in program memory. This is used mostly for accessing labeled static memory. Both expect the top of stack to be an address or offset, store expects the next value (top - 1) to be the value to store. All required arguments are popped from the stack.

### fst, dfst, sec, dsec, nth, dnth

These operations duplicate items on the stack and push the duplicated value on top of the stack preserving the original. **fst** duplicates the stack top, **sec** duplicates the stack top - 1, and **nth** duplicates the nth value down the stack (where top is 0). The elements duplicated are not popped. This is handy when a subroutine call will consume its arguments and you still want them after the call.

### swap, dswap, rot, drot

These are some more handy Forth inspired operations to adjust the order of data on the stack. **swap** takes the top two elements and changes their places on the stack. **rot** takes the third stack element and moves it to the top. This moves the other two back. For example if the stack from bottom to top was `[A,B,C,D]` after rot it would be `[A,C,D,B]`.

### rpush, drpush, rpop, drpop, rgrab, drgrab

These ops deal with the return stack directly. **rpush** takes the top element of the data stack and moves it to the return stack. **rpop** takes the top element of the return stack and moves it onto the data stack. This is different from pop which discards values popped from the data stack. **rgrab** duplicates the top return stack element and pushes it onto the data stack. Other than **call** and **ret** which push and pop addresses from the return stack these are the only operations that manipulate the return stack.

## Arithmetic Operations

### add, dadd

Pops the top two stack element and push the result of thier addition onto the stack.

### sub, dsub

Pops the top two stack elements and subtracts top from top - 1. For example from bottom to top of the stack if we have `[1,2,3]` after sub we will have `[1,-1]`. Other arithmetic operations where order matters follow this convention.

### mult, dmult, multu

Pop the top two stack elements and push the result onto the stack. **multu** treats the top two numbers as unsigned words and pushes the result as a double word. This prevents overflow. There is no double word equivalent because there is no support for quad words, and multiplication on the bits of signed and unsigned numbers otherwise has the same results. It only matters how the bits are interpreted for other operations.

### div, ddiv, divu, ddivu

All versions pop the top two stack elements and divide the top - 1 stack element by the top. This is integer division as done in C so values that would result in fractions are rounded toward `0`. That means `-1.23` will be `-1` **NOT** `-2`. Use the unsigned versions if the values are being treated as unsigned. For example `0x10 / 0xff(-1)` is `0xf0(-16)` when signed, but it is just `0x00` when unsigned as `0xff` is much larger than `0x10`.

### mod, dmod, modu, dmodu

Pops the top two stack elements and takes top - 1 stack element mod by the top.

**NOTE:** The behavior of mod is the [default of the C % operator](https://en.cppreference.com/w/c/language/operator_arithmetic). This may not be intuitive if the numbers involved are negative.

### eq, deq, lt, dlt, gt, dgt, ltu, dltu, gtu, dgtu

Pops the top two stack elements and compares them. The unsigned versions treat the numbers as unsigned as `0xff` is less than `0x01` when signed, but greater when unsigned. Where  `1` is pushed onto the stack when `true` and `0` when `false`.

## Bitwise Operations

### sl, sr, dsl, dsr

Pops the top two stack elements and shift the top - 1  element the number of times given by the top. These are always signed and will perform sign extension. This means shifting a negative number right will not make it a positive number as the most significant bit will be filled with a `1` and not a `0`.

### and, dand, or, dor, not, dnot

Bitwise operations on the top of the stack. And and or pop the top two elements and push the result. Not simply replaces the top element with its bitwise and. Note that given `0` and `1` these can behave like logic operations, however since truth values can be any non-zero value there could be unexpected results if the elements are not guaranteed to be `0` or `1`. So some caution should be used when using them as logic operations.

## Character Operations

### bufload, bufstore

Similar to **load** and **store**, but move between the stack and buffer. The top stack value is always read as an unsigned offset from the buffer pointer (**bfp**).

### high, low

These are more character operations, but they can be used to code and encode bytes. **high** pushes the top byte of a word onto the stack in the low byte position. **low** pushes the lower byte of the top element on the stack into the lower byte position. For example given the stack `[0x6566]` **high** will produce a stack of `[0x6566, 0x0065]` and **low** will produce a stack of `[0x6566, 0x0066]`.

**NOTE:**  Because these are specifically intended to be used on *ascii* characters they do not sign extend. The resulting word on the stack with have the top 8 bits zeroed.

### pack, unpack

**pack** pops the top two stack elements and puts the lower byte of the top into lower byte of a word and the lower byte from the top - 1 element and puts it into the top byte of the same word and pushes this onto the stack. For example given the stack `[0x0065, 0x0066]` **pack** gives `[0x6566]`.

**unpack** pops the top stack element and puts the top byte of the element in the lower byte of a word and pushes it. It then takes the lower byte of the element and puts it in the lower byte of a word and pushes it. For example given the stack `[0x6566]` **unpack** gives `[0x0065, 0x0066]`.

## Movement

### jump

Pops an address element from the top of the stack and sets the program counter (**pc**) to that address and continues from the new **pc** value.

### branch

Pops the top two elements of the stack. If the top - 1 element is non-zero then it sets **pc** to the value of top and continues the program from there.

### call

First pushes `pc + 1` onto the return stack. Then jumps to the address on top of the data stack.

### ret

Pops the top of the return stack and jumps to the address it represents.

### dsp, pc, bfb, fmp

Pushes the address of the respective pointer onto the stack.

## I/O Operations

### wprn, dprn, wprnu, dprnu

Pops the top element from the stack and prints it as a signed or unsigned decimal integer.

### prnch, prnpk

**prnch** pops the top word and prints the bottom byte as an 8 bit *ascii* char. **prnpk** prints the top word as two charcters. The first character is in the top byte and the second in the low byte.

### prn, prnln, prnmem

The first two do not affect the stack and print the character buffer from `buf[0]` to the first `null (0x00)` byte.

**prnmem** has the same printing behavior, but it pops an word off the stack and starts printing from **fmp** + the value popped. It can also have a `1` encoded into the top byte in order to print using the popped value as an address and not an offset from **fmp**.

### wread, dread

Reads a 16 or 32 bit integer from *stdin* onto the stack. Accepts either signed or unsigned numbers as larger unsigned numbers that are in range are stored the same as signed numbers.

### readch

Reads the next char from *stdin* onto the stack. This reads the char into the bottom byte of the word that is placed on the stack. There is no way to automatically pack these read characters into a single word.

### readln

Read the next line into the buffer as a null terminated string. Will always make the last buffer element a `0x0000`.

## Fixed Point Numbers

These operations are similar to signed double word operations, but with scaling factors applied to deal with extra decimal places that may be created in the intermediate numbers.

### fmult, fdiv

Perform multiplication and division on the top two double words on the stack while treating them as default scaled (`3` significant digits) fixed point numbers.

### fmultsc, fdivsc

Pop the top word of the stack to use as the number of significant digits for the scaling factor. Then perform the operation the same as **fmult** and **fdiv**. For example to use `2` significant digits (scale factor of `100`) the operation would have `0x0002` on top of the stack. The maximum number of significant digits is `9` and any time a larger number is given it will be treated as the default number of significant digits `3`. Giving `0x0001` will just treat the numbers as integers.

### fprn

Print the top double word on the stack as a fixed point number. Uses the default scaling factor of `1000` for `3` significant digits. Always prints with the number of significant digits even if they are zeros. I.e. `1.2` with default scaling will print as `1.200`.

### fprnsc

Pop the top word off the stack and use it as the number of siginificant digits for the scaling factor. Then print the top double word on the stack as a fixed point number.

