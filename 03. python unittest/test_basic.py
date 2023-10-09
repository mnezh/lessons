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
