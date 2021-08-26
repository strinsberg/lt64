from clitest import Test
import vmtest


tests = [
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),

]

if __name__=='__main__':
    vmtest.VmTests("It handles bit operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()
