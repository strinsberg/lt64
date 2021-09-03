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
]


if __name__=='__main__':
    vmtest.VmTests("Handles WORD operations",
                   vmtest.EXEC_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()


    """
    Test(
        "Pop a WORD",
        "01 aa 01 bb 01 cc 02 00",
        "bb aa"
    ),

    ### Storage ###
    Test(
        "Load a word from the bottom of the stack.",
        "01 aa 01 bb 10 ff fb 04 00",
        "aa bb aa"
    ),
    Test(
        "Store a word on the bottom of the stack.",
        "01 aa 01 bb 01 cc 10 ff fb 05 00",
        "bb cc"
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
        "01 07 01 08 07 00",
        "ff"
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
"""
