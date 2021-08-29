from clitest import Test
import vmtest


tests = [
    ### Stack Manipulation ###
    Test(
        "it pushes QWORDs",
        "1F aa ee aa dd 1F bb cc bb ff 00",
        "bb cc bb ff aa ee aa dd"
    ),
    Test(
        "it pops a QWORD",
        "1F aa aa aa ff 1F bb bb bb ee 1F cc cc cc aa 20 00",
        "bb bb bb ee aa aa aa ff"
    ),

    ### Storage ###
    Test(
        "Load a qword from the bottom of the stack.",
        "1F aa bb aa bb 1F cc dd cc dd 10 ff f8 22 00",
        "aa bb aa bb cc dd cc dd aa bb aa bb"
    ),
    Test(
        "Store a qword on the bottom of the stack.",
        "1F aa bb aa bb 1F cc dd cc dd 1F ee ff ee ff 10 ff f8 23 00",
        "cc dd cc dd ee ff ee ff"
    ),

    ### Addition ###
    Test(
        "Add positive QWORD",
        "1F 00 00 00 08 1F 00 00 00 07 24 00",
        "00 00 00 0f"
    ),
    Test(
        "Add positive and negative QWORDS",
        "1F ff ff ff ff 1F 00 00 00 05 24 00",
        "00 00 00 04"
    ),

    ### Subtract ###
    Test(
        "Subract positive QWORD",
        "1F 00 00 00 07 1F 00 00 00 08 25 00",
        "ff ff ff ff"
    ),
    Test(
        "Subract positive and negative QWORDS",
        "1F 00 00 00 05 1F ff ff ff ff 25 00",
        "00 00 00 06"
    ),

    ### Multiply ###
    Test(
        "Multiply positive QWORDS",
        "1F 00 00 00 08 1F 00 00 00 07 26 00",
        "00 00 00 38"
    ),
    Test(
        "Multiply positive and negative QWORDS",  # fb is -5
        "1F 00 00 00 05 1F ff ff ff fb 26 00",
        "ff ff ff e7"
    ),

    ### Divide ###
    Test(
        "Divide positive QWORDS",
        "1F 00 00 00 38 1F 00 00 00 07 27 00",
        "00 00 00 08"
    ),
    Test(
        "Divide positive and negative QWORDS",  # ff is -1
        "1F 00 00 00 05 1F ff ff ff ff 27 00",
        "ff ff ff fb"
    ),
    Test(
        "Divide positive QWORDS small by large",
        "1F 00 00 00 03 1F 00 00 00 10 27 00",
        "00 00 00 00"
    ),
    Test(
        "Divide positive QWORDS with remainder",
        "1F 00 00 00 38 1F 00 00 00 03 27 00",
        "00 00 00 12"
    ),
    Test(
        "Divide UNsigned positive QWORDS",
        "1F 00 00 00 38 1F 00 00 00 08 28 00",
        "00 00 00 07"
    ),
    Test(
        "Divide UNsigned positive and would be negative QWORDS",
        "1F 00 00 00 05 1F ff ff ff ff 28 00",
        "00 00 00 00"
    ),

    ### Equality ###
    Test(
        "Equal QWORDS success",
        "1F 00 00 08 00 1F 00 00 08 00 29 00",
        "01"
    ),
    Test(
        "Equal QWORDS failure",  # fb is -5
        "1F 00 00 00 05 1F ff ff ff fb 29 00",
        "00"
    ),

    ### Less Than ###
    # Note that the order of the arguments has to change for signed to unsigned
    # as a large unsigned value is a negative signed value
    Test(
        "Less than QWORDS success",
        "1F ff ff ff ff 1F 00 00 00 08 2A 00",
        "01"
    ),
    Test(
        "Less than QWORDS failure",
        "1F 00 00 00 08 1F ff ff ff ff 2A 00",
        "00"
    ),
    Test(
        "Less than UNsigned QWORDS success",  # ff is 225
        "1F 00 00 00 08 1F ff ff ff ff 2B 00",
        "01"
    ),
    Test(
        "Less than UNsigned QWORDS failure",  # ff is 225
        "1F ff ff ff ff 1F 00 00 00 08 2B 00",
        "00"
    ),

    ### Greater Than ###
    Test(
        "Greater than QWORDS success",
        "1F 00 00 00 08 1F ff ff ff ff 2C 00",
        "01"
    ),
    Test(
        "Greater than QWORDS failure",
        "1F ff ff ff ff 1F 00 00 00 08 2C 00",
        "00"
    ),
    Test(
        "Greater than UNsigned QWORDS success",  # ff is 225
        "1F ff ff ff ff 1F 00 00 00 08 2D 00",
        "01"
    ),
    Test(
        "Greater than UNsigned QWORDS failure",  # ff is 225
        "1F 00 00 00 08 1F ff ff ff ff 2D 00",
        "00"
    ),

    ### Fixed point (All are signed) ###
    # Scale Factor of 1000 which makes the max number around (+/-) 2mill
    # storing it in 32 bits.
    # The arithmetic does not require new ops from all of them, but just to
    # keep it simple, and if things change, I will do all of them.
    Test(
        # a = 10.123, b = 10.456, ans = 20.579
        # a * 1000 as hex = 278b, b = 28d8, c = 5063
        "Add fixed point numbers",
        "1F 00 00 27 8b 1F 00 00 28 d8 56 00",
        "00 00 50 63"
    ),
    Test(
        # a = 10.123, b = 10.456, ans = -0.333
        "Subract fixed point numbers",
        "1F 00 00 27 8b 1F 00 00 28 d8 57 00",
        "ff ff fe b3"
    ),
    Test(
        # a = 10.123, b = 10.456, ans = 105.846
        # multiplication of binary nums must be divided by 1000 to keep at 3 digits
        "Multiply fixed point numbers",
        "1F 00 00 27 8b 1F 00 00 28 d8 58 00",
        "00 01 9d 76"
    ),
    Test(
        # a = 10.123, b = -5.234, ans = -1.934
        # division must be scaled to floats and divided, then scaled back
        "Division fixed point numbers, one negative",
        "1F 00 00 27 8b 1F ff ff eb 8e 59 00",
        "ff ff f8 72"
    ),
    Test(
        # a = 10.123, b = 10.456, ans = 0.968
        "Division fixed point numbers",
        "1F 00 00 27 8b 1F 00 00 28 d8 59 00",
        "00 00 03 c8"
    ),

    ### Fixed point comparisson ###
    Test(
        # a = 2000000.123, b = 2000000.123
        "Equality fixed point numbers, success",
        "1F 77 35 94 7b 1F 77 35 94 7b 5A 00",
        "01"
    ),
    Test(
        # a = 10.123, b = 10.456
        "Equality fixed point numbers, failure",
        "1F 00 00 27 8b 1F 00 00 28 d8 5A 00",
        "00"
    ),
    Test(
        # a = -5.235, b = 10.123
        "Less than fixed point, success",
        "1F ff ff eb 8e 1F 00 00 27 8b 5B 00",
        "01"
    ),
    Test(
        # a = 10.123, b = -5.234
        "Less than fixed point failure",
        "1F 00 00 27 8b 1F ff ff eb 8e 5B 00",
        "00"
    ),
    Test(
        # a = 10.123, b = -5.234
        "Greater than fixed point success",
        "1F 00 00 27 8b 1F ff ff eb 8e 5C 00",
        "01"
    ),
    Test(
        # a = -5.235, b = 10.123
        "Greater than fixed point, failure",
        "1F ff ff eb 8e 1F 00 00 27 8b 5C 00",
        "00"
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles QWORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

