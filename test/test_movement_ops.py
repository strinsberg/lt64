from clitest import Test
import vmtest


tests = [
    Test(
        "Jump some WORD PUSH instructions",
        "01 aa 10 00 08 2E 01 bb 01 cc 00",
        "cc aa"
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles movement operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()
