from clitest import *
import vmtest
import test_word_ops as word
import test_dword_ops as dword
import test_movement_ops as move
import test_io_ops as io
import test_bit_ops as bits
import test_errors as errors
import sys

def make_vm_suite(name, tests, prog_name):
    return vmtest.VmTests(name,
                          prog_name,
                          tests=tests,
                          program_source=vmtest.INPUT_FILE)

prog_name = vmtest.TEST_NAME

suites = [
    make_vm_suite("Handles word ops", word.tests, prog_name),
    make_vm_suite("Handles dword ops", dword.tests, prog_name),
    #make_vm_suite("Handles qword ops", qword.tests, prog_name),
    make_vm_suite("Handles movement ops", move.tests, prog_name),
    #make_vm_suite("Handles print ops", io.tests, prog_name),
    #make_vm_suite("Handles bit ops", bits.tests, prog_name),
    #vmtest.VmIoTests("Handles read ops",
                        #prog_name,
                        #tests=io.read_tests,
                        #program_source=vmtest.INPUT_FILE),
    vmtest.VmErrorTests("Handles errors",
                        prog_name,
                        tests=errors.tests,
                        program_source=vmtest.INPUT_FILE),
]

run_test_suites(suites)

