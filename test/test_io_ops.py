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

    ## Strings and Chars ##
    Test("It prints characters",
         "01 00  43 44  01 00  41 42  4B 00  4B 00  00 00",
         "AC"
    ),
    Test("It prints a string from the buffer",
         "01 00  41 42  58 01  01 00  43 44  58 02"
         + "4C 00  00 00",
         "ABCD"
    ),
    Test("It prints a string from the buffer with a new line",
         "01 00  41 42  58 01  01 00  43 44  58 02"
         + "4D 00  00 00",
         "ABCD\n"
    ),
    Test("It prints a string from memory",
         "01 00  41 42  01 00 00 00  04 00"
         + "01 00  43 44  01 00  01 00  04 00"
         + "01 00  00 00  01 00  02 00  04 00"
         + "01 00  00 00  4F 00  00 00",
         "ABCD"
    ),


]

read_tests = [
    ### Read Number Tests ###
    vmtest.IoTest(
        "It reads in a word sized negative int",
        "50 00  00 00",
        "-1",  # input
        "ffff"  # expected stack
    ),
    vmtest.IoTest(
        "It reads in a double word sized negative int",
        "51 00  00 00",
        "-1",
        "ffff ffff"
    ),
    vmtest.IoTest(
        "It reads in a fixed point number and default scales it",
        "52 00  00 00",
        "10.123",
        "0000 278b"
    ),
    vmtest.IoTest(
        "It reads in a fixed point number and user scales it",
        "53 02  00 00",
        "10.123",
        "0000 03f4"
    ),
    vmtest.IoTest(
        "It reads in a character",
        "54 00  54 00  00 00",
        "AB",
        "0041 0042"
    ),
    vmtest.IoTest(
        "It reads a string up to a space into the buffer.",
        "56 00  4C 00  00 00",
        "ABCD\n",
        "ABCD"
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


