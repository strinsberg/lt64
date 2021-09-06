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
        "Store and load double words relative to top of memory",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc"
        + "01 00  00 00  10 00  01 00  02 00  10 00"
        + "01 00  00 00  0F 00  01 00  02 00  0F 00  00 00",
        "ddcc ccdd bbaa aabb"
    ),
    Test(
        "Load double words from memory",
        "01 00  00 00  0F 01  01 00  02 00  0F 01  00 00",
        "0001 0000 010f 0001"
    ),
    Test(
        "Store double words in memory",
        "0D 00  aa bb bb aa  0D 00  cc dd dd cc"
        + "01 00  fe ff  10 01  01 00  fc ff  10 01"
        + "01 00  00 00  0F 00  01 00  02 00  0F 00  00 00",
        "ddcc ccdd bbaa aabb"
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
        "Left shift double word at top - 1 by top of the stack",
        "0D 00  00 00  02 00  01 00 03 00 38 00  00 00",
        "0000 0010"
    ),
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
        "0D 00  00 00  10 00  01 00  03 00  39 00  00 00",
        "0000 0002"
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

    ### Fixed point ###
    Test(
        "Multiply top two dwords as default scaled fixed point nums",
        "0D 00  00 00  50 15  0D 00  00 00  8b 27  60 00  00 00",
        "0000 d7bf"
    ),
    Test(
        "Multiply top two fwords with intermediate overflow handled",
        "0D 00  eb 0b  c8 c3  0D 00  00 00  8b 27  60 00  00 00",
        "78ad 03c8"
    ),
    Test(
        "Divide top two dwords as default scaled fixed point nums",
        "0D 00  00 00  8b 27  0D 00  00 00  50 15  61 00  00 00",
        "0000 073f"
    ),
    Test(
        "Divide top two dwords as default scaled fixed point nums, negative",
        "0D 00  ff ff  75 d8  0D 00  00 00  50 15  61 00  00 00",
        "ffff f8c1"
    ),
    Test(
        "Multiply top two dwords. User scaled fixed point nums",
        "0D 00  00 00  21 02  0D 00  00 00  f4 03  62 02  00 00",
        "0000 158b"
    ),
    Test(
        "Multiply top two user scaled fwords with intermediate overflow",
        "0D 00  eb 0b  2d c2  0D 00  00 00  f4 03  62 02  00 00",
        "78a3 cbc7"
    ),
    Test(
        "Divide top two dwords. User scaled fixed point nums",
        "0D 00  00 00  f4 03  0D 00  00 00  21 02  63 02  00 00",
        "0000 00b9"
    ),
    Test(
        "Divide top two dwords. User scaled fixed point nums, negative",
        "0D 00  ff ff  0c fc  0D 00  00 00  21 02  63 02  00 00",
        "ffff ff47"
    ),

]

if __name__=='__main__':
    vmtest.VmTests("It handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

