from clitest import *

### Vars ###
TEST_NAME = "./lt64-test"
COMPILE_FOR_TESTS = ['gcc', 'main.c', '-o', 'lt64-test',
                     '-Og', '-D', 'TEST']

COMPILE_FOR_RELEASE_TESTS = ['gcc', 'main.c', '-o', 'lt64-release-test',
                             '-O3', '-D', 'TEST']
RELEASE_TEST_NAME = "./lt64-release-test"

INPUT_FILE = "test.vm"

### EXIT CODES ###
EXIT_MEM = 1;
EXIT_LEN = 2;
EXIT_FILE = 3;
EXIT_SOF = 4;
EXIT_SUF = 5;
EXIT_POB = 6;
EXIT_OP = 7;

### Test Classes ###
class VmTests(TestSuite):
    def write_program_input(self, test):
        data = bytes.fromhex(test.input.replace(" ", "").replace("\n", ""))
        with open(self.program_source, 'wb+') as f:
            f.write(data)

class VmErrorTests(VmTests):
    def get_actual(self, test, proc):
        test.actual = proc.returncode
        return proc.returncode

    def get_expected(self, test, proc):
        return test.expected

