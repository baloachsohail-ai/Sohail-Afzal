import unittest

from calculator import CalculatorError, calculate


class CalculatorTest(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calculate("2 + 3"), 5)
        self.assertEqual(calculate("10 - 4"), 6)
        self.assertEqual(calculate("6 * 7"), 42)
        self.assertEqual(calculate("9 / 2"), 4.5)
        self.assertEqual(calculate("9 // 2"), 4)
        self.assertEqual(calculate("9 % 2"), 1)

    def test_precedence_and_parentheses(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)
        self.assertEqual(calculate("(2 + 3) * 4"), 20)
        self.assertEqual(calculate("-3 + 5"), 2)

    def test_power(self):
        self.assertEqual(calculate("2 ** 10"), 1024)
        self.assertEqual(calculate("2 ^ 3"), 8)

    def test_functions_and_constants(self):
        self.assertEqual(calculate("sqrt(16)"), 4)
        self.assertAlmostEqual(calculate("cos(pi)"), -1)

    def test_variables(self):
        self.assertEqual(calculate("ans * 2", {"ans": 21}), 42)

    def test_errors(self):
        for expr in ["1 / 0", "2 +", "foo", "__import__('os')", "sqrt(-1)"]:
            with self.assertRaises(CalculatorError):
                calculate(expr)


if __name__ == "__main__":
    unittest.main()
