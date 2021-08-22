from clitest import Test
import vmtest


tests = [
    Test(
        "Forgot to HALT",
        "01 aa 01 bb",
        vmtest.EXIT_POB
    ),
    Test(
        "Bad OP code",
        "01 aa 01 bb 99 00",
        vmtest.EXIT_OP
    ),
    Test(
        "Stack underflow from POP",
        "01 aa 20",
        vmtest.EXIT_SUF
    ),
    Test(
        "Stack overflow from infinite loop",
        "1F aa aa aa aa 1F bb bb bb bb 2F 00 00 00",
        vmtest.EXIT_SOF,
        show_fail_info = False
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles errors",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

