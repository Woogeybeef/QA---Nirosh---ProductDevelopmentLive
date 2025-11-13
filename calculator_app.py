import argparse

class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def get_sum(self):
        return self.a + self.b
    
    def get_difference(self):
        return self.a - self.b
    
    def get_product(self):
        return self.a * self.b
    
    def get_quotient(self):
        if self.b != 0:
            return self.a / self.b
        else:
            return "Cannot divide by zero"

# Set up command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Perform basic arithmetic operations")
    parser.add_argument('a', type=int, help="The first number")
    parser.add_argument('b', type=int, help="The second number")
    return parser.parse_args()

def main():
    # Parse arguments
    args = parse_arguments()

    # Create a Calculator instance with the passed arguments
    calc = Calculator(args.a, args.b)

    # Perform operations and print the results
    print(f"Sum: {calc.get_sum()}")
    print(f"Difference: {calc.get_difference()}")
    print(f"Product: {calc.get_product()}")
    print(f"Quotient: {calc.get_quotient()}")

if __name__ == "__main__":
    main()


