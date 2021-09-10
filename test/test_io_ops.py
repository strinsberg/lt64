"""
Tests for movement operations on the lieutenant-64 virtual machine.

See the test_words.py file for some more information on how test input and
output is written.

Printing tests all need clean stacks at the end of the VM run. This way nothing
is printed for the stack and the expected output can just be what should be
printed. If it is desireable the stack contents will be printed immediately
after any other output with no added newlines or spaces. So if you don't print
a space or newline you could get someting like '-1aabb' for output. This is
fine, but not super intuitive.

Read tests take an extra input member after the program input. This input will
be sent to stdin during the VM execution. If the program is going to read a
whole line the given input string must have a newline added at the end.

See the lieutenant-64 README for more information on what each operation
does.
"""
from clitest import Test
import vmtest

tests = [
    ### Print Numbers ###
    Test("Prints a word as a signed int",
         "01 00  ff ff  45 00  00 00",
         "-1"
    ),
    Test("Prints a double word as a signed int",
         "0D 00  ff ff  ff ff  46 00  00 00",
         "-1"
    ),
    Test("(Unsigned) Prints a word",
         "01 00  ff ff  47 00  00 00",
         "65535"
    ),
    Test("(Unsigned) Prints a double word",
         "0D 00  ff ff  ff ff  48 00  00 00",
         "4294967295"
    ),
    Test("Prints a fixed point number with default 1000 scaling",
         "0D 00  00 00  8B 27  49 00  00 00",
         "10.123"
    ),
    Test("Prints a fixed point number with given scaling",
         "0D 00  12 00  A6 D6  4A 02  00 00",
         "12345.98"
    ),

    ## Strings and Chars ##
    Test("Prints characters",
         "01 00  43 44  01 00  41 42  4B 00  4B 00  00 00",
         "AC"
    ),
    Test("Prints a string from the buffer",
         "01 00  41 42  58 01  01 00  43 44  58 02"
         + "4C 00  00 00",
         "ABCD"
    ),
    Test("Prints a string from the buffer with a new line",
         "01 00  41 42  58 01  01 00  43 44  58 02"
         + "4D 00  00 00",
         "ABCD\n"
    ),
    Test("Prints a string from memory",
         "01 00  41 42  01 00 00 00  04 00"
         + "01 00  43 44  01 00  01 00  04 00"
         + "01 00  00 00  01 00  02 00  04 00"
         + "01 00  00 00  4F 00  00 00",
         "ABCD"
    ),


]

read_tests = [
    ### Read Number Tests ###
    vmtest.IoTest(
        "Reads in a word sized negative int",
        "50 00  00 00",
        "-1",  # input
        "ffff"  # expected stack
    ),
    vmtest.IoTest(
        "Reads in a double word sized negative int",
        "51 00  00 00",
        "-1",
        "ffff ffff"
    ),
    vmtest.IoTest(
        "Reads in a fixed point number and default scale it",
        "52 00  00 00",
        "10.123",
        "0000 278b"
    ),
    vmtest.IoTest(
        "Reads in a fixed point number and user scale it",
        "53 02  00 00",
        "10.123",
        "0000 03f4"
    ),
    vmtest.IoTest(
        "Reads in a character",
        "54 00  54 00  00 00",
        "AB",
        "0041 0042"
    ),
    vmtest.IoTest(
        "Reads a string up to a space into the buffer.",
        "56 00  4C 00  00 00",
        "ABCD\n",
        "ABCD"
    ),

]

