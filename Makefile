CC= gcc
CC_FLAGS = -o lt64 -O3
CC_DEBUG_FLAGS= -o lt64-debug -Og -D DEBUG

%.o: %.cpp
	$(CC) $(CC_FLAGS) -c $< -o $@

release: main.c
	$(CC) main.c $(CC_FLAGS)

debug: main.c
	$(CC) main.c $(CC_DEBUG_FLAGS)

.PHONY: tests
tests:
	python3 test/runner.py
	rm test.vm lt64-test

.PHONY: release-tests
release-tests:
	python3 test/runner.py release
	rm test.vm lt64-release-test

memcheck: lt64
	valgrind --leak-check=full ./lt64

.PHONY: clean
clean:
	rm -rf lt64 lt64-debug lt64-test lt64-release-test test.vm *.o *.out

