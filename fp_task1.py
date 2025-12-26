from __future__ import annotations


class Node:
    def __init__(self, value: int, next: "Node | None" = None):
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value})"


def reverse_list(head: Node | None) -> Node | None:
    """Реверсування однозв'язного списку шляхом зміни посилань між вузлами."""
    prev = None
    current = head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def merge_sorted_lists(a: Node | None, b: Node | None) -> Node | None:
    """Об'єднання двох відсортованих однозв'язних списків в один відсортований."""
    dummy = Node(0)
    tail = dummy

    while a is not None and b is not None:
        if a.value <= b.value:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a is not None else b
    return dummy.next


def _split_middle(head: Node) -> tuple[Node, Node]:
    """Розділити список на 2 частини: повертає (ліва_частина, права_частина)."""
    slow: Node = head
    fast: Node | None = head
    prev: Node | None = None

    while fast is not None and fast.next is not None:
        prev = slow
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next.next

    # prev - кінець лівої частини, slow - початок правої
    # розриваємо зв'язок
    if prev is not None:
        prev.next = None

    return head, slow


def merge_sort_list(head: Node | None) -> Node | None:
    """Сортування однозв'язного списку (merge sort)."""
    if head is None or head.next is None:
        return head

    left, right = _split_middle(head)
    left_sorted = merge_sort_list(left)
    right_sorted = merge_sort_list(right)

    return merge_sorted_lists(left_sorted, right_sorted)


def from_list(values: list[int]) -> Node | None:
    head = None
    tail = None
    for v in values:
        node = Node(v)
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node
    return head


def to_list(head: Node | None) -> list[int]:
    res = []
    cur = head
    while cur is not None:
        res.append(cur.value)
        cur = cur.next
    return res


if __name__ == "__main__":
    # Перевірка реверсу
    h = from_list([1, 2, 3, 4])
    h = reverse_list(h)
    print("reverse:", to_list(h))  # [4, 3, 2, 1]

    # Перевірка сортування
    h2 = from_list([4, 1, 5, 2, 3])
    h2 = merge_sort_list(h2)
    print("sort:", to_list(h2))  # [1, 2, 3, 4, 5]

    # Перевірка злиття двох відсортованих списків
    a = from_list([1, 3, 5])
    b = from_list([2, 4, 6])
    m = merge_sorted_lists(a, b)
    print("merge:", to_list(m))  # [1, 2, 3, 4, 5, 6]
