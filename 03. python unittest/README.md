# Unit testing basics with unittest python module

<!-- vscode-markdown-toc -->
* 1. [What is unit testing](#Whatisunittesting)
* 2. [What's in there](#Whatsinthere)
* 3. [Code under test](#Codeundertest)
* 4. [Testing code with a python script](#Testingcodewithapythonscript)
* 5. [unittest framework](#unittestframework)
	* 5.1. [Empty executable test file](#Emptyexecutabletestfile)
	* 5.2. [Using framework to implement actual tests](#Usingframeworktoimplementactualtests)
	* 5.3. [Data-driven tests](#Data-driventests)
	* 5.4. [Let unittest find the tests in many files](#Letunittestfindthetestsinmanyfiles)
	* 5.5. [Automating the routine with Makefile](#AutomatingtheroutinewithMakefile)
* 6. [The final code](#Thefinalcode)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

##  1. <a name='Whatisunittesting'></a>What is unit testing
Citing [Unit Testing – What is Its Importance in Software Testing?](https://www.testingxperts.com/blog/unit-testing):
> Unit Testing is the software testing technique where a group of software program components or modules are tested individually. This technique effectively helps in validating the accuracy of a section of code by considering stubs, mock objects, drivers, and unit testing frameworks. Since it is practiced at the initial testing phase, this testing technique assures to identify and fix the bugs at the early stage of SDLC even before they become expensive for the enterprises to fix when identified at a later stage.

##  2. <a name='Whatsinthere'></a>What's in there
* [divider.py](divider.py) - a trivial code to test
* [no_framework.py](no_framework.py) - test implementation without any framework
* [test_empty.py](test_empty.py) - minimal runnable test file
* [test_basic.py](test_basic.py) - basic implementation of test cases
* [test_data_driven.py](test_data_driven.py) - data-driven re-implementation of the test cases
* [test_data_driven_final.py](test_data_driven_final) - removing unessary parts
* [Makefile](Makefile) - test task automation

##  3. <a name='Codeundertest'></a>Code under test
Let's implement a trivial function we're going to test in a file `divider.py`:

```python
def divide(dividend, divisor):
    return dividend / divisor
```

We can think of many things we may want to check, let's list just a couple of *test cases*:
1. integer 4 divided by integer 2 gives us integer 2
2. floating point 4.0 divided by 2.0 gives us 2.0
3. division by zero gives us `ZeroDivisionError`
4. division by string value gives us `TypeError`
5. a false assumption: 4 divided by 2 gives us 1

##  4. <a name='Testingcodewithapythonscript'></a>Testing code with a python script
It is possible to test your code with just a plain python script. Let's create `no_framework.py` and implement the first *test case*:

```python
from divider import divide


if divider(4,2) != 2:
    raise Exception("4/2 should be 2!")
```

The same check could be written in one line using the [`assert`](https://www.w3schools.com/python/ref_keyword_assert.asp) python keyword:

```python
assert divider(4,2) == 2, "4/2 should be 2!"
assert divider(4.0,2.0) == 2.0, "4.0/2.0 should be 2.0!"
```

Let's check that expected exceptions are raised and write code for `ZeroDivisionError`, the code for TypeError would look the same:
```python
try:
    divide(4, 0)
except Exception as e:
    assert isinstance(e, ZeroDivisionError), f"Expected ZeroDivisionError, got {e}"
else:
    raise Exception("Expected ZeroDivisionError, got nothing")
```

And of course a failing test for false assumption:
```python
assert divider(4,2) == 1, "4/2 should be 1!"
```

Let's run the test:
```shell
$ python no_framework.py
Traceback (most recent call last):
  File "/Users/andrej.misustin/Gits/lessons/03. python unittest/no_framework.py", line 28, in <module>
    assert divide(4, 2) == 1, "4/2 should be 1!"
           ^^^^^^^^^^^^^^^^^
AssertionError: 4/2 should be 1!
```

Does the job, we can implement many things on a top of that, for the very least:
- reporting
- debug output

##  5. <a name='unittestframework'></a>unittest framework
Or instead we can use some framework, which does it for us. Python has a built-in framework, called [unittest](https://docs.python.org/3/library/unittest.html):

> The unittest unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing frameworks in other languages. It supports test automation, sharing of setup and shutdown code for tests, aggregation of tests into collections, and independence of the tests from the reporting framework.

###  5.1. <a name='Emptyexecutabletestfile'></a>Empty executable test file
Let's create an empty test file `test_empty.py`:

```python
import unittest

if __name__ == "__main__":
    unittest.TestProgram()
```

`unittest.TestProgram()` will look for the tests in our file and execute them (we have none), but also will provide a command line interface to control test execution. Let's see what we got:
```shell
python test_empty.py --help
usage: test_empty.py [-h] [-v] [-q] [--locals] [-f] [-c] [-b] [-k TESTNAMEPATTERNS] [tests ...]

positional arguments:
  tests                a list of any number of test modules, classes and test methods.

options:
  -h, --help           show this help message and exit
  -v, --verbose        Verbose output
  -q, --quiet          Quiet output
  --locals             Show local variables in tracebacks
  -f, --failfast       Stop on first fail or error
  -c, --catch          Catch Ctrl-C and display results so far
  -b, --buffer         Buffer stdout and stderr during tests
  -k TESTNAMEPATTERNS  Only run tests which match the given substring

Examples:
  test_empty.py                           - run default set of tests
  test_empty.py MyTestSuite               - run suite 'MyTestSuite'
  test_empty.py MyTestCase.testSomething  - run MyTestCase.testSomething
  test_empty.py MyTestCase                - run all 'test*' test methods
                                       in MyTestCase
```

Ok, now let's try to run the tests:
```shell
$ python test_empty.py

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
```
Pretty much what we expected: tried to find tests, found none, told us the summary.

###  5.2. <a name='Usingframeworktoimplementactualtests'></a>Using framework to implement actual tests
So let's implement the first test using the framework in `test_basic.py`:

```python
from divider import divide
import unittest


class BasicTest(unittest.TestCase):
    def test_divide_integers(self):
        self.assertEqual(divide(4, 2), 2)


if __name__ == "__main__":
    unittest.TestProgram()
```

The `unittest.TestCase` class provides [several assert methods](https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug) to check for and report failures, `assertEqual` is one of them.


Let's run the test:

```shell
$ python test_basic.py -v
test_divide_integers (__main__.BasicTest.test_divide_integers) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Tried to find the tests, found one, the test has passed.

Now let's try to implement different kind of test - expecting an exception. It is possible to [check the production of exceptions, warnings, and log messages](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertNotIsInstance) using the `unittest.TestCase` methods:

```python
class BasicTest(unittest.TestCase):
    def test_divide_integers(self):
        self.assertEqual(divide(4, 2), 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(4, 0)
```

```shell
$ python test_basic.py -v
test_divide_by_zero (__main__.BasicTest.test_divide_by_zero) ... ok
test_divide_integers (__main__.BasicTest.test_divide_integers) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s
```

Let's implement all five test cases:
```python
from divider import divide
import unittest


class BasicTest(unittest.TestCase):
    def test_divide_integers(self):
        self.assertEqual(divide(4, 2), 2)

    def test_divide_floats(self):
        self.assertEqual(divide(4.0, 2.0), 2.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(4, 0)

    def test_divide_by_string(self):
        with self.assertRaises(TypeError):
            divide(4, "zero")

    def test_failing(self):
        self.assertEqual(divide(4, 2), 1)


if __name__ == "__main__":
    unittest.TestProgram()
```

###  5.3. <a name='Data-driventests'></a>Data-driven tests
You've probably noticed that test case methods look like the copies of each other, except for the input and expected data. While it is OK for a limited number of test cases, if we would have 50 test cases instead of 5, that would be a lot of copy-pasting and expensive test maintenance. Since test cases only differ by data, let's separate test data from the actual test method:

```python
class DataDrivenTest(unittest.TestCase):
    data_cases = [
        ("divide integers", 4, 2, 2),
        ("failing test", 4, 2, 1),
        ("divide floats", 4.0, 2.0, 2.0),
    ]

    error_cases = [
        ("divide by zero", 4, 0, ZeroDivisionError),
        ("divide by string", 4, "zero", TypeError),
    ]

    def test_with_data(self):
        for case in self.data_cases:
            with self.subTest(case[0]):
                self.assertEqual(divide(case[1], case[2]), case[3])

    def test_errors(self):
        for case in self.error_cases:
            with self.subTest(case[0]):
                with self.assertRaises(case[3]):
                    divide(case[1], case[2])
```

Now we can implement extra test case by just defining another data line.

###  5.4. <a name='Letunittestfindthetestsinmanyfiles'></a>Let unittest find the tests in many files

Python `unittest` itself has a CLI, let's see what it can do:

```shell
$ python -m unittest --help
usage: python3.11 -m unittest [-h] [-v] [-q] [--locals] [-f] [-c] [-b] [-k TESTNAMEPATTERNS] [tests ...]

positional arguments:
  tests                a list of any number of test modules, classes and test methods.

options:
  -h, --help           show this help message and exit
  -v, --verbose        Verbose output
  -q, --quiet          Quiet output
  --locals             Show local variables in tracebacks
  -f, --failfast       Stop on first fail or error
  -c, --catch          Catch Ctrl-C and display results so far
  -b, --buffer         Buffer stdout and stderr during tests
  -k TESTNAMEPATTERNS  Only run tests which match the given substring

Examples:
  python3.11 -m unittest test_module               - run tests from test_module
  python3.11 -m unittest module.TestClass          - run tests from module.TestClass
  python3.11 -m unittest module.Class.test_method  - run specified test method
  python3.11 -m unittest path/to/test_file.py      - run tests from test_file.py

usage: python3.11 -m unittest discover [-h] [-v] [-q] [--locals] [-f] [-c] [-b] [-k TESTNAMEPATTERNS] [-s START] [-p PATTERN] [-t TOP]

options:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose output
  -q, --quiet           Quiet output
  --locals              Show local variables in tracebacks
  -f, --failfast        Stop on first fail or error
  -c, --catch           Catch Ctrl-C and display results so far
  -b, --buffer          Buffer stdout and stderr during tests
  -k TESTNAMEPATTERNS   Only run tests which match the given substring
  -s START, --start-directory START
                        Directory to start discovery ('.' default)
  -p PATTERN, --pattern PATTERN
                        Pattern to match tests ('test*.py' default)
  -t TOP, --top-level-directory TOP
                        Top level directory of project (defaults to start directory)

For test discovery all test modules must be importable from the top level directory of the project.
```

So `unittest` could discover your tests in multiple files, you don't have to call each test file one by one.
Let's run it:

```shell
$ python3 -m unittest -v
test_divide_by_string (test_basic.BasicTest.test_divide_by_string) ... ok
test_divide_by_zero (test_basic.BasicTest.test_divide_by_zero) ... ok
test_divide_floats (test_basic.BasicTest.test_divide_floats) ... ok
test_divide_integers (test_basic.BasicTest.test_divide_integers) ... ok
test_failing (test_basic.BasicTest.test_failing) ... FAIL
test_errors (test_data_driven.DataDrivenTest.test_errors) ... ok
test_with_data (test_data_driven.DataDrivenTest.test_with_data) ... 
  test_with_data (test_data_driven.DataDrivenTest.test_with_data) [failing test] ... FAIL

======================================================================
FAIL: test_failing (test_basic.BasicTest.test_failing)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/andrej.misustin/Gits/lessons/03. python unittest/test_basic.py", line 21, in test_failing
    self.assertEqual(divide(4, 2), 1)
AssertionError: 2.0 != 1

======================================================================
FAIL: test_with_data (test_data_driven.DataDrivenTest.test_with_data) [failing test]
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/andrej.misustin/Gits/lessons/03. python unittest/test_data_driven.py", line 20, in test_with_data
    self.assertEqual(divide(case[1], case[2]), case[3])
AssertionError: 2.0 != 1

----------------------------------------------------------------------
Ran 7 tests in 0.000s

FAILED (failures=2)
```

As you can see, the framework found both of our test files and executed all tests defined there. If we're using `python3 -m unittest` command, we can skip the unittest invocation in our test files:
```python
 ̶i̶f̶ ̶_̶_̶n̶a̶m̶e̶_̶_̶ ̶=̶=̶ ̶"̶_̶_̶m̶a̶i̶n̶_̶_̶"̶:̶
̶ ̶ ̶ ̶ ̶u̶n̶i̶t̶t̶e̶s̶t̶.̶T̶e̶s̶t̶P̶r̶o̶g̶r̶a̶m̶(̶)̶
```

###  5.5. <a name='AutomatingtheroutinewithMakefile'></a>Automating the routine with Makefile

Let's add a trivial `Makefile` to automate test running:
```make
.PHONY: test
test:
	python -m unittest -v
```

##  6. <a name='Thefinalcode'></a>The final code

1. The code under test in [divider.py](divider.py):

```python
def divide(dividend, divisor):
    return dividend / divisor
```

2. The test in [test_data_driven_final.py](test_data_driven_final.py):

```python
from divider import divide
import unittest


class DataDrivenTest(unittest.TestCase):
    data_cases = [
        ("divide integers", 4, 2, 2),
        ("failing test", 4, 2, 1),
        ("divide floats", 4.0, 2.0, 2.0),
    ]

    error_cases = [
        ("divide by zero", 4, 0, ZeroDivisionError),
        ("divide by string", 4, "zero", TypeError),
    ]

    def test_with_data(self):
        for case in self.data_cases:
            with self.subTest(case[0]):
                self.assertEqual(divide(case[1], case[2]), case[3])

    def test_errors(self):
        for case in self.error_cases:
            with self.subTest(case[0]):
                with self.assertRaises(case[3]):
                    divide(case[1], case[2])

```

3. Task automation in [Makefile](Makefile):

```make
.PHONY: test
test:
	python -m unittest -v
```
