import pytest

class MinStack:
    def __init__(self):
        self._min_array = list()
        self._stack = list()
    
    def pop(self) -> int:
        self._check_empty()

        value = self._stack.pop()
        if self._min_array[-1] == value:
            self._min_array.pop()
        return value
    
    def push(self, value: int) -> None:
        if not self._min_array:
            self._stack.append(value)
            self._min_array.append(value)
        else:
            if self._min_array and value <= self._min_array[-1]:
                self._min_array.append(value)
            self._stack.append(value)
        
    def min(self) -> int:
        self._check_empty()
        return self._min_array[-1]

    def _check_empty(self):
        if not self._stack:
            raise IndexError("Empty stack")


@pytest.fixture
def stack():
    """Fixture to provide a fresh MinStack instance for each test."""
    return MinStack()


def test_empty_stack_operations(stack):
    """Test operations on an empty stack."""
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.min()


def test_push_and_pop(stack):
    """Test basic push and pop operations."""
    stack.push(5)
    assert stack.pop() == 5
    
    # Test multiple pushes and pops
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_min_value(stack):
    """Test minimum value tracking."""
    # Test with descending values
    stack.push(5)
    stack.push(4)
    stack.push(3)
    assert stack.min() == 3
    
    # Test with ascending values
    stack = MinStack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.min() == 1


def test_min_value_after_pop(stack):
    """Test minimum value updates after pop operations."""
    stack.push(5)
    stack.push(3)
    stack.push(7)
    assert stack.min() == 3
    
    stack.pop()  # Remove 7
    assert stack.min() == 3
    
    stack.pop()  # Remove 3
    assert stack.min() == 5


def test_duplicate_min_values(stack):
    """Test handling of duplicate minimum values."""
    stack.push(5)
    stack.push(3)
    stack.push(3)
    assert stack.min() == 3
    
    stack.pop()  # Remove first 3
    assert stack.min() == 3
    
    stack.pop()  # Remove second 3
    assert stack.min() == 5


@pytest.mark.parametrize("values,expected_min", [
    ([5, 3, 7], 3),
    ([1, 2, 3], 1),
    ([3, 3, 3], 3),
    ([5, 3, 3, 7], 3),
])
def test_min_value_parameterized(stack, values, expected_min):
    """Parameterized test for minimum value tracking with different inputs."""
    for value in values:
        stack.push(value)
    assert stack.min() == expected_min
