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
