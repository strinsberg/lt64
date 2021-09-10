"""
Tests for word operations on the lieutenant-64 virtual machine.

Test input is given as a hex string specifying the bytes of the program the
VM will read. These can be given with spaces between bytes or words and all
spaces and newlines will be stripped before converting the hex to bytes and
writing to a file.

Bytes are given in little endian order. This means that for a word the bytes
are given low byte then high byte. I.e. to get the hex number aabb you need
to write the least significant byte first. So it would be 'bb aa' in a string
for program input. However, somewhat contrary to this double words are stored
on the stack and in memory with the most significant word first and the least
significant word on top. I.e when putting the double word aabbccdd as an
argument to DPUSH it would be split into the two words aabb and ccdd. The
order is correct for word with just this split, but then each word must be
reordered as specified above. Meaning the final result would be 'bb aa  dd cc'.
The spaces are optional, but given the rules for ordering it makes sense to
use them to separate bytes and words. Most of the tests try to have 1 space
between the bytes of a word and 2 spaces between words.

Now to add to the confusion of the bytes the stacks are printed bottom to top
and each word is printed as any normal number with it's most significant digits
first. So if we push 'aa bb' onto the stack it will be printed out 'bbaa'. This
output makes sense as it is just printing a 16 bit number in hex, but it will
seem backward to the input.

For more information on how each operation works see the lieutenant-64 README.
"""
from clitest import Test
import vmtest

