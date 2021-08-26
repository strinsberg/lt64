from clitest import Test
import vmtest

tests = [
    ### Stack Manipulation ###
    Test(
        "Push DWORDs",
        "10 aa bb 10 cc dd 10 ee ff 00",
        "ee ff cc dd aa bb"
    ),
    Test(
        "Pop a DWORD",
        "10 aa ee 10 bb ff 10 cc cc 11 00",
        "bb ff aa ee"
    ),

    ### Addition ###
    Test(
        "Add positive DWORDs",
        "10 08 00 10 07 00 15 00",
        "0f 00"
    ),
    Test(
        "Add positive and negative DWORDS",
        "10 ff 00 10 05 00 15 00",
        "04 00"
    ),

    ### Subtract ###
    Test(
        "Subract positive DWORDs",
        "10 00 07 10 00 08 16 00",
        "ff ff"
    ),
    Test(
        "Subract positive and negative DWORDS",
        "10 00 05 10 ff ff 16 00",
        "00 06"
    ),

    ### Multiply ###
    Test(
        "Multiply positive DWORDS",
        "10 00 08 10 00 07 17 00",
        "00 38"
    ),
    Test(
        "Multiply positive and negative DWORDS",  # fb is -5
        "10 00 05 10 ff fb 17 00",
        "ff e7"
    ),

    ### Divide ###
    Test(
        "Divide positive DWORDS",
        "10 00 38 10 00 07 18 00",
        "00 08"
    ),
    Test(
        "Divide positive and negative DWORDS",  # ff is -1
        "10 00 05 10 ff ff 18 00",
        "ff fb"
    ),
    Test(
        "Divide positive DWORDS small by large",
        "10 00 03 10 00 10 18 00",
        "00 00"
    ),
    Test(
        "Divide positive DWORDS with remainder",
        "10 00 38 10 00 03 18 00",
        "00 12"
    ),
    Test(
        "Divide UNsigned positive DWORDS",
        "10 00 38 10 00 08 19 00",
        "00 07"
    ),
    Test(
        "Divide UNsigned positive and would be negative DWORDS",
        "10 00 05 10 00 ff 19 00",
        "00 00"
    ),

    ### Equality ###
    Test(
        "Equal DWORDS success",
        "10 08 00 10 08 00 1A 00",
        "01"
    ),
    Test(
        "Equal DWORDS failure",  # fb is -5
        "10 00 05 10 00 fb 1A 00",
        "00"
    ),

    ### Less Than ###
    # Note that the order of the arguments has to change for signed to unsigned
    # as a large unsigned value is a negative signed value
    Test(
        "Less than DWORDS success",
        "10 ff ff 10 00 08 1B 00",
        "01"
    ),
    Test(
        "Less than DWORDS failure",
        "10 00 08 10 ff ff 1B 00",
        "00"
    ),
    Test(
        "Less than UNsigned DWORDS success",  # ff is 225
        "10 00 08 10 ff ff 1C 00",
        "01"
    ),
    Test(
        "Less than UNsigned DWORDS failure",  # ff is 225
        "10 ff ff 10 00 08 1C 00",
        "00"
    ),

    ### Greater Than ###
    Test(
        "Greater than DWORDS success",
        "10 00 08 10 ff ff 1D 00",
        "01"
    ),
    Test(
        "Greater than DWORDS failure",
        "10 ff ff 10 00 08 1D 00",
        "00"
    ),
    Test(
        "Greater than UNsigned DWORDS success",  # ff is 225
        "10 ff ff 10 00 08 1E 00",
        "01"
    ),
    Test(
        "Greater than UNsigned DWORDS failure",  # ff is 225
        "10 00 08 10 ff ff 1E 00",
        "00"
    ),
]

if __name__=='__main__':
    vmtest.VmTests("It handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()
