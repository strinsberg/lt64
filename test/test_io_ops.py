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

    ### Print Char, String, Hex ###
    Test("It prints a char and a newline char",
         "01 0D 01 40 3D 02 02 00",
         "@\n"
    ),
    Test("It prints a string",
         "01 00 01 65 01 76 01 65 01 74 01 53 33 3E 02 02 02 02 02 02 00",
         "Steve"
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles I/O operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()


