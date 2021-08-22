from clitest import Test
import vmtest


tests = [
    ### Stack Manipulation ###
    Test(
        "it pushes QWORDs",
        "1F aa aa aa aa 1F bb bb bb bb 00",
        "bb bb bb bb aa aa aa aa"
    ),
    Test(
        "it pops a QWORD",
        "1F aa aa aa aa 1F bb bb bb bb 1F cc cc cc cc 20 00",
        "bb bb bb bb aa aa aa aa"
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles QWORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

