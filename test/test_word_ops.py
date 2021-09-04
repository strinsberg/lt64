from clitest import Test
import vmtest

# NOTE the little endian order of each 16 bit word. 2 spaces are used
# to separate each word and 1 to separate the bytes since their order is
# backward we don't want them connected or it is confusing (more so)

# NOTE stack output is now  bottom -> top

# NOTE load and store use addresses that are relative to the top of memory
# and move down. So you need to address them 0, 1, 2, etc.

# NOTE nth is 0 based, even though it is a little awkward with fst and sec

tests = [
    ### Standard ops ###
    Test(
        "Push words",
        "01 00  bb aa  01 00  dd cc  00 00",
        "aabb ccdd"
    ),
    Test(
        "Pop words",
        "01 00  bb aa  01 00  dd cc  02 00 00 00",
        "aabb"
    ),
    Test(
        "Load words relative to top of memory",
        "01 00  00 00  03 00  01 00  01 00  03 00  00 00",
        "0000 0000"
    ),
    Test(
        "Store words relative to top of memory",
        "01 00 bb aa 01 00 dd cc  01 00  00 00  04 00"
        + "02 00  01 00  00 00  03 00  00 00",
        "ccdd"
    ),

    ### Manipulation ###
    Test(
        "Duplicate stack top",
        "01 00  bb aa  01 00  dd cc  05 00  00 00",
        "aabb ccdd ccdd"
    ),
    Test(
        "Duplicate stack top - 1",
        "01 00  bb aa  01 00  dd cc  06 00  00 00",
        "aabb ccdd aabb"
    ),
    Test(
        "Duplicate nth element down from stack top",
        "01 00  bb aa  01 00  dd cc  01 00  ff ee"
        + "01 00  02 00  07 00  00 00",
        "aabb ccdd eeff aabb"
    ),
    Test(
        "Swap the top two stack elements",
        "01 00  bb aa  01 00  dd cc  08 00  00 00",
        "ccdd aabb"
    ),
    Test(
        "Rotate 3rd stack (top - 2) element to stack top",
        "01 00  bb aa  01 00  dd cc  01 00  ff ee  09 00  00 00",
        "ccdd eeff aabb"
    ),

    ## Return stack ##
    Test(
        "Push an element onto return stack and get it back",
        "01 00  bb aa  0A 00  01 00  dd cc  0B 00  0C 00  00 00",
        "ccdd aabb 0000"
    ),
    Test(
        "Push an element onto return stack and grab it twice",
        "01 00  bb aa  0A 00  01 00  dd cc  0C 00  0B 00  0C 00  00 00",
        "ccdd aabb aabb 0000"
    ),

    ## Arithmetic ##
    Test(
        "Add the top two stack elements",
        "01 00  04 00  01 00  05 00  19 00  00 00",
        "0009"
    ),
    Test(
        "Add the top two stack elements, One is negative",
        "01 00  04 00  01 00  fe ff  19 00  00 00",
        "0002"
    ),
    Test(
        "Subtract the top two stack elements",
        "01 00  04 00  01 00  05 00  1A 00  00 00",
        "ffff"
    ),
    Test(
        "Subtract the top two stack elements, One is negative",
        "01 00  04 00  01 00  fe ff  1A 00  00 00",
        "0006"
    ),
    Test(
        "Multiply the top two stack elements",
        "01 00  04 00  01 00  05 00  1B 00  00 00",
        "0014"
    ),
    Test(
        "Multiply the top two stack elements, One is negative",
        "01 00  04 00  01 00  fe ff  1B 00  00 00",
        "fff8"
    ),
    Test(
        "Divide the top two stack elements",
        "01 00  0A 00  01 00  05 00  1C 00  00 00",
        "0002"
    ),
    Test(
        "Divide the top two stack elements, One is negative",
        "01 00  04 00  01 00  ff ff  1C 00  00 00",
        "fffc"
    ),
    Test(
        "Mod the top two stack elements",
        "01 00  08 00  01 00  03 00  1D 00  00 00",
        "0002"
    ),
    Test(
        "Mod the top two stack elements, Bottom is negative",
        "01 00  08 00  01 00  fd ff  1D 00  00 00",
        "0002"
    ),
    Test(
        "Mod the top two stack elements, Top is negative",
        "01 00 f8 ff  01 00  03 00  1D 00  00 00",
        "fffe"
    ),

    ## Comparisson ##
    Test(
        "Check the top two stack elements for equality, Pass",
        "01 00  08 00  01 00  08 00  1E 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements for equality, Fail",
        "01 00  08 00  01 00  03 00  1E 00  00 00",
        "0000"
    ),
    Test(
        "Check the top two stack elements bottom < top, Pass",
        "01 00  03 00  01 00  08 00  1F 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements bottom < top, Fail",
        "01 00  08 00  01 00  03 00  1F 00  00 00",
        "0000"
    ),
    Test(
        "Check the top two stack elements bottom < top, One neg, Pass",
        "01 00  ff ff  01 00  03 00  1F 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements bottom > top, Pass",
        "01 00  08 00  01 00  03 00  20 00  00 00",
        "0001"
    ),
    Test(
        "Check the top two stack elements bottom > top, Fail",
        "01 00  03 00  01 00  08 00  20 00  00 00",
        "0000"
    ),
    Test(
        "Check the top two stack elements bottom > top, One neg, Pass",
        "01 00  03 00  01 00  ff ff  20 00  00 00",
        "0001"
    ),

    ## Unsigned Arithmetic and Comparisson ##
    Test(
        "(Unsigned) Multiply 2 words and store as double word, large",
        "01 00  E8 FD  01 00  E8 03  21 00  00 00",
        "03df d240"
    ),
    Test(
        "(Unsigned) Multiply 2 words and store as double word",
        "01 00  00 7D  01 00  E8 03  21 00  00 00",
        "01e8 4800"
    ),
    Test(
        "(Unsigned) Divide 2 words on stack, large",
        "01 00  E8 FD  01 00  E8 03  22 00  00 00",
        "0041"
    ),
    Test(
        "(Unsigned) Divide 2 words on stack",
        "01 00  00 7D  01 00  E8 03  22 00  00 00",
        "0020"
    ),
    Test(
        "(Unsigned) Mod the top two stack elements",
        "01 00  08 00  01 00  03 00  23 00  00 00",
        "0002"
    ),
    Test(
        "(Unsigned) Mod the top two stack elements, Bottom is large",
        "01 00  08 00  01 00  fd ff  23 00  00 00",
        "0008"
    ),
    Test(
        "(Unsigned) Mod the top two stack elements, Top is large",
        "01 00 f8 ff  01 00  03 00  23 00  00 00",
        "0002"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, Pass",
        "01 00  03 00  01 00  08 00  24 00  00 00",
        "0001"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, Fail",
        "01 00  08 00  01 00  03 00  24 00  00 00",
        "0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom < top, large, Fail",
        "01 00  ff ff  01 00  03 00  24 00  00 00",
        "0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, Pass",
        "01 00  08 00  01 00  03 00  25 00  00 00",
        "0001"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, Fail",
        "01 00  03 00  01 00  08 00  25 00  00 00",
        "0000"
    ),
    Test(
        "(Unsigned) Check the top two stack elements bottom > top, large, Fail",
        "01 00  03 00  01 00  ff ff  25 00  00 00",
        "0000"
    ),

    ## Bits ##
    Test(
        "Left shift word on top of the stack",
        "01 00  02 00  26 01  26 01  00 00",
        "0008"
    ),
    Test(
        "Left shift word on top of the stack, negative",
        "01 00  fe ff  26 01  26 01  00 00",
        "fff8"
    ),
    Test(
        "Right shift word on top of the stack",
        "01 00  08 00  27 01  27 01  00 00",
        "0002"
    ),
    Test(
        "Right shift word on top of the stack, negative",
        "01 00  f8 ff  27 01  27 01  00 00",
        "fffe"
    ),
    Test(
        "Bitwise and the 2 words on top of the stack",
        "01 00  ff 00  01 00  00 ff  28 00  00 00",
        "0000"
    ),
    Test(
        "Bitwise or the 2 words on top of the stack",
        "01 00  00 ff  01 00  ff 00  29 00  00 00",
        "ffff"
    ),
    Test(
        "Bitwise not the word on top of the stack",
        "01 00  f0 f0  2A 00  00 00",
        "0f0f"
    ),

]


if __name__=='__main__':
    vmtest.VmTests("Handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

