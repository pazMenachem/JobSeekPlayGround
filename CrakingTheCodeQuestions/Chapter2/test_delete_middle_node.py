from linked_list import create_linked_list, linked_list_to_array, ListNode
from typing import Optional
import pytest

def delete_middle_node(node: Optional[ListNode]):
    """Deletes a node from the middle of a linked list by copying values
    
    Args:
        node: The node to delete (not the last node)
    """
    while node.next.next:
        node.val = node.next.val
        node = node.next
    
    node.val = node.next.val
    node.next = None

# Test Cases
def test_delete_second_node(create_linked_list, linked_list_to_array):
    """Test deleting the second node in a list of 3 nodes"""
    head = create_linked_list([1, 2, 3])
    node_to_delete = head.next
    delete_middle_node(node_to_delete)
    assert linked_list_to_array(head) == [1, 3]

def test_delete_middle_node(create_linked_list, linked_list_to_array):
    """Test deleting a node in the middle of a longer list"""
    head = create_linked_list([1, 2, 3, 4, 5, 6, 7])
    node_to_delete = head.next.next.next  # node with value 4
    delete_middle_node(node_to_delete)
    assert linked_list_to_array(head) == [1, 2, 3, 5, 6, 7]

def test_delete_second_to_last_node(create_linked_list, linked_list_to_array):
    """Test deleting the second to last node"""
    head = create_linked_list([1, 2, 3, 4, 5])
    node_to_delete = head.next.next.next  # node with value 4
    delete_middle_node(node_to_delete)
    assert linked_list_to_array(head) == [1, 2, 3, 5]

def test_delete_third_node(create_linked_list, linked_list_to_array):
    """Test deleting the third node in a list of 4 nodes"""
    head = create_linked_list([1, 2, 3, 4])
    node_to_delete = head.next.next  # node with value 3
    delete_middle_node(node_to_delete)
    assert linked_list_to_array(head) == [1, 2, 4]

def test_delete_node_in_long_list(create_linked_list, linked_list_to_array):
    """Test deleting a node in a longer list"""
    head = create_linked_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    node_to_delete = head.next.next.next.next  # node with value 5
    delete_middle_node(node_to_delete)
    assert linked_list_to_array(head) == [1, 2, 3, 4, 6, 7, 8, 9, 10]

# Parametrized test for multiple scenarios
@pytest.mark.parametrize("input_list,node_index,expected", [
    ([1, 2, 3], 1, [1, 3]),           # Delete second node
    ([1, 2, 3, 4], 1, [1, 3, 4]),     # Delete second node
    ([1, 2, 3, 4], 2, [1, 2, 4]),     # Delete third node
    ([1, 2, 3, 4, 5], 2, [1, 2, 4, 5]), # Delete third node
    ([1, 2, 3, 4, 5], 3, [1, 2, 3, 5]), # Delete fourth node
])
def test_multiple_scenarios(create_linked_list, linked_list_to_array, input_list, node_index, expected):
    """Test multiple scenarios using parametrize"""
    head = create_linked_list(input_list)
    node_to_delete = head
    for _ in range(node_index):
        node_to_delete = node_to_delete.next
    delete_middle_node(node_to_delete)
    assert linked_list_to_array(head) == expected

# Edge Cases
def test_delete_last_node(create_linked_list, linked_list_to_array):
    """Test attempting to delete the last node (should raise error)"""
    head = create_linked_list([1, 2, 3])
    node_to_delete = head.next.next  # last node
    with pytest.raises(AttributeError):
        delete_middle_node(node_to_delete)

def test_delete_single_node(create_linked_list, linked_list_to_array):
    """Test attempting to delete a single node (should raise error)"""
    head = create_linked_list([1])
    with pytest.raises(AttributeError):
        delete_middle_node(head)