tests = [
    ### Standard ops ###
    Test(
        "Push words",
        "01 00  bb aa  01 00  dd cc  00 00",
        "aabb ccdd"
    ),
    Test(
        "Pop words",
        "01 00  bb aa  01 00  dd cc  02 00 00 00",
        "aabb"
    ),
    Test(
        "Store and load words relative to top of memory",
        "01 00 bb aa 01 00 dd cc"
        + "01 00  00 00  04 00  01 00  01 00  04 00"
        + "01 00  00 00  03 00  01 00  01 00  03 00  00 00",
        "ccdd aabb"
    ),
    Test(
        "Load words at a specific address",
        "01 00  02 00  03 01  01 00  03 00  03 01  00 00",
        "0103 0001"
    ),
    Test(
        "Store and load words at a specific address",
        "01 00  bb aa  01 00  dd cc"
        + "01 00  ff ff  04 01  01 00  fe ff  04 01"
        + "01 00  ff ff  03 01  01 00  fe ff  03 01  00 00",
        "ccdd aabb"
    ),

    ### Manipulation ###
    Test(
        "Duplicate stack top",
        "01 00  bb aa  01 00  dd cc  05 00  00 00",
        "aabb ccdd ccdd"
    ),
    Test(
        "Duplicate stack top - 1",
        "01 00  bb aa  01 00  dd cc  06 00  00 00",
        "aabb ccdd aabb"
    ),
    Test(
        "Duplicate nth element down from stack top",
        "01 00  bb aa  01 00  dd cc  01 00  ff ee"
        + "01 00  02 00  07 00  00 00",
        "aabb ccdd eeff aabb"
    ),
    Test(
        "Swap the top two stack elements",
        "01 00  bb aa  01 00  dd cc  08 00  00 00",
        "ccdd aabb"
    ),
    Test(
        "Rotate 3rd stack (top - 2) element to stack top",
        "01 00  bb aa  01 00  dd cc  01 00  ff ee  09 00  00 00",
        "ccdd eeff aabb"
    ),

    ## Return stack ##
    Test(
        "Push an element onto return stack and get it back",
        "01 00  bb aa  0A 00  01 00  dd cc  0B 00  0C 00  00 00",
        "ccdd aabb 0000"
    ),
    Test(
        "Push an element onto return stack and grab it twice",
        "01 00  bb aa  0A 00  01 00  dd cc  0C 00  0B 00  0C 00  00 00",
        "ccdd aabb aabb 0000"
    ),

    ## Arithmetic ##
    Test(
        "Add the top two stack elements",
        "01 00  04 00  01 00  05 00  19 00  00 00",
        "0009"
    ),
    Test(
        "Add the top two stack elements, One is negative",
        "01 00  04 00  01 00  fe ff  19 00  00 00",
        "0002"
    ),
    Test(
        "Subtract the top two stack elements",
        "01 00  04 00  01 00  05 00  1A 00  00 00",
        "ffff"
    ),
    Test(
        "Subtract the top two stack elements, One is negative",
        "01 00  04 00  01 00  fe ff  1A 00  00 00",
        "0006"
    ),
    Test(
        "Multiply the top two stack elements",
        "01 00  04 00  01 00  05 00  1B 00  00 00",
        "0014"
    ),
    Test(
        "Multiply the top two stack elements, One is negative",
        "01 00  04 00  01 00  fe ff  1B 00  00 00",
        "fff8"
    ),
    Test(
        "Divide the top two stack elements",
        "01 00  0A 00  01 00  05 00  1C 00  00 00",
        "0002"
    ),
    Test(
        "Divide the top two stack elements, One is negative",
        "01 00  04 00  01 00  ff ff  1C 00  00 00",
        "fffc"
    ),
    Test(
        "Mod the top two stack elements",
        "01 00  08 00  01 00  03 00  1D 00  00 00",
        "0002"
    ),
    Test(
        "Mod the top two stack elements, Bottom is negative",
        "01 00  08 00  01 00  fd ff  1D 00  00 00",
        "0002"
    ),
    Test(
        "Mod the top two stack elements, Top is negative",
        "01 00 f8 ff  01 00  03 00  1D 00  00 00",
        "fffe"
    ),

    ## Comparisson ##
    Test(
        "Check the top two stack elements for equality, Pass",
        "01 00  08 00  01 00  08 00  1E 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements for equality, Fail",
        "01 00  08 00  01 00  03 00  1E 00  00 00",
        "0000"
    ),
    Test(
        "Check the top two stack elements bottom < top, Pass",
        "01 00  03 00  01 00  08 00  1F 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements bottom < top, Fail",
        "01 00  08 00  01 00  03 00  1F 00  00 00",
        "0000"
    ),
    Test(
        "Check the top two stack elements bottom < top, One neg, Pass",
        "01 00  ff ff  01 00  03 00  1F 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements bottom > top, Pass",
        "01 00  08 00  01 00  03 00  20 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements bottom > top, Fail",
        "01 00  03 00  01 00  08 00  20 00  00 00",
        "0000"
    ),
    Test(
        "Check the top two stack elements bottom > top, One neg, Pass",
        "01 00  03 00  01 00  ff ff  20 00  00 00",
        "0001"
    ),

    ## Unsigned Arithmetic and Comparisson ##
    Test(
        "(Unsigned) Multiply 2 words and store as double word, large",
        "01 00  E8 FD  01 00  E8 03  21 00  00 00",
        "03df d240"
    ),
    Test(
        "(Unsigned) Multiply 2 words and store as double word",
        "01 00  00 7D  01 00  E8 03  21 00  00 00",
        "01e8 4800"
    ),
    Test(
        "(Unsigned) Divide 2 words on stack, large",
        "01 00  E8 FD  01 00  E8 03  22 00  00 00",
        "0041"
    ),
    Test(
        "(Unsigned) Divide 2 words on stack",
        "01 00  00 7D  01 00  E8 03  22 00  00 00",
        "0020"
    ),
    Test(
        "(Unsigned) Mod the top two stack elements",
        "01 00  08 00  01 00  03 00  23 00  00 00",
        "0002"
    ),
    Test(
        "(Unsigned) Mod the top two stack elements, Bottom is large",
        "01 00  08 00  01 00  fd ff  23 00  00 00",
        "0008"
    ),
    Test(
        "(Unsigned) Mod the top two stack elements, Top is large",
        "01 00 f8 ff  01 00  03 00  23 00  00 00",
        "0002"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, Pass",
        "01 00  03 00  01 00  08 00  24 00  00 00",
        "0001"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, Fail",
        "01 00  08 00  01 00  03 00  24 00  00 00",
        "0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, large, Fail",
        "01 00  ff ff  01 00  03 00  24 00  00 00",
        "0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, Pass",
        "01 00  08 00  01 00  03 00  25 00  00 00",
        "0001"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, Fail",
        "01 00  03 00  01 00  08 00  25 00  00 00",
        "0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, large, Fail",
        "01 00  03 00  01 00  ff ff  25 00  00 00",
        "0000"
    ),

    ## Bits ##
    Test(
        "Left shift word at top-1 by top",
        "01 00  02 00  01 00  02 00  26 00  00 00",
        "0008"
    ),
    Test(
        "Left shift word on top of the stack",
        "01 00  02 00  26 01  26 01  00 00",
        "0008"
    ),
    Test(
        "Left shift word on top of the stack, negative",
        "01 00  fe ff  26 01  26 01  00 00",
        "fff8"
    ),
    Test(
        "Right shift word on top of the stack",
        "01 00  08 00  01 00  02 00  27 00  00 00",
        "0002"
    ),
    Test(
        "Right shift word on top of the stack",
        "01 00  08 00  27 01  27 01  00 00",
        "0002"
    ),
    Test(
        "Right shift word on top of the stack, negative",
        "01 00  f8 ff  27 01  27 01  00 00",
        "fffe"
    ),
    Test(
        "Bitwise and the 2 words on top of the stack",
        "01 00  ff 00  01 00  00 ff  28 00  00 00",
        "0000"
    ),
    Test(
        "Bitwise or the 2 words on top of the stack",
        "01 00  00 ff  01 00  ff 00  29 00  00 00",
        "ffff"
    ),
    Test(
        "Bitwise not the word on top of the stack",
        "01 00  f0 f0  2A 00  00 00",
        "0f0f"
    ),
]

