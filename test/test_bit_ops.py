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
]

if __name__=='__main__':
    vmtest.VmTests("It handles bit operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

"""
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),

    ### Or ###
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),

    ### Not ###
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
    Test(
        "It fails, in bit operations",
        "00",
        "to fail"
    ),
"""
