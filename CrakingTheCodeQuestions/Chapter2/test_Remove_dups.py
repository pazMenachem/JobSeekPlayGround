import pytest
from typing import Optional
import collections

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

def remove_duplicates(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return None

    values = collections.defaultdict(lambda: 0)
    tmp = head

    while tmp:
        values[tmp.val] += 1
        tmp = tmp.next

    new_head = ListNode()
    tmp = new_head

    for key, value in values.items():
        if value > 1:
            continue
        else:
            tmp.next = ListNode(key)
            tmp = tmp.next

    return new_head.next

# Fixtures
@pytest.fixture
def create_linked_list():
    """Fixture to create a linked list from an array"""
    def _create_linked_list(arr: list[int]) -> Optional[ListNode]:
        if not arr:
            return None
        head = ListNode(arr[0])
        current = head
        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next
        return head
    return _create_linked_list

@pytest.fixture
def linked_list_to_array():
    """Fixture to convert linked list to array"""
    def _linked_list_to_array(head: Optional[ListNode]) -> list[int]:
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result
    return _linked_list_to_array

# Test Cases
def test_empty_list(create_linked_list, linked_list_to_array):
    """Test removing duplicates from an empty list"""
    head = None
    result = remove_duplicates(head)
    assert result is None

def test_single_node(create_linked_list, linked_list_to_array):
    """Test removing duplicates from a list with single node"""
    head = create_linked_list([1])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == [1]

def test_no_duplicates(create_linked_list, linked_list_to_array):
    """Test removing duplicates from a list with no duplicates"""
    head = create_linked_list([1, 2, 3, 4, 5])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == [1, 2, 3, 4, 5]

def test_all_duplicates(create_linked_list, linked_list_to_array):
    """Test removing duplicates from a list where all elements are duplicates"""
    head = create_linked_list([1, 1, 1, 1, 1])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == []

def test_duplicates_at_beginning(create_linked_list, linked_list_to_array):
    """Test removing duplicates at the beginning of the list"""
    head = create_linked_list([1, 1, 1, 2, 3, 4])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == [2, 3, 4]

def test_duplicates_at_end(create_linked_list, linked_list_to_array):
    """Test removing duplicates at the end of the list"""
    head = create_linked_list([1, 2, 3, 4, 4, 4])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == [1, 2, 3]

def test_duplicates_in_middle(create_linked_list, linked_list_to_array):
    """Test removing duplicates in the middle of the list"""
    head = create_linked_list([1, 2, 2, 2, 3, 4])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == [1, 3, 4]

def test_multiple_consecutive_duplicates(create_linked_list, linked_list_to_array):
    """Test removing multiple groups of consecutive duplicates"""
    head = create_linked_list([1, 1, 1, 2, 2, 2, 3, 3, 3])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == []

def test_scattered_duplicates(create_linked_list, linked_list_to_array):
    """Test removing duplicates scattered throughout the list"""
    head = create_linked_list([1, 2, 1, 3, 2, 4, 1])
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == [3, 4]

# Parametrized test for multiple scenarios
@pytest.mark.parametrize("input_list,expected", [
    ([], []),
    ([1], [1]),
    ([1, 2, 3], [1, 2, 3]),
    ([1, 1, 1], []),
    ([1, 2, 2, 3], [1, 3]),
    ([1, 1, 2, 2, 3, 3], []),
])
def test_multiple_scenarios(create_linked_list, linked_list_to_array, input_list, expected):
    """Test multiple scenarios using parametrize"""
    head = create_linked_list(input_list)
    result = remove_duplicates(head)
    assert linked_list_to_array(result) == expected