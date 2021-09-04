from clitest import Test
import vmtest

# NOTE default fixed point printing always prints 3 decimal places. User
# suplied scaling prints the C default for lf which should be 6.

tests = [
    ### Print Numbers ###
    Test("It prints a word as a signed int",
         "01 00  ff ff  45 00  00 00",
         "-1"
    ),
    Test("It prints a double word as a signed int",
         "0D 00  ff ff  ff ff  46 00  00 00",
         "-1"
    ),
    Test("(Unsigned) It prints a word",
         "01 00  ff ff  47 00  00 00",
         "65535"
    ),
    Test("(Unsigned) It prints a double word",
         "0D 00  ff ff  ff ff  48 00  00 00",
         "4294967295"
    ),
    Test("It prints a fixed point number with default 1000 scaling",
         "0D 00  00 00  8B 27  49 00  00 00",
         "10.123"
    ),
    Test("It prints a fixed point number with given scaling",
         "0D 00  12 00  A6 D6  4A 02  00 00",
         "12345.98"
    ),

]

read_tests = [
    ### Read Number Tests ###
    vmtest.IoTest(
        "It reads in a word sized negative int",
        "4F 00",
        "-1",  # input
        "ffff"  # expected stack
    ),
]

if __name__=='__main__':
    vmtest.VmTests("It handles print operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()
    vmtest.VmIoTests("It handles read operations",
                      vmtest.TEST_NAME,
                      tests=read_tests,
                      program_source=vmtest.INPUT_FILE,
                      compile_command=vmtest.COMPILE_FOR_TESTS).run()


