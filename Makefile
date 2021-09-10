CC= gcc
CC_FLAGS = -I include
CC_RELEASE_FLAGS = -o lt64 -O3
CC_DEBUG_FLAGS= -o lt64-debug -Og -D DEBUG
CC_TEST_FLAGS= -o lt64-test -Og -D TEST

%.o: %.cpp
	$(CC) $(CC_FLAGS) -c $< -o $@

.PHONY: release
release: src/main.c
	$(CC) src/* $(CC_FLAGS) $(CC_RELEASE_FLAGS)

.PHONY: debug
debug: src/main.c
	$(CC) src/* $(CC_FLAGS) $(CC_DEBUG_FLAGS)

.PHONY: tests
tests: src/main.c
	$(CC) src/* $(CC_FLAGS) $(CC_TEST_FLAGS)
	python3 test/runner.py
	rm test.vm lt64-test

.PHONY: clean
clean:
	rm -rf lt64 lt64-debug lt64-test lt64-release-test test.vm *.o *.out

