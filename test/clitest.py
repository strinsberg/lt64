import subprocess as sp

### Color Codes ###
NORMAL = "\033[0;39;49m"
RED = "\033[1;31;49m"
GREEN = "\033[1;32;49m"
YELLOW = "\033[1;33;49m"

### Functions ################################################################
def display_totals(failed, total, reprint_failed=True, show_fail_info=True):
    print()
    print()
    if len(failed):
        print(f"{RED}****{NORMAL} Failed Tests {RED}****{NORMAL}")
        print()
        if reprint_failed:
            for i, t in failed:
                display_test_results(t, False, i, show_fail_info)
    else:
        print(f"{GREEN}****{NORMAL} {total} Tests Passed {GREEN}****{NORMAL}")

def display_test_results(test, passed, num, show_fail_info=True):
    print(f"{f'{num}:':<3} {test.name:<60}", end="")
    if passed:
        print(f"[{GREEN}PASS{NORMAL}]")
    else:
        print(f"[{RED}FAIL{NORMAL}]")
        if show_fail_info and test.show_fail_info:
            if test.error:
                print(f"    {YELLOW}{test.error}{NORMAL}",
                      end="")
                print()
            print(f"    {GREEN}EXPECTED{NORMAL}: {test.expected}")
            print(f"    {RED}ACTUAL{NORMAL}:   {test.actual}")

def compile_program(command_list):
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
        print("base write")
        with open(self.program_source, 'w+') as f:
            f.write(test.input)

    def get_test_input(self, test):
        if self.input_is_file:
            with open(test.input, 'rb') as f:
                return f.read()
        else:
            return test.input().encode('utf-8')

    def check(self, test, proc):
        actual = self.get_actual(test, proc)
        expected = self.get_expected(test, proc)
        return actual == expected

    def get_actual(self, test, proc):
        if self.program_output != "stdout":
            with open(self.program_output, 'r'):
                test.actual = f.read().strip()
        else:
            test.actual = proc.stdout.decode('utf-8').strip()
        return test.actual

    def get_expected(self, test, proc):
        if self.expected_is_file:
            with open(test.expected, 'r'):
                test.expected = f.read().strip()
        else:
            test.expected = test.expected.strip()
        return test.expected

class Test:
    def __init__(self, name, input_, expected, show_fail_info=True):
        self.name = name
        self.input = input_
        self.expected = expected
        self.show_fail_info = show_fail_info
        self.actual = None
        self.stderr = None

