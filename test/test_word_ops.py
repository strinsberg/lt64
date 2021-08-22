from clitest import Test
import vmtest

tests = [
    ### Stack Manipulation ###
    Test(
        "Push WORDs",
        "01 aa 01 bb 00",
        "bb aa"
    ),
    Test(
        "Pop a WORD",
        "01 aa 01 bb 01 cc 02 00",
        "bb aa"
    ),

    ### Addition ###
    Test(
        "Add positive WORDs",
        "01 08 01 07 06 00",
        "0f"
    ),
    Test(
        "Add positive and negative WORDs",  # ff is -1
        "01 ff 01 05 06 00",
        "04"
    ),

    ### Subtract ###
    Test(
        "Subract positive WORDs",
        "01 08 01 07 07 00",
        "01"
    ),
    Test(
        "Subract positive and negative WORDs",  # ff is -1
        "01 05 01 ff 07 00",
        "06"
    ),

    ### Multiply ###
    Test(
        "Multiply positive WORDs",
        "01 08 01 07 08 00",
        "38"
    ),
    Test(
        "Multiply positive and negative WORDs",  # fb is -5
        "01 05 01 fb 08 00",
        "e7"
    ),

    ### Divide ###
    Test(
        "Divide positive WORDs",
        "01 38 01 07 09 00",
        "08"
    ),
    Test(
        "Divide positive and negative WORDs",  # ff is -1
        "01 05 01 ff 09 00",
        "fb"
    ),
    Test(
        "Divide positive WORDs small by large",
        "01 03 01 10 09 00",
        "00"
    ),
    Test(
        "Divide positive WORDs with remainder",
        "01 38 01 03 09 00",
        "12"
    ),
    Test(
        "Divide UNsigned positive WORDs",
        "01 38 01 08 0A 00",
        "07"
    ),
    Test(
        "Divide UNsigned positive and negative WORDs",  # ff is -1
        "01 05 01 ff 0A 00",
        "00"
    ),

    ### Equality ###
    Test(
        "Equal WORDs success",
        "01 08 01 08 0B 00",
        "01"
    ),
    Test(
        "Equal WORDs failure",  # fb is -5
        "01 05 01 fb 0B 00",
        "00"
    ),

    ### Less Than ###
    # Note that the order of the arguments has to change for signed to unsigned
    # as a large unsigned value is a negative signed value
    Test(
        "Less than WORDs success",
        "01 ff 01 08 0C 00",
        "01"
    ),
    Test(
        "Less than WORDs failure",
        "01 08 01 ff 0C 00",
        "00"
    ),
    Test(
        "Less than UNsigned WORDs success",  # ff is 225
        "01 08 01 ff 0D 00",
        "01"
    ),
    Test(
        "Less than UNsigned WORDs failure",  # ff is 225
        "01 ff 01 08 0D 00",
        "00"
    ),

    ### Greater Than ###
    Test(
        "Greater than WORDs success",
        "01 08 01 ff 0E 00",
        "01"
    ),
    Test(
        "Greater than WORDs failure",
        "01 ff 01 08 0E 00",
        "00"
    ),
    Test(
        "Greater than UNsigned WORDs success",  # ff is 225
        "01 ff 01 08 0F 00",
        "01"
    ),
    Test(
        "Greater than UNsigned WORDs failure",  # ff is 225
        "01 08 01 ff 0F 00",
        "00"
    ),
]


if __name__=='__main__':
    vmtest.VmTests("It handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

