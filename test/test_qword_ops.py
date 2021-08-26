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
]


if __name__=='__main__':
    vmtest.VmTests("It handles QWORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

