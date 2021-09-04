from clitest import Test
import vmtest


tests = [
    ### Jumps ###
    Test(
        "Jumps to the program address on the top of the stack.",
        "01 00  05 00  3D 00  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    ),
    Test(
        "Jumps by a given offset and not a stack element.",
        "3D 03  01 00  aa aa  01 00  bb bb  00 00",
        "bbbb"
    )

]


if __name__=='__main__':
    vmtest.VmTests("It handles movement operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

