from clitest import Test
import vmtest


tests = [
    Test(
        "Bad OP code",
        "99 00",
        vmtest.EXIT_OP
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles errors",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

