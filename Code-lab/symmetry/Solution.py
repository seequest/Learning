""" [Symmetry]()

Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

Example :
Given binary tree

        1
    /       \
   2         2
 /   \     /   \
3     4   4     3

return

True

Example :
Given binary tree

      1
    /   \
   1     2
 /  \   /  \
1    2 3    4

return

False

"""
from collections import deque
from typing import Optional, Sequence
import pytest


class TreeNode:
    def __init__(self, value: int, left: Optional['TreeNode'], right: Optional['TreeNode']):
        self.val = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f'TreeNode(value={self.val}, left={repr(self.left)}, right={repr(self.right)})'

    def __str__(self):
        return f'value={self.val}, left={self.left}, right={self.right}'


class Solution(object):
    @staticmethod
    def compute(root: TreeNode) -> bool:

        assert root is not None
        parents = deque([root])

        def is_asymmetric(level: Sequence[TreeNode]):
            assert (len(level) & 1) == 0, f'Expected an even number of tree nodes, not {len(level)}'

            length = len(level)
            n = len(level) >> 1
            left = (level[i] if level[i] is None else level[i].val for i in range(n))
            right = (level[i] if level[i] is None else level[i].val for i in range(length - 1, n - 1, -1))

            return any(x != y for x, y in zip(left, right))

        while True:
            children = deque()

            while len(parents) > 0:
                node = parents.pop()
                if node is not None:
                    children.append(node.left)
                    children.append(node.right)

            if len(children) == 0:
                return True

            if is_asymmetric(children):
                return False

            parents = children


@pytest.mark.parametrize(
    'root,expected', [
        # (
        #         TreeNode(3, TreeNode(9, None, None), TreeNode(20, TreeNode(15, None, None), TreeNode(7, None, None))),
        #         False
        # ),
        (
                TreeNode(1,
                         TreeNode(2,
                                  TreeNode(2,
                                           TreeNode(1, None, None),
                                           TreeNode(2, None, None)),
                                  TreeNode(3,
                                           TreeNode(3, None, None),
                                           TreeNode(4, None, None))),
                         TreeNode(2,
                                  TreeNode(3,
                                           TreeNode(4, None, None),
                                           TreeNode(3, None, None)),
                                  TreeNode(2,
                                           TreeNode(2, None, None),
                                           TreeNode(1, None, None)))
                         ),
                True
        ),
        (
                TreeNode(1,
                         TreeNode(2,
                                  TreeNode(2,
                                           None,
                                           TreeNode(2, None, None)),
                                  TreeNode(3,
                                           TreeNode(3, None, None),
                                           TreeNode(4, None, None))),
                         TreeNode(2,
                                  TreeNode(3,
                                           TreeNode(4, None, None),
                                           TreeNode(3, None, None)),
                                  TreeNode(2,
                                           TreeNode(2, None, None),
                                           None))
                         ),
                True
        ),
        (
                TreeNode(1,
                         TreeNode(2,
                                  TreeNode(2,
                                           TreeNode(2, None, None),
                                           None),
                                  TreeNode(3,
                                           TreeNode(3, None, None),
                                           TreeNode(4, None, None))),
                         TreeNode(2,
                                  TreeNode(3,
                                           TreeNode(4, None, None),
                                           TreeNode(3, None, None)),
                                  TreeNode(2,
                                           TreeNode(2, None, None),
                                           None))
                         ),
                False
        ),
    ]
)
def test_correctness(root: TreeNode, expected: Sequence[Sequence[int]]):
    observed = Solution.compute(root)
    assert observed == expected, f'Expected {expected}, not {observed}'
