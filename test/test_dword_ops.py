from clitest import Test
import vmtest

tests = [
    ### Standard ops ###
    Test(
        "Push double words",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  00 00",
        "bbaa aabb ddcc ccdd"
    ),
    Test(
        "Pop double words",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  0E 00 00 00",
        "bbaa aabb"
    ),
    Test(
        "Load double words relative to top of memory",
        "01 00  00 00  0F 00  01 00  01 00  0F 00  00 00",
        "0000 0000 0000 0000"
    ),
    Test(
        "Store double words relative to top of memory",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  01 00  00 00  10 00"
        + "0E 00  01 00  00 00  0F 00  00 00",
        "ddcc ccdd"
    ),

    ### Manipulation ###
    Test(
        "Duplicate double stack top",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  11 00  00 00",
        "bbaa aabb ddcc ccdd ddcc ccdd"
    ),
    Test(
        "Duplicate double stack top - 2",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  12 00  00 00",
        "bbaa aabb ddcc ccdd bbaa aabb"
    ),
    Test(
        "Duplicate nth double element down from stack top",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  0D 00  ee ff ff ee"
        + "01 00  02 00  13 00  00 00",
        "bbaa aabb ddcc ccdd ffee eeff bbaa aabb"
    ),
    Test(
        "Swap the top two double stack elements",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  14 00  00 00",
        "ddcc ccdd bbaa aabb"
    ),
    Test(
        "Rotate 3rd stack (top - 5) double element to stack top",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc  0D 00  ee ff ff ee  15 00  00 00",
        "ddcc ccdd ffee eeff bbaa aabb"
    ),

    ## Return stack ##
    Test(
        "Push a double element onto return stack and get it back",
        "0D 00  aa bb bb aa  16 00  0D 00  cc dd dd cc  17 00  18 00  00 00",
        "ddcc ccdd bbaa aabb 0000 0000"
    ),
    Test(
        "Push a double element onto return stack and grab it twice",
        "0D 00  aa bb bb aa  16 00  0D 00  cc dd dd cc  18 00  17 00  18 00  00 00",
        "ddcc ccdd bbaa aabb bbaa aabb 0000 0000"
    ),

    ## Arithmetic ##
    Test(
        "Add the top two double stack elements",
        "0D 00  00 00  04 00  0D 00  00 00  05 00  2B 00  00 00",
        "0000 0009"
    ),
    Test(
        "Add the top two double stack elements, One is negative",
        "0D 00  00 00  04 00  0D 00  ff ff  fe ff  2B 00  00 00",
        "0000 0002"
    ),
    Test(
        "Subtract the top two double stack elements",
        "0D 00  00 00  04 00  0D 00  00 00  05 00  2C 00  00 00",
        "ffff ffff"
    ),
    Test(
        "Subtract the top two double stack elements, One is negative",
        "0D 00  00 00  04 00  0D 00  ff ff  fe ff  2C 00  00 00",
        "0000 0006"
    ),
    Test(
        "Multiply the top two double stack elements",
        "0D 00  00 00  04 00  0D 00  00 00  05 00  2D 00  00 00",
        "0000 0014"
    ),
    Test(
        "Multiply the top two double stack elements, One is negative",
        "0D 00  00 00  04 00  0D 00  ff ff  fe ff  2D 00  00 00",
        "ffff fff8"
    ),
    Test(
        "Divide the top two double stack elements",
        "0D 00  00 00  04 00  0D 00  00 00  02 00  2E 00  00 00",
        "0000 0002"
    ),
    Test(
        "Divide the top two double stack elements, One is negative",
        "0D 00  00 00  04 00  0D 00  ff ff  ff ff  2E 00  00 00",
        "ffff fffc"
    ),
    Test(
        "Mod the top two double stack elements",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  2F 00  00 00",
        "0000 0002"
    ),
    Test(
        "Mod the top two double stack elements, Bottom is negative",
        "0D 00  00 00  08 00  0D 00  ff ff  fd ff  2F 00  00 00",
        "0000 0002"
    ),
    Test(
        "Mod the top two double stack elements, Top is negative",
        "0D 00  ff ff  f8 ff  0D 00  00 00  03 00  2F 00  00 00",
        "ffff fffe"
    ),

    ## Comparisson ##
    Test(
        "Check the top two double stack elements for equality, Pass",
        "0D 00 00 00  08 00  0D 00  00 00  08 00  30 00  00 00",
        "0000 0001"
    ),
    Test(
        "Check the top two double stack elements for equality, Fail",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  30 00  00 00",
        "0000 0000"
    ),
    Test(
        "Check the top two double stack elements bottom < top, Pass",
        "0D 00  00 00  03 00  0D 00  00 00  08 00  31 00  00 00",
        "0000 0001"
    ),
    Test(
        "Check the top two double stack elements bottom < top, Fail",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  31 00  00 00",
        "0000 0000"
    ),
    Test(
        "Check the top two double stack elements bottom < top, One neg, Pass",
        "0D 00  ff ff  ff ff  0D 00  00 00  03 00  31 00  00 00",
        "0000 0001"
    ),
    Test(
        "Check the top two double stack elements bottom > top, Pass",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  32 00  00 00",
        "0000 0001"
    ),
    Test(
        "Check the top two double stack elements bottom > top, Fail",
        "0D 00  00 00  03 00  0D 00  00 00  08 00  32 00  00 00",
        "0000 0000"
    ),
    Test(
        "Check the top two double stack elements bottom > top, One neg, Pass",
        "0D 00  00 00  03 00  0D 00  ff ff  ff ff  32 00  00 00",
        "0000 0001"
    ),

    ## Unsigned Arithmetic and Comparison ##
    Test(
        "(Unsigned) Divide 2 double words on stack, large",
        "0D 00  00 00 E8 FD  0D 00  00 00  E8 03  34 00  00 00",
        "0000 0041"
    ),
    Test(
        "(Unsigned) Divide 2 double words on stack",
        "0D 00  00 00  00 7D  0D 00  00 00  E8 03  34 00  00 00",
        "0000 0020"
    ),
    Test(
        "(Unsigned) Mod the top two double stack elements",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  35 00  00 00",
        "0000 0002"
    ),
    Test(
        "(Unsigned) Mod the top two double stack elements, Bottom is large",
        "0D 00  00 00  08 00  0D 00  ff ff  fd ff  35 00  00 00",
        "0000 0008"
    ),
    Test(
        "(Unsigned) Mod the top two double stack elements, Top is large",
        "0D 00  ff ff  f8 ff  0D 00  00 00  03 00  35 00  00 00",
        "0000 0002"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, Pass",
        "0D 00  00 00  03 00  0D 00  00 00  08 00  36 00  00 00",
        "0000 0001"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, Fail",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  36 00  00 00",
        "0000 0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, large, Fail",
        "0D 00  ff ff  ff ff  0D 00  00 00  03 00  36 00  00 00",
        "0000 0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, Pass",
        "0D 00  00 00  08 00  0D 00  00 00  03 00  37 00  00 00",
        "0000 0001"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, Fail",
        "0D 00  00 00  03 00  0D 00  00 00  08 00  37 00  00 00",
        "0000 0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, large, Fail",
        "0D 00  00 00  03 00  0D 00  ff ff  ff ff  37 00  00 00",
        "0000 0000"
    ),

    ## Bits ##
    Test(
        "Left shift double word on top of the stack",
        "0D 00  00 00  02 00  38 02  38 01  00 00",
        "0000 0010"
    ),
    Test(
        "Left shift double word on top of the stack, negative",
        "0D 00  ff ff  fe ff  38 02  38 01  00 00",
        "ffff fff0"
    ),
    Test(
        "Right shift double word on top of the stack",
        "0D 00  00 00  10 00  39 02  39 01  00 00",
        "0000 0002"
    ),
    Test(
        "Right shift word on top of the stack, negative",
        "0D 00  ff ff f0 ff  39 02  39 01  00 00",
        "ffff fffe"
    ),
    Test(
        "Bitwise and the 2 double words on top of the stack",
        "0D 00  ff 00  ff 00  0D 00  00 ff  00 ff  3A 00  00 00",
        "0000 0000"
    ),
    Test(
        "Bitwise or the 2 double words on top of the stack",
        "0D 00  00 ff  00 ff  0D 00  ff 00  ff 00  3B 00  00 00",
        "ffff ffff"
    ),
    Test(
        "Bitwise not the double word on top of the stack",
        "0D 00  f0 f0 f0 f0  3C 00  00 00",
        "0f0f 0f0f"
    ),

]

if __name__=='__main__':
    vmtest.VmTests("It handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()


"""
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

    ### Storage ###
    Test(
        "Load a dword from the bottom of the stack.",
        "10 aa bb 10 cc dd 10 ff fa 13 00",
        "aa bb cc dd aa bb"
    ),
    Test(
        "Store a dword on the bottom of the stack.",
        "10 aa bb 10 cc dd 10 ee ff 10 ff fa 14 00",
        "cc dd ee ff"
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
"""
