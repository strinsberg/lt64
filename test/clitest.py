"""
TestSuite and Test objects and some helper functions for running simple tests
on command line programs.

Tries to do a lot and not too much while providing simple clean output for
test results. Uses ansi color codes to color the output. This will make test
output hard to read on terminals that do not support them.

Lots of different kind of tests that feed a command line program some input and
expect some output can be run with these tools. However, it is likely that some
things will need to be adjusted. The test suite has been written with a lot of
small methods that are called by other methods. This gives it a bit of a
template pattern to replace any little peice as needed. This may be to read
input or output differently or to perform a different check to determine
success or failure or to add new data and operations while keeping the same
general pattern. The helper functions are also separate and not TestSuite
methods to allow their use in different ways without always subclassing
TestSuite. To see some project specific uses see the lieutenant-64 repository.

TODO Make this it's own project and repo. Then add some examples of how it
could be used to test certain kinds of program and maybe some simple extensions
to cover common use cases not covered by the base class.
"""
import subprocess as sp

### Exit codes ###
EXIT_SUCCESS = 0

### Color Codes ###
NORMAL = "\033[0;39;49m"
RED = "\033[1;31;49m"
GREEN = "\033[1;32;49m"
YELLOW = "\033[1;33;49m"

### Functions ################################################################
def display_totals(failed, total, reprint_failed=True, show_fail_info=True):
    """Display the results of a test run to stdout.

    failed is a list of failed Test objects. If there are any failed tests,
    and reprint_failed is true, they will have their individual results
    printed with all their info. If show_fail_info is false then the short
    output for each failed test result will be reprinted.

    total is the number of tests that were run.
    """
    print()
    print()
    if len(failed):
        print(f"{RED}****{NORMAL} Failed Test Results {RED}****{NORMAL}")
        print()
        if reprint_failed:
            for i, t in failed:
                display_test_results(t, False, i, show_fail_info)
        print(f"{YELLOW}Tests Failed{NORMAL}: {len(failed)}")
        print()
    else:
        print(f"{GREEN}****{NORMAL} {total} Tests Passed {GREEN}****{NORMAL}")

def display_test_results(test, passed, num, show_fail_info=True):
    """Displays a line with the test name and whether it passed or failed.

    If show_fail_info is true more detailed output will be given with any error
    text and exit code followed by the expected output and the actual output.

    num is the number of the test in it's test suite and will be printed before
    the test name.
    """
    print(f"{f'{num}:':<3} {test.name:<70}", end="")
    if passed:
        print(f"[{GREEN}PASS{NORMAL}]")
    else:
        print(f"[{RED}FAIL{NORMAL}]")
        if show_fail_info and test.show_fail_info:
            if test.error:
                print(f"{YELLOW}{test.error}{NORMAL}",
                      end="")
                print(f"Exit Code: {test.exit_code}")
                print()
            print(f"{GREEN}EXPECTED{NORMAL}: {test.expected}")
            print(f"{RED}ACTUAL{NORMAL}:   {test.actual}")
            print()

def compile_program(command_list):
    """Given a list of the compilation command and it's arguments will run
    a subprocess to compile a program.

    Captures error output and the exit code and prints them to stderr if the
    compilation fails.

    Retruns True on successful compilation and False otherwise.
    """
    command = " ".join(command_list)
    print(f"Compiling: {command}")
    comp = sp.run(command_list, capture_output=True)
    if comp.returncode != 0:
        print(f"Error: Failed to compile: {command}")
        print(f"Exit Code: {comp.returncode}")
        print()
        print(comp.stderr.decode('utf-8'))
        return False
    return True

def run_test_suites(test_suites):
    """Runs each test suite in a list of tests suites.

    Sets all test output for the running of the tests to False so that only
    the test names and results are printed during the run of each suite.
    At the end reprints each failed test with all of it's verbose info."""
    failed = []
    total = 0
    for suite in test_suites:
        suite.show_fail_info = False
        suite.print_end_info = False
        suite.reprint_failed = False
        suite.run()
        total += len(suite.tests)
        failed.extend(suite.failed)

    display_totals(failed, total)

### Test classes #############################################################

