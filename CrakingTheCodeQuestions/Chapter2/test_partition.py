from linked_list import create_linked_list, linked_list_to_array, ListNode
from typing import Optional
import pytest

def partition(head: Optional[ListNode], value: int) -> Optional[ListNode]:
    if not head:
        return None
    
    lower, higher = head, head

    while higher:
        if higher.val < value:
            lower.val, higher.val = higher.val, lower.val
            lower = lower.next
        higher = higher.next
    return head

# Test Cases
def test_empty_list(create_linked_list, linked_list_to_array):
    """Test partitioning an empty list"""
    head = None
    result = partition(head, 5)
    assert result is None

def test_single_node(create_linked_list, linked_list_to_array):
    """Test partitioning a list with single node"""
    head = create_linked_list([3])
    result = partition(head, 5)
    assert linked_list_to_array(result) == [3]

def test_all_nodes_less_than_value(create_linked_list, linked_list_to_array):
    """Test when all nodes are less than partition value"""
    head = create_linked_list([1, 2, 3, 4])
    result = partition(head, 5)
    assert linked_list_to_array(result) == [1, 2, 3, 4]

def test_all_nodes_greater_than_value(create_linked_list, linked_list_to_array):
    """Test when all nodes are greater than partition value"""
    head = create_linked_list([6, 7, 8, 9])
    result = partition(head, 5)
    assert linked_list_to_array(result) == [6, 7, 8, 9]

def test_mixed_values(create_linked_list, linked_list_to_array):
    """Test with mixed values around partition value"""
    head = create_linked_list([3, 5, 8, 5, 10, 2, 1])
    result = partition(head, 5)
    # Verify that all values less than 5 come before values >= 5
    array_result = linked_list_to_array(result)
    partition_index = next((i for i, x in enumerate(array_result) if x >= 5), len(array_result))
    assert all(x < 5 for x in array_result[:partition_index])
    assert all(x >= 5 for x in array_result[partition_index:])

def test_partition_value_not_in_list(create_linked_list, linked_list_to_array):
    """Test when partition value is not in the list"""
    head = create_linked_list([1, 4, 3, 2, 5, 2])
    result = partition(head, 3)
    array_result = linked_list_to_array(result)
    partition_index = next((i for i, x in enumerate(array_result) if x >= 3), len(array_result))
    assert all(x < 3 for x in array_result[:partition_index])
    assert all(x >= 3 for x in array_result[partition_index:])

def test_duplicate_values(create_linked_list, linked_list_to_array):
    """Test with duplicate values including partition value"""
    head = create_linked_list([3, 3, 3, 1, 2, 3, 4, 5])
    result = partition(head, 3)
    array_result = linked_list_to_array(result)
    partition_index = next((i for i, x in enumerate(array_result) if x >= 3), len(array_result))
    assert all(x < 3 for x in array_result[:partition_index])
    assert all(x >= 3 for x in array_result[partition_index:])

# Parametrized test for multiple scenarios
@pytest.mark.parametrize("input_list,partition_value,expected_less_than,expected_greater_equal", [
    ([1, 4, 3, 2, 5, 2], 3, [1, 2, 2], [4, 5, 3]),
    ([3, 5, 8, 5, 10, 2, 1], 5, [3, 2, 1], [5, 10, 5, 8]),
    ([1, 2, 3], 2, [1], [2, 3]),
    ([3, 2, 1], 2, [1], [2, 3]),
])
def test_multiple_scenarios(create_linked_list, linked_list_to_array, input_list, partition_value, expected_less_than, expected_greater_equal):
    """Test multiple scenarios using parametrize"""
    head = create_linked_list(input_list)
    result = partition(head, partition_value)
    array_result = linked_list_to_array(result)
    
    # Find the partition point
    partition_index = next((i for i, x in enumerate(array_result) if x >= partition_value), len(array_result))
    
    # Verify the partition
    assert array_result[:partition_index] == expected_less_than
    assert array_result[partition_index:] == expected_greater_equal