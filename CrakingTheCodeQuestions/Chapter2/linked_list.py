from typing import Optional, List
import pytest

class ListNode:
    """Node class for singly linked list"""
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

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
