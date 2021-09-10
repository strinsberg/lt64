"""
Tests for movement operations on the lieutenant-64 virtual machine.

See the test_words.py file for some more information on how test input and
output is written.

See the lieutenant-64 README for more information on what each operation
does.
"""
from clitest import Test
import vmtest


tests = [
    ### Jumps ###
    Test(
        "Jumps to the program address on the top of the stack",
        "01 00  05 00  3D 00  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),
    Test(
        "Jumps by offset in top byte and not a stack element",
        "3D 03  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),

    ### Branch ###
    Test(
        "Branches to the address at top when top - 1 is non zero (true)",
        "01 00  01 00  01 00  07 00  3E 00  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),
    Test(
        "Branches by a given offset when top is non zero (true)",
        "01 00  01 00  3E 03  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),
    Test(
        "Doesn't Branch to when top is zero (false)",
        "01 00  00 00  01 00  07 00  3E 00  01 00  aa aa  01 00  bb bb  00 00",
        "aaaa bbbb"
    ),
    Test(
        "Doesn't Branch to when top is zero (false), offset",
        "01 00  00 00  3E 03  01 00  aa aa  01 00  bb bb  00 00",
        "aaaa bbbb"
    ),

    ### Call and Ret ###
    Test(
        "Call jumps to an address on the stack and returns",
        "01 00  06 00  3F 00  01 00  aa aa  00 00  01 00  bb bb  40 00",
        "bbbb aaaa"
    ),

    ### Address Pushes ###
    Test(
        "Pushes the data stack pointer address onto the stack",
        "01 00  aa aa  41 00  00 00",
        "aaaa 0001"
    ),
    Test(
        "Pushes the data stack pointer address onto the stack + offset",
        "01 00  aa aa  41 05  00 00",
        "aaaa 0006"
    ),
    Test(
        "Pushes the program counter address onto the stack",
        "01 00  aa aa  42 00  00 00",
        "aaaa 0002"
    ),
    Test(
        "Pushes the program counter address onto the stack + offset",
        "01 00  aa aa  42 05  00 00",
        "aaaa 0007"
    ),
    Test(
        "Pushes the char buffer address onto the stack",
        "01 00  aa aa  43 00  00 00",
        "aaaa 0004"
    ),
    Test(
        "Pushes the char buffer address onto the stack + offset",
        "01 00  aa aa  43 05  00 00",
        "aaaa 0009"
    ),
    Test(
        "Pushes the free memory address onto the stack + offset",
        "01 00  aa aa  44 00  00 00",
        "aaaa 0404"
    ),
    Test(
        "Pushes the free memory address onto the stack + offset",
        "01 00  aa aa  44 05  00 00",
        "aaaa 0409"
    ),

    ## Memory copying ##
    Test(
        "Copy memory from memory to buffer",
        "01 00  41 42  01 00  00 00  04 00"
        + "01 00  43 44  01 00  01 00  04 00"
        + "01 00  00 00  01 00  02 00  5E 00  4C 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy memory from buffer to memory",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "01 00  00 00  01 00  02 00  5E 01"
        + "01 00  00 00  4F 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from memory to buffer",
        "01 00  41 42  01 00  00 00  04 00"
        + "01 00  43 44  01 00  01 00  04 00"
        + "01 00  00 00  5F 00  4C 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from buffer to memory",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "01 00  00 00  5F 01"
        + "01 00  00 00  4F 00  00 00",
        "ABCD"
    ),

    ### Buffer and Chars ###
    Test(
        "Store words in the char buffer",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "4C 00  00 00",
        "ABCD"
    ),
    Test(
        "Store words in the char buffer, using offset",
        "01 00  41 42  58 01"
        + "01 00  43 44  58 02"
        + "4C 00  00 00",
        "ABCD"
    ),
    Test(
        "Load words in the char buffer",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "01 00  01 00  59 00"
        + "01 00  00 00  59 00  00 00",
        "4443 4241"
    ),
    Test(
        "Load words in the char buffer, using offset",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "59 02  59 01  00 00",
        "4443 4241"
    ),
    Test(
        "High duplicates the high byte as a full word in the low byte pos",
        "01 00  43 44  5A 00  00 00",
        "4443 0044"
    ),
    Test(
        "High duplicates without sign extension",
        "01 00  43 ff  5A 00  00 00",
        "ff43 00ff"
    ),
    Test(
        "Low duplicates the low byte as a full word",
        "01 00  43 44  5B 00  00 00",
        "4443 0043"
    ),
    Test(
        "Unpack the top word into high and low and push them onto stack",
        "01 00  43 44  5C 00  00 00",
        "4443 0044 0043"
    ),
    Test(
        "Pack the low bytes of top 2 words into a single word on the stack",
        "01 00  44 00  01 00  43 00  5D 00  00 00",
        "4443"
    ),

]


if __name__=='__main__':
    vmtest.VmTests("It handles movement operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

