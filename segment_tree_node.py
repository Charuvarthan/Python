"""
Implementation of a Segment Tree using node-based binary tree structure.

Supports efficient range sum queries and point updates.

Doctest examples:
>>> st = SegmentTree([1, 3, 5])
>>> st.query(0, 2)
9
>>> st.update(1, 2)
>>> st.query(0, 2)
8
"""

from typing import Optional


class SegmentTreeNode:
    def __init__(self, start: int, end: int, value: int = 0) -> None:
        self.start: int = start
        self.end: int = end
        self.value: int = value
        self.left: Optional["SegmentTreeNode"] = None
        self.right: Optional["SegmentTreeNode"] = None


class SegmentTree:
    def __init__(self, nums: list[int]) -> None:
        """
        Initialize the segment tree with input list.

        >>> SegmentTree([1, 2, 3])  # doctest: +ELLIPSIS
        <...SegmentTree object at ...>
        """
        if not nums:
            raise ValueError("Input list cannot be empty.")
        self.root: SegmentTreeNode = self._build(nums, 0, len(nums) - 1)

    def _build(self, nums: list[int], start: int, end: int) -> SegmentTreeNode:
        """
        Build the segment tree recursively.

        >>> st = SegmentTree([1, 2, 3])
        >>> st.root.value
        6
        """
        if start == end:
            return SegmentTreeNode(start, end, nums[start])
        mid: int = (start + end) // 2
        node = SegmentTreeNode(start, end)
        node.left = self._build(nums, start, mid)
        node.right = self._build(nums, mid + 1, end)
        node.value = node.left.value + node.right.value
        return node

    def update(self, index: int, new_value: int) -> None:
        """
        Update the value at a specific index.

        >>> st = SegmentTree([1, 2, 3])
        >>> st.update(1, 5)
        >>> st.query(0, 2)
        9
        """
        self._update(self.root, index, new_value)

    def _update(self, node: SegmentTreeNode, index: int, new_value: int) -> None:
        if node.start == node.end == index:
            node.value = new_value
            return
        if node.left and index <= node.left.end:
            self._update(node.left, index, new_value)
        elif node.right:
            self._update(node.right, index, new_value)
        node.value = (node.left.value if node.left else 0) + (node.right.value if node.right else 0)

    def query(self, left: int, right: int) -> int:
        """
        Return the sum of elements in range [left, right].

        >>> st = SegmentTree([1, 3, 5, 7, 9])
        >>> st.query(1, 3)
        15
        """
        return self._query(self.root, left, right)

    def _query(self, node: Optional[SegmentTreeNode], left: int, right: int) -> int:
        if node is None or node.end < left or node.start > right:
            return 0
        if left <= node.start and node.end <= right:
            return node.value
        return self._query(node.left, left, right) + self._query(node.right, left, right)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
