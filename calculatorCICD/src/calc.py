"""
Calculator module providing basic arithmetic operations.

This module contains functions for addition, subtraction, multiplication,
and division operations with proper type hints and error handling.
"""

from typing import Union

# Type alias for numbers (int or float)
Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    Add two numbers together.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        The sum of a and b

    Example:
        >>> add(2, 3)
        5
        >>> add(2.5, 1.5)
        4.0
    """
    return a + b


def sub(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first.

    Args:
        a: Number to subtract from
        b: Number to subtract

    Returns:
        The difference of a and b (a - b)

    Example:
        >>> sub(5, 2)
        3
        >>> sub(1.5, 0.5)
        1.0
    """
    return a - b


def mul(a: Number, b: Number) -> Number:
    """
    Multiply two numbers together.

    Args:
        a: First number to multiply
        b: Second number to multiply

    Returns:
        The product of a and b

    Example:
        >>> mul(3, 4)
        12
        >>> mul(2.5, 2)
        5.0
    """
    return a * b


def div(a: Number, b: Number) -> float:
    """
    Divide the first number by the second.

    Args:
        a: Number to be divided (dividend)
        b: Number to divide by (divisor)

    Returns:
        The quotient of a and b (a / b) as a float

    Raises:
        ZeroDivisionError: If b is zero

    Example:
        >>> div(8, 2)
        4.0
        >>> div(7, 2)
        3.5
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
