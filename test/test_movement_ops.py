from clitest import Test
import vmtest


tests = [
    ### Jumps ###
    Test(
        "It jumps some pushes",
        "01 aa 10 00 08 2E 01 bb 01 cc 00",
        "cc aa"
    ),
    Test(
        "It jump some pushes with an immediate address",
        "01 aa 2F 00 07 01 bb 01 cc 00",
        "cc aa"
    ),

    ### Branching ###
    Test(
        "It branches on true value",
        "01 01 30 00 09 01 aa 01 bb 01 cc 00",
        "cc"
    ),
    Test(
        "It continues on false value",
        "01 00 30 00 09 01 aa 01 bb 01 cc 00",
        "cc bb aa"
    ),

    ### CALL, ARG, and RET ###
    # Procs are started on a new line to make it a little easier to read
    Test(
        "It Calls a function to add two WORDs and return result",
        "01 05 01 04 31 02 00 09 00" \
        + "03 00 03 01 06 32 01 00",
        "09"
    ),
    # Remember args are passed in reverse order of declared params
    Test(
        "It Calls a function to do a - b with WORDs and return result",
        "01 05 01 04 31 02 00 09 00 03 00" \
        + "03 01 07 32 01 00",
        "ff"
    ),
    Test(
        "It does not remove stack elements before args",
        "10 aa aa 10 00 04 10 00 05 31 04 00 0e 00" \
        + "12 00 12 02 15 32 02 00",
        "00 09 aa aa"
    ),
    Test(
        "It does not return local function stack elements",
        "10 00 04 10 00 05 31 04 00 0b 00" \
        + "01 ff 12 00 12 02 15 32 02 00",
        "00 09"
    ),
    # Reverse a Qword and word on the stack
    Test(
        "It calls with different size args and return values",
        "1F aa bb cc dd 01 05 31 05 00 0c 00" \
        + "03 00 21 01 32 05 00",
        "aa bb cc dd 05"
    ),
    # important to confirm that ra and fp are being saved properly
    # as with a single function call they are not really needed
    # second proc doubles its arg
    # first proc calls second proc on its arg and adds one to result
    # Program calls first proc on a word and then subtracts 3 from the result
    Test(
        "It handles a nested function call",
        "01 05 31 01 00 0a 01 03 07 00" \
        + "03 00 31 01 00 16 01 01 06 32 01 00" \
        + "01 02 03 00 08 32 01 00 ",
        "08"
    ),

    ### Push Special Addresses ###
    # BP = fffc
    Test(
        "It pushes SP",
        "01 aa 33 01 bb 33 00",
        "ff f8 bb ff fb aa"
    ),
    Test(
        "It pushes FP",
        "34 00",
        "ff fc"
    ),
    Test(
        "It pushes PC",
        "35 01 aa 01 bb 35 00",
        "00 05 bb aa 00 00"
    ),
    Test(
        "It pushes RA",
        "36 00",
        "00 00"
    ),

    ### Free Mem ###
    Test(
        "It pushes program end pointer (PRG)",
        "52 00 00 00",
        "00 04"
    ),
    # Same as PRG if there has been no movement
    Test(
        "It pushes BRK",
        "53 00 00 00",
        "00 04"
    ),
    # BRK_ADD will push the inital brk and BRK will push the new value
    Test(
        "It pushes the address of brk and adds words to it",
        "10 00 05 54 53 00",
        "00 0b 00 06"
    ),
    # BRK_DROP will push the new value after the drop
    Test(
        "It pushes the address of brk and  words to it",
        "10 00 05 54 11 10 00 02 55 00",
        "00 0d"
    ),
    # Adding or Dropping too much returns 0xffff
    # 5 + fff8 is fffd which is in mem range, but past sp
    Test(
        "It returns 0xffff if BRK_ADD is too much, past sp",
        "10 ff f8 54 00",
        "ff ff"
    ),
    # 5 + fff5 is fffa which is in mem range, but is sp
    Test(
        "It returns 0xffff if BRK_ADD is too much, is sp",
        "10 ff f5 54 00",
        "ff ff"
    ),
    # 5 + ffff is 0004
    Test(
        "It returns 0xffff if BRK_ADD is too much, out of bounds",
        "10 ff ff 54 00",
        "ff ff"
    ),
    # 5 - 3 is still in mem range, but below prg
    Test(
        "It returns 0xffff if BRK_DROP is too much, below prg",
        "10 00 03 55 00",
        "ff ff"
    ),
    # 5 - 10 is fffb and wraps around out
    Test(
        "It returns 0xffff if BRK_DROP is too much, out of bounds",
        "10 00 0a 55 00",
        "ff ff"
    ),

    ### Blocks and scoping ###
    Test(
        "Create a new block and GET upper scope local var",
        "01 aa 5F 01 bb 65 01 00 00",
        "aa bb ff fc aa"
    ),
    Test(
        "Create a new block and GET_D upper scope local var",
        "10 aa bb 5F 01 cc 66 01 00 00",
        "aa bb cc ff fc aa bb"
    ),
    Test(
        "Create a new block and GET_Q upper scope local var",
        "1F aa bb cc dd 5F 01 ee 67 01 00 00",
        "aa bb cc dd ee ff fc aa bb cc dd"
    ),
    Test(
        "Create a new block and GET upper scope local var then END",
        "01 aa 5F 01 bb 65 01 00 60 00",
        "aa"
    ),
    Test(
        "Create a new block and get LOCAL var",
        "01 aa 5F 01 bb 01 cc 01 dd 62 01 00",
        "cc dd cc bb ff fc aa"
    ),
    Test(
        "Create a new block and get LOCAL_D var",
        "01 aa 5F 01 bb 10 cc ee 01 dd 63 01 00",
        "cc ee dd cc ee bb ff fc aa"
    ),
    Test(
        "Create a new block and get LOCAL_Q var",
        "01 aa 5F 01 bb 1F cc ee ff 22 01 dd 64 01 00",
        "cc ee ff 22 dd cc ee ff 22 bb ff fc aa"
    ),

]


if __name__=='__main__':
    vmtest.VmTests("It handles movement operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

