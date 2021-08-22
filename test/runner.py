from clitest import *
import vmtest
import test_word_ops as word
import test_dword_ops as dword
import test_qword_ops as qword
import test_movement_ops as move
import test_errors as errors
import sys

if len(sys.argv) > 1 and sys.argv[1] == "release":
    prog_name = vmtest.RELEASE_TEST_NAME
    compile_command = vmtest.COMPILE_FOR_RELEASE_TESTS
else:
    prog_name = vmtest.TEST_NAME
    compile_command = vmtest.COMPILE_FOR_TESTS

suites = [
    vmtest.VmTests("It handles word ops",
                   prog_name,
                   tests=word.tests,
                   program_source=vmtest.INPUT_FILE),
    vmtest.VmTests("It handles dword ops",
                   prog_name,
                   tests=dword.tests,
                   program_source=vmtest.INPUT_FILE),
    vmtest.VmTests("It handles qword ops",
                   prog_name,
                   tests=qword.tests,
                   program_source=vmtest.INPUT_FILE),
    vmtest.VmTests("It handles movement ops",
                   prog_name,
                   tests=move.tests,
                   program_source=vmtest.INPUT_FILE),
    vmtest.VmErrorTests("It handles errors",
                        prog_name,
                        tests=errors.tests,
                        program_source=vmtest.INPUT_FILE),
]

compile_program(compile_command)
run_test_suites(suites)

