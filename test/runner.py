"""
Test runner for the lieutenant-64 virtual machine.

Assembles and runs all test suites and their tests. Calling
`python3 runner.py` will execute all tests for the VM. The only thing it
requires is that the lt64-test binary has been created. To both create the
binary and run the tests and clean up afterward run `make tests`.

For more information on the tests see the individual test files.
"""
from clitest import *
import vmtest
import test_word_ops as word
import test_dword_ops as dword
import test_movement_ops as move
import test_io_ops as io
import test_errors as errors
import sys

def make_vm_suite(name, tests, prog_name):
    """Helper to more easily create a VmTests object."""
    return vmtest.VmTests(name,
                          prog_name,
                          tests=tests,
                          program_source=vmtest.INPUT_FILE)

# The name of the program under test
prog_name = vmtest.TEST_NAME

# The various test suites to use to test the VM
suites = [
    make_vm_suite("Handles word ops", word.tests, prog_name),
    make_vm_suite("Handles dword ops", dword.tests, prog_name),
    make_vm_suite("Handles movement ops", move.tests, prog_name),
    make_vm_suite("Handles print ops", io.tests, prog_name),
    vmtest.VmIoTests("Handles read ops",
                     prog_name,
                     tests=io.read_tests,
                     program_source=vmtest.INPUT_FILE),
    vmtest.VmErrorTests("Handles errors",
                        prog_name,
                        tests=errors.tests,
                        program_source=vmtest.INPUT_FILE),
]

# Execute each given test suite
run_test_suites(suites)