# TODO implement behaviour for show_line_diff=True
class TestSuite:
    """A collection of tests for a command line program that will be run
    as a group.

    Takes a test suite name, a command for the command line program to run for
    each test, and a list of tests.

    The input to the program defaults to stdin, but program_source can be
    passed a file name to read the input to pass to the program under test's
    subprocess. In a similar way program output can specify where to expect
    the actual output. If it is stdout the programs output will be read from
    stdout. If it is a filename that file will be read instead.

    input_is_file tells the test suite that the program under test expects to
    read from a file instead of being given input. If this is true then
    program source must be set as the filename and any program input will be
    written to that file so the program under test can use it to get test
    input.

    expected_is_file tells the test suite that the expected output needs to be
    read from a file. This might be handy if the expected output is very large
    and it is impractical to specify it in a string when creating the Test
    object.
    
    print_end_info will tell the suite that when it is finished running it
    should display some information about the run of the suite. If this is
    true and reprint_failed is true then each failed test will be reprinted
    after the tests have all finished running.

    show_fail_info specifies that when a test fails a verbose output of
    failure information should be printed. This might contain error information
    and will always contain the expected output vs the actual output.

    show_line_diff(unimplemented) is indended to give a view of the difference
    between the expected and actual instead of printing them completely.
    However it has not been setup yet.
    """
    def __init__(self, name, command,
                 tests=[], compile_command=None,
                 program_source="stdin", program_output="stdout",
                 input_is_file=False, expected_is_file=False,
                 show_line_diff=False, show_fail_info=True,
                 print_end_info=True, reprint_failed=True):
        self.name = name
        self.command = command
        self.tests=tests
        self.compile_command = compile_command
        self.program_source = program_source
        self.program_output = program_output
        self.input_is_file = input_is_file
        self.expected_is_file = expected_is_file
        self.show_line_diff = show_line_diff
        self.show_fail_info = show_fail_info
        self.print_end_info = print_end_info
        self.reprint_failed = reprint_failed
        self.failed=[]

    def run(self):
        """Runs each test in order and displays the results for each run
        and the totals if print_end_info is true.
        """
        print()
        print(f"======== {self.name} ========")
        if self.compile_command:
            if not compile_program(self.compile_command):
                return
        self.execute()

        if self.print_end_info:
            display_totals(self.failed, len(self.tests),
                           self.reprint_failed, self.show_fail_info)

    def execute(self):
        """Executes each test and prints the individual test info
        according to the printing flags that are set."""
        for i, t in enumerate(self.tests):
            if self.program_source != "stdin":
                self.write_program_input(t)
                proc = sp.run(self.command, capture_output=True)
            else:
                send = self.get_test_input(t)
                proc = sp.run(self.command, input=send, capture_output=True)

            t.error = proc.stderr.decode('utf-8')
            passed = self.check(t, proc)
            display_test_results(t, passed, i+1, self.show_fail_info)

            if not passed:
                self.failed.append((i+1, t))

    def write_program_input(self, test):
        """Writes a test's program input to a file so that it can be read
        by the program under test. Can be overridden if a specific Test type
        might need a different output type. I.e. writing a binary file."""
        with open(self.program_source, 'w+') as f:
            f.write(test.input)

    def get_test_input(self, test):
        """Returns the test input. If the test expects input from a file it
        will be read in and returned. Otherwise the test input will be
        returned as a byte string. The reason for this is that Subprocess.run
        expects program input as a byte string. It can also be overriden if
        getting or creating the test input from a test is more complex. I.e.
        test input is given as a hex string and needs to be converted to the
        appropriate representation before being returned as a byte string."""
        if self.input_is_file:
            with open(test.input, 'rb') as f:
                return f.read()
        else:
            return test.input().encode('utf-8')

    def check(self, test, proc):
        """Checks to see if the process result output matches the expected
        output. To pass a test must have matching expected and actual
        output as well as return 0 for the exit code."""
        actual = self.get_actual(test, proc)
        expected = self.get_expected(test, proc)
        test.exit_code = proc.returncode
        return actual == expected and test.exit_code == EXIT_SUCCESS

    def get_actual(self, test, proc):
        """Returns the string of actual output after stripping whitespace
        from the ends. If the output is expected to be in a file it reads it
        from, otherwise the output captured to stdout by the process run is
        returned as a utf-8 string. Can be overriden to provide different
        behaviour such as returning an ascii string."""
        if self.program_output != "stdout":
            with open(self.program_output, 'r'):
                test.actual = f.read().strip()
        else:
            test.actual = proc.stdout.decode('utf-8').strip()
        return test.actual

    def get_expected(self, test, proc):
        """Retrns the string of expected output. As get_actual it will read
        from a file or from the test's expected propery. Strips all leading
        and trailing whitespace. Can be also be overriden."""
        if self.expected_is_file:
            with open(test.expected, 'r'):
                test.expected = f.read().strip()
        else:
            test.expected = test.expected.strip()
        return test.expected

class Test:
    """A simple data object for a test used to test the running of
    a cli program.

    name is the name that will be printed when showing test results.

    input_ and expected are strings for data to pass to the program
    under test and what to compare its output to.

    show_fail_info tells display functions whether or not to show detailed
    information on test failure.

    members actual, stderr, and exit_code are provided to add information to
    a test after running it to save for processes that may need it but run
    in a different place than where the test was executed."""
    def __init__(self, name, input_, expected, show_fail_info=True):
        self.name = name
        self.input = input_
        self.expected = expected
        self.show_fail_info = show_fail_info
        self.actual = None
        self.stderr = None
        self.exit_code = EXIT_SUCCESS

