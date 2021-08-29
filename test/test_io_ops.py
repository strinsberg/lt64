from clitest import Test
import vmtest


tests = [
    ### Print Numbers ###
    Test("It prints a word as a signed int",
         "01 ff 37 02 00",
         "-1"
    ),
    Test("It prints a word as an unsigned int",
         "01 ff 38 02 00",
         "255"
    ),
    Test("It prints a dword as a signed int",
         "10 ff ff 39 11 00",
         "-1"
    ),
    Test("It prints a dword as an unsigned int",
         "10 ff ff 3A 11 00",
         "65535"
    ),
    Test("It prints a qword as a signed int",
         "1F ff ff ff ff 3B 20 00",
         "-1"
    ),
    Test("It prints a qword as an unsigned int",
         "1F ff ff ff ff 3C 20 00",
         "4294967295"
    ),
    Test("It prints a fixed point as float, positive",
         "1F 00 00 27 8b 5D 20 00",
         "10.123"
    ),
    Test("It prints a fixed point as float, negative",
         "1F ff ff eb 8e 5D 20 00",
         "-5.234"
    ),

    ### Print Char, String, Hex ###
    Test("It prints a char and a newline char",
         "01 0A 01 40 3D 02 02 00",
         "@\n"
    ),
    Test("It prints a string",
         "01 00 01 65 01 76 01 65 01 74 01 53 33 3E 02 02 02 02 02 02 00",
         "Steve"
    ),

]

read_tests = [
    ### Read Number Tests ###
    vmtest.IoTest(
        "It reads in a word sized negative int",
        "3F 00",
        "-1",  # input
        "ff"  # expected stack
    ),
    vmtest.IoTest(
        "It reads in a word sized positive int",
        "3F 00",
        "125",
        "7d"
    ),
    vmtest.IoTest(
        "It reads in a word sized int that would wrap around",
        "3F 00",
        "255",
        "ff"
    ),
    vmtest.IoTest(
        "It reads in a dword sized negative int",
        "40 00",
        "-1",  # input
        "ff ff"  # expected stack
    ),
    vmtest.IoTest(
        "It reads in a dword sized positive int",
        "40 00",
        "32000",
        "7d 00"
    ),
    vmtest.IoTest(
        "It reads in a dword sized int that would wrap around",
        "40 00",
        "65535",
        "ff ff"
    ),
    vmtest.IoTest(
        "It reads in a qword sized negative int",
        "41 00",
        "-1",  # input
        "ff ff ff ff"  # expected stack
    ),
    vmtest.IoTest(
        "It reads in a qword sized positive int",
        "41 00",
        "2000000000",
        "77 35 94 00"
    ),
    vmtest.IoTest(
        "It reads in a qword sized int that would wrap around",
        "41 00",
        "4294967295",
        "ff ff ff ff"
    ),
    vmtest.IoTest(
        "It reads in a fixed point, positive (truncate)",
        "5E 00",
        "10.123999",
        "00 00 27 8b"
    ),
    vmtest.IoTest(
        "It reads in a fixed point, negative",
        "5E 00",
        "-5.234",
        "ff ff eb 8e"
    ),
    # It will wrap around as n * 1000 % 2**32
    vmtest.IoTest(
        "It reads in a fixed point, positive (wraps around)",
        "5E 00",
        "8000000.123",
        "dc d6 50 7b"
    ),

    ### Read Chars and Strings ###
    vmtest.IoTest(
        "It reads a string onto the stack",
        "42 00",
        "Steve\n",
        "53 74 65 76 65 00"
    ),
    vmtest.IoTest(
        "It reads a string onto the stack when it is not empty",
        "01 aa 01 bb 42 01 cc 00",
        "Steve\n",
        "cc 53 74 65 76 65 00 bb aa"
    ),
    vmtest.IoTest("It reads and prints a string",
         "42 33 3E 02 02 02 02 02 02 00",
         "Steve\n",
         "Steve"
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


