"""
TestSuite and Test extensions specifically for testing the lieutenant-64
virtual machine.
"""
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
EXIT_STR = 8;
EXIT_ARGS = 9;
EXIT_RSOF = 10;
EXIT_RSUF = 11;

### Test Classes ###
class VmTests(TestSuite):
    """Test Suite specific to the running of the lieutenant-64 virtual machine.

    Overrides the write_program_input to allow tests to be written as hex
    strings with whitespace. This way the string can separate bytes or words
    and be much easier to read rather than just a long string of hex
    characters.
    """
    def write_program_input(self, test):
        """Converts the test's input into a byte string from a string of hex
        characters. First removes all spaces and newlines. Also writes the
        file in binary mode so that the hex is directly translated into bytes
        in the file and not into characters. The VM reads bytes not chars.
        """
        data = bytes.fromhex(test.input.replace(" ", "").replace("\n", ""))
        with open(self.program_source, 'wb+') as f:
            f.write(data)

class VmErrorTests(VmTests):
    """A test suite that allows testing error conditions in the VM.

    It treats expected and actual as error codes and not as program output.
    This way we can expect a specific error condition from the failing of
    the VM.
    """
    def check(self, test, proc):
        """Check to see that expected and actual match only. As mentioned these
        will be error codes not program output."""
        actual = self.get_actual(test, proc)
        expected = self.get_expected(test, proc)
        return actual == expected

    def get_actual(self, test, proc):
        """Return the process return code to compare as an exit code."""
        test.actual = proc.returncode
        return proc.returncode

    def get_expected(self, test, proc):
        """Return the expected value from the test. It will be an exit code."""
        return test.expected

# When initializing leave program_source=stdin
# This class will write to the file as normal AND send test.stdin to the program
# if the test has it.
class VmIoTests(VmTests):
    """Test suite specifically for testing VM operations that read from stdin.

    When initializing leave program_source=stdin.
    """

    def execute(self):
        """Execute the IO test by writing the tests input to the file that
        the VM will read. Then when running the process send the tests stdin
        member to the subprocess as program input during the VM execution.
        """
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
    """An IO specific test to add the member stdin to the test. This is data
    that will be sent to stdin during the VM run. This is necessary since the
    normal VM tests will just read progra instructions from the test file.
    However, read operations need input during the VM's exectution.
    """
    def __init__(self, name, input_, stdin, expected, show_fail_info=True):
        super().__init__(name, input_, expected, show_fail_info=show_fail_info)
        self.stdin = stdin

