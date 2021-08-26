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

    ### Call and Ret ###

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
]


if __name__=='__main__':
    vmtest.VmTests("It handles movement operations",
                   vmtest.TEST_NAME,
                   tests=tests,
                   program_source=vmtest.INPUT_FILE,
                   compile_command=vmtest.COMPILE_FOR_TESTS).run()

