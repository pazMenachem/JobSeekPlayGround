import pytest
from typing import Optional
from linked_list import create_linked_list, linked_list_to_array, ListNode

def remove_kth_element(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    
    dummy = ListNode(0)
    dummy.next = head
    slow = dummy
    fast = dummy
    count = k
    
    while count:
        ## k is larger than LL length
        if not fast:
            return head
        
        fast = fast.next
        count -= 1
        
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    
    slow.next = slow.next.next
    return dummy.next

# Test cases
def test_empty_list(create_linked_list, linked_list_to_array):
    head = None
    assert remove_kth_element(head, 2) is None

def test_basic_case(create_linked_list, linked_list_to_array):
    head = create_linked_list([1, 2, 3, 4, 5, 6])
    assert linked_list_to_array(remove_kth_element(head, 3)) == [1, 2, 3, 5, 6]

def test_LL_shorter_than_k(create_linked_list, linked_list_to_array):
    head = create_linked_list([1, 2, 3, 4, 5, 6])
    assert linked_list_to_array(remove_kth_element(head, 100)) == [1, 2, 3, 4, 5, 6]

def test_edge_case_k(create_linked_list, linked_list_to_array):
    head = create_linked_list([1, 2, 3, 4, 5, 6])
    assert linked_list_to_array(remove_kth_element(head, 1)) == [1, 2, 3, 4, 5]

def test_edge_case_head(create_linked_list, linked_list_to_array):
    head = create_linked_list([1, 2, 3, 4, 5, 6])
    assert linked_list_to_array(remove_kth_element(head, 6)) == [2, 3, 4, 5, 6]
