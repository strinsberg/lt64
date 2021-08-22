from clitest import Test
import vmtest

tests = [
    ### Stack Manipulation ###
    Test(
        "Push DWORDs",
        "10 aa aa 10 bb bb 10 cc cc 00",
        "cc cc bb bb aa aa"
    ),
    Test(
        "Pop a DWORD",
        "10 aa aa 10 bb bb 10 cc cc 11 00",
        "bb bb aa aa"
    ),
]

if __name__=='__main__':
    vmtest.VmTests("It handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()
