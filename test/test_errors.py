"""
Tests for double word operations on the lieutenant-64 virtual machine.

See the test_words.py file for some more information on how test input and
output is written.

The expected field is passed an integer exit code to compare to the one
returned by the VM when it exits on an error. For all VM errors there is a
constant in vmtest.py. Not all of them are tested because they are not all
easy to test with the given testing format.

See the lieutenant-64 README for more information on what each operation
does.
"""
from clitest import Test
import vmtest


tests = [
    Test(
        "Bad OP code",
        "99 00  00 00",
        vmtest.EXIT_OP
    ),
    Test(
        "Stack overflow",
        "01 00  aa aa  01 00  00 00  3D 00  00 00",
        vmtest.EXIT_SOF
    ),
    Test(
        "Stack underflow",
        "02 00  00 00",
        vmtest.EXIT_SUF
    ),
    Test(
        "Pc out of bounds",
        "01 00  aa aa  3D 00  00 00",
        vmtest.EXIT_POB
    ),
    Test(
        "Return stack overflow",
        "01 00  aa aa  0A 00  01 00  00 00  3D 00  00 00",
        vmtest.EXIT_RSOF
    ),
    Test(
        "Return stack underflow",
        "0B 00  00 00",
        vmtest.EXIT_RSUF
    ),
]

