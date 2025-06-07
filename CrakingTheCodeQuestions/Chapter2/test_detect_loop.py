from linked_list import create_linked_list, linked_list_to_array, ListNode
from typing import Optional
import pytest

def detect_loop_start(head: ListNode) -> ListNode:
    slow, fast = head, head
    loop = False

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            loop = True
            break ## Theres a loop.
    
    if not loop:
        return None

    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow

@pytest.fixture
def create_looped_list(create_linked_list):
    """Fixture to create a linked list with a loop at a specified position"""
    def _create_looped_list(values: list[int], loop_start_index: int) -> ListNode:
        if not values:
            return None
            
        head = create_linked_list(values)
        if loop_start_index < 0 or loop_start_index >= len(values):
            return head
            
        # Find the node where the loop should start
        current = head
        for _ in range(loop_start_index):
            current = current.next
            
        # Find the last node
        last = head
        while last.next:
            last = last.next
            
        # Create the loop
        last.next = current
        return head
    return _create_looped_list

def test_no_loop(create_linked_list, linked_list_to_array):
    """Test a list with no loop"""
    head = create_linked_list([1, 2, 3, 4, 5])
    result = detect_loop_start(head)
    assert result is None

def test_loop_at_start(create_looped_list, linked_list_to_array):
    """Test a list with a loop starting at the first node"""
    head = create_looped_list([1, 2, 3, 4, 5], 0)
    result = detect_loop_start(head)
    assert result.val == 1

def test_loop_at_middle(create_looped_list, linked_list_to_array):
    """Test a list with a loop starting in the middle"""
    head = create_looped_list([1, 2, 3, 4, 5], 2)
    result = detect_loop_start(head)
    assert result.val == 3

def test_loop_at_end(create_looped_list, linked_list_to_array):
    """Test a list with a loop starting at the last node"""
    head = create_looped_list([1, 2, 3, 4, 5], 4)
    result = detect_loop_start(head)
    assert result.val == 5

def test_empty_list(create_linked_list):
    """Test an empty list"""
    head = None
    result = detect_loop_start(head)
    assert result is None

def test_single_node(create_linked_list):
    """Test a list with a single node"""
    head = create_linked_list([1])
    result = detect_loop_start(head)
    assert result is None

def test_single_node_loop(create_looped_list):
    """Test a list with a single node that points to itself"""
    head = create_looped_list([1], 0)
    result = detect_loop_start(head)
    assert result.val == 1

# Parametrized test for multiple scenarios
@pytest.mark.parametrize("values,loop_index,expected_value", [
    ([1, 2, 3, 4, 5], 0, 1),  # Loop at start
    ([1, 2, 3, 4, 5], 2, 3),  # Loop in middle
    ([1, 2, 3, 4, 5], 4, 5),  # Loop at end
    ([1, 2, 3], 1, 2),        # Small list, loop in middle
    ([1, 2], 0, 1),           # Two nodes, loop at start
    ([1, 2], 1, 2),           # Two nodes, loop at end
])
def test_multiple_scenarios(create_looped_list, values, loop_index, expected_value):
    """Test multiple scenarios using parametrize"""
    head = create_looped_list(values, loop_index)
    result = detect_loop_start(head)
    assert result.val == expected_value
