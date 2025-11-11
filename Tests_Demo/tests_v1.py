import unittest
from calculator_app import Calculator

class TestOperations (unittest,TestCase):

    def test_sum(self):
        calc = Calculator(2, 8)
        self.assertEqual(calc.get_sum(), 10, "Incorrect Sum")

if __name__ == "__main__"
    unittest.main()
    myCalc = Calculator(2,4)

    print(myCalc.get_product())