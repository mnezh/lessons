#######
# not using testing framework for testing:
# - tests your code anyways
# - no reporting
# - if a test fails, the following would not be executed

from divider import divide

# trivial integer division
assert divide(4, 2) == 2, "4/2 should be 2!"
# trivial floating point division
assert divide(4.0, 2) == 2.0, "4.0/2.0 should be 2.0!"

try:
    divide(4, 0)
except Exception as e:
    assert isinstance(e, ZeroDivisionError), f"Expected ZeroDivisionError, got {e}"
else:
    raise Exception("Expected ZeroDivisionError, got nothing")

try:
    divide(4, "zero")
except Exception as e:
    assert isinstance(e, TypeError), f"Expected TypeError, got {e}"
else:
    raise Exception("Expected TypeError, got nothing")

assert divide(4, 2) == 1, "4/2 should be 1!"
