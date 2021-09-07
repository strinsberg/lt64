from clitest import Test
import vmtest


tests = [
    Test(
        "Bad OP code",
        "99 00  00 00",
        vmtest.EXIT_OP
    ),
    Test(
        "Stack overflow",
        "01 00  aa aa  01 00  00 00  3D 00  00 00",
        vmtest.EXIT_SOF
    ),
    Test(
        "Stack underflow",
        "02 00  00 00",
        vmtest.EXIT_SUF
    ),
    Test(
        "Pc out of bounds",
        "01 00  aa aa  3D 00  00 00",
        vmtest.EXIT_POB
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles errors",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

