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
        "Branches to the address at top - 1 when top is non zero (true)",
        "01 00  07 00  01 00  01 00  3E 00  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),
    Test(
        "Branches by a given offset when top is non zero (true)",
        "01 00  01 00  3E 03  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),
    Test(
        "Doesn't Branch to when top is zero (false)",
        "01 00  07 00  01 00  00 00  3E 00  01 00  aa aa  01 00  bb bb  00 00",
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
        "aaaa 0404"
    ),
    Test(
        "Pushes the char buffer address onto the stack + offset",
        "01 00  aa aa  43 05  00 00",
        "aaaa 03ff"
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
        "Copy memory from memory to stack",
        "01 00  41 42  01 00  00 00  04 00"
        + "01 00  43 44  01 00  01 00  04 00"
        + "01 00  00 00  01 00  02 00  5E 01  4E 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy memory from buffer to memory",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "01 00  00 00  01 00  02 00  5E 02"
        + "01 00  00 00  4F 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy memory from buffer to stack",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "01 00  02 00  5E 03  4E 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy memory from stack to memory",
        "01 00  00 00  01 00  43 44  01 00  41 42"
        + "01 00  00 00  01 00  03 00  5E 04"
        + "01 00  00 00  4F 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy memory from stack to buffer",
        "01 00  00 00  01 00  43 44  01 00  41 42"
        + "01 00  03 00  5E 05  4C 00  00 00",
        "ABCD"
    ),

    ## String copying ##
    Test(
        "Copy string from memory to buffer",
        "01 00  41 42  01 00  00 00  04 00"
        + "01 00  43 44  01 00  01 00  04 00"
        + "01 00  00 00  5F 00  4C 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from memory to stack",
        "01 00  41 42  01 00  00 00  04 00"
        + "01 00  43 44  01 00  01 00  04 00"
        + "01 00  00 00  5F 01  4E 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from buffer to memory",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "01 00  00 00  5F 02"
        + "01 00  00 00  4F 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from buffer to stack",
        "01 00  41 42  01 00  00 00  58 00"
        + "01 00  43 44  01 00  01 00  58 00"
        + "5F 03  4E 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from stack to memory",
        "01 00  00 00  01 00  43 44  01 00  41 42"
        + "01 00  00 00  5F 04"
        + "01 00  00 00  4F 00  00 00",
        "ABCD"
    ),
    Test(
        "Copy string from stack to buffer",
        "01 00  00 00  01 00  43 44  01 00  41 42"
        + "5F 05  4C 00  00 00",
        "ABCD"
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles movement operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

