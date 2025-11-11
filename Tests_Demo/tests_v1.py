import unittest
from calculator_app import Calculator

class TestOperations(unittest.TestCase):

    def setup(self):        
        self.calc = Calculator(8,2)

    def test_sum(self):
        self.assertEqual(self.calc.get_sum(), 10, "Incorrect Sum")

    def test_product(self):
        self.assertEqual(self.calc.get_product(), 16, "Incorrect Product")

    def test_quotient(self):
        self.assertEqual(self.calc.get_quotient(), 4, "Incorrect Quotient")

    def test_difference(self):
        self.assertEqual(self.calc.get_difference(), 6, "Incorrect Difference")    
    
if __name__ == "__main__":
    unittest.main()

