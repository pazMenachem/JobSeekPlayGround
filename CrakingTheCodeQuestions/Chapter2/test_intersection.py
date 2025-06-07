from linked_list import create_linked_list, linked_list_to_array, ListNode
from typing import Optional
import pytest

def getIntersectionNode(headA: ListNode, headB: ListNode) -> Optional[ListNode]:
    if not headA or not headB:
        return None
    a, b = headA, headB
    while (a != b):
        a = headB if not a else a.next
        b = headA if not b else b.next
    return a

@pytest.fixture
def create_intersecting_lists(create_linked_list):
    """Fixture to create two linked lists that intersect at a common point"""
    def _create_intersecting_lists(list_a: list[int], list_b: list[int], intersection: list[int]) -> tuple[ListNode, ListNode]:
        # Create the intersection part first
        intersection_head = create_linked_list(intersection)
        
        # Create list A
        if list_a:
            head_a = create_linked_list(list_a)
            current = head_a
            while current.next:
                current = current.next
            current.next = intersection_head
        else:
            head_a = intersection_head
            
        # Create list B
        if list_b:
            head_b = create_linked_list(list_b)
            current = head_b
            while current.next:
                current = current.next
            current.next = intersection_head
        else:
            head_b = intersection_head
            
        return head_a, head_b
    return _create_intersecting_lists

# Test Cases
def test_no_intersection(create_linked_list, linked_list_to_array):
    """Test when lists don't intersect"""
    head_a = create_linked_list([1, 2, 3])
    head_b = create_linked_list([4, 5, 6])
    result = getIntersectionNode(head_a, head_b)
    assert result is None

def test_same_list(create_linked_list, linked_list_to_array):
    """Test when both lists are the same"""
    head = create_linked_list([1, 2, 3, 4, 5])
    result = getIntersectionNode(head, head)
    assert linked_list_to_array(result) == [1, 2, 3, 4, 5]

def test_intersection_at_end(create_intersecting_lists, linked_list_to_array):
    """Test when lists intersect at the end"""
    head_a, head_b = create_intersecting_lists(
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    )
    result = getIntersectionNode(head_a, head_b)
    assert linked_list_to_array(result) == [7, 8, 9]

def test_intersection_at_middle(create_intersecting_lists, linked_list_to_array):
    """Test when lists intersect in the middle"""
    head_a, head_b = create_intersecting_lists(
        [1, 2, 3],
        [4, 5],
        [6, 7, 8]
    )
    result = getIntersectionNode(head_a, head_b)
    assert linked_list_to_array(result) == [6, 7, 8]

def test_one_empty_list(create_linked_list, linked_list_to_array):
    """Test when one list is empty"""
    head_a = create_linked_list([1, 2, 3])
    head_b = None
    result = getIntersectionNode(head_a, head_b)
    assert result is None

def test_different_lengths(create_intersecting_lists, linked_list_to_array):
    """Test lists of different lengths"""
    head_a, head_b = create_intersecting_lists(
        [1, 2, 3, 4, 5],
        [6, 7],
        [8, 9, 10]
    )
    result = getIntersectionNode(head_a, head_b)
    assert linked_list_to_array(result) == [8, 9, 10]

def test_intersection_at_start(create_intersecting_lists, linked_list_to_array):
    """Test when lists intersect at the start"""
    head_a, head_b = create_intersecting_lists(
        [],
        [],
        [1, 2, 3, 4, 5]
    )
    result = getIntersectionNode(head_a, head_b)
    assert linked_list_to_array(result) == [1, 2, 3, 4, 5]

# Parametrized test for multiple scenarios
@pytest.mark.parametrize("list_a,list_b,intersection,expected", [
    ([1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 8, 9]),
    ([1, 2], [3, 4, 5], [6, 7], [6, 7]),
    ([1], [2], [3, 4, 5], [3, 4, 5]),
    ([], [], [1, 2, 3], [1, 2, 3]),
])
def test_multiple_scenarios(create_intersecting_lists, linked_list_to_array, list_a, list_b, intersection, expected):
    """Test multiple scenarios using parametrize"""
    head_a, head_b = create_intersecting_lists(list_a, list_b, intersection)
    result = getIntersectionNode(head_a, head_b)
    assert linked_list_to_array(result) == expected
