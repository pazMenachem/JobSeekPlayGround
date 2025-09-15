"""
Main entry point for the calculatorCICD application.

This module demonstrates the calculator functions with sample operations.
"""

from calc import add, sub, mul, div


def main() -> None:
    """
    Demonstrate calculator functionality with sample operations.

    Prints the results of basic arithmetic operations to show
    that the calculator functions are working correctly.
    """
    print("calculatorCICD ready.")
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", sub(5, 2))
    print("3 * 4 =", mul(3, 4))
    print("8 / 2 =", div(8, 2))

    # Demonstrate error handling
    try:
        print("Attempting to divide by zero...")
        result = div(10, 0)
        print("Result:", result)  # This won't execute
    except ZeroDivisionError as e:
        print(f"Error caught: {e}")


if __name__ == "__main__":
    main()
