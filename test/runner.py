from clitest import *
import vmtest
import test_word_ops as word
import test_dword_ops as dword
import test_qword_ops as qword
import test_movement_ops as move
import test_io_ops as io
import test_errors as errors
import sys

def make_vm_suite(name, tests):
    return vmtest.VmTests(name,
                          prog_name,
                          tests=tests,
                          program_source=vmtest.INPUT_FILE)


if len(sys.argv) > 1 and sys.argv[1] == "release":
    prog_name = vmtest.RELEASE_TEST_NAME
    compile_command = vmtest.COMPILE_FOR_RELEASE_TESTS
else:
    prog_name = vmtest.TEST_NAME
    compile_command = vmtest.COMPILE_FOR_TESTS


suites = [
    make_vm_suite("It handles word ops", word.tests),
    make_vm_suite("It handles dword ops", dword.tests),
    make_vm_suite("It handles qword ops", qword.tests),
    make_vm_suite("It handles movement ops", move.tests),
    make_vm_suite("It handles print ops", io.tests),
    vmtest.VmIoTests("It handles io ops",
                        prog_name,
                        tests=io.read_tests,
                        program_source=vmtest.INPUT_FILE),
    vmtest.VmErrorTests("It handles errors",
                        prog_name,
                        tests=errors.tests,
                        program_source=vmtest.INPUT_FILE),
]

compile_program(compile_command)
run_test_suites(suites)

