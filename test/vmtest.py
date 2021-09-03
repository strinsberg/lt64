from clitest import *

### Vars ###
TEST_NAME = "./lt64-test"
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
    def check(self, test, proc):
        actual = self.get_actual(test, proc)
        expected = self.get_expected(test, proc)
        return actual == expected

    def get_actual(self, test, proc):
        test.actual = proc.returncode
        return proc.returncode

    def get_expected(self, test, proc):
        return test.expected

# When initializing leave program_source=stdin
# This class will write to the file as normal AND send test.stdin to the program
# if the test has it.
class VmIoTests(VmTests):
    def execute(self):
        for i, t in enumerate(self.tests):
            self.write_program_input(t)
            send = t.stdin.encode('utf-8')
            proc = sp.run(self.command, input=send, capture_output=True)

            t.error = proc.stderr.decode('utf-8')
            passed = self.check(t, proc)
            display_test_results(t, passed, i+1, self.show_fail_info)

            if not passed:
                self.failed.append((i+1, t))

class IoTest(Test):
    def __init__(self, name, input_, stdin, expected, show_fail_info=True):
        super().__init__(name, input_, expected, show_fail_info=show_fail_info)
        self.stdin = stdin

