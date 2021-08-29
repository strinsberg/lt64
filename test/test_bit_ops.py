from clitest import Test
import vmtest


tests = [
    ### Shift Left ###
    Test(
        "It shifts a word 1 bit to the left",
        "01 01 43 01 00",
        "02"
    ),
    Test(
        "It shifts a word 8 bits to the left, past end",
        "01 01 43 08 00",
        "00"
    ),
    Test(
        "It shifts a dword 8 bits to the left",
        "10 00 01 45 08 00",
        "01 00"
    ),
    Test(
        "It shifts a dword 16 bits to the left",
        "1F 00 00 00 01 47 10 00",
        "00 01 00 00"
    ),

    ### Shift Right ###
    Test(
        "It shifts a word 1 bit to the right",
        "01 02 44 01 00",
        "01"
    ),
    Test(
        "It shifts a word 2 bits to the left, past end",
        "01 02 44 02 00",
        "00"
    ),
    Test(
        "It shifts a dword 8 bits to the right",
        "10 01 00 46 08 00",
        "00 01"
    ),
    Test(
        "It shifts a dword 16 bits to the right",
        "1F 00 01 00 00 48 10 00",
        "00 00 00 01"
    ),

    ### And ###
    Test(
        "It and for a word",
        "01 03 01 06 49 00",
        "02"
    ),
    Test(
        "It and for a dword",
        "10 ff ff 10 00 ff 4A 00",
        "00 ff"
    ),
    Test(
        "It and for a qword",
        "1F ff ff ff ff 1F 00 00 ff ff 4B 00",
        "00 00 ff ff"
    ),

    ### And ###
    Test(
        "It or for a word",
        "01 03 01 06 4C 00",
        "07"
    ),
    Test(
        "It or for a dword",
        "10 0f 0f 10 f0 f0 4D 00",
        "ff ff"
    ),
    Test(
        "It or for a qword",
        "1F f0 f0 f0 f0 1F 0f 0f 0f 0f 4E 00",
        "ff ff ff ff"
    ),

    ### And ###
    Test(
        "It not for a word",
        "01 f0 4F 00",
        "0f"
    ),
    Test(
        "It or for a dword",
        "10 0f 0f 50 00",
        "f0 f0"
    ),
    Test(
        "It or for a qword",
        "1F f0 f0 f0 f0 51 00",
        "0f 0f 0f 0f"
    ),
]

if __name__=='__main__':
    vmtest.VmTests("It handles bit operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

