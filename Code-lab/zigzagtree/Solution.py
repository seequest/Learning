""" [ZigzagTree]()

Given a binary tree, return the zigzag level order traversal of its nodes’ values. (ie, from left to right, then right to left for the next level and alternate between).

Example :
Given binary tree

    3
   / \
  9  20
    /  \
   15   7
return

[
         [3],
         [20, 9],
         [15, 7]
]

Example :
Given binary tree

      1
    /   \
   1     2
 /  \   /  \
1    2 3    4

return
[
         [1],
         [2, 1],
         [1, 2, 3, 4]
]

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
    def compute(root: TreeNode) -> Sequence[Sequence[int]]:

        assert root is not None
        parents = deque([root])
        left_to_right = False
        result = []

        while True:
            left_to_right = not left_to_right
            children = deque()
            level = []

            if left_to_right:
                while len(parents) > 0:
                    node = parents.pop()
                    if node.left is not None:
                        children.append(node.left)
                    if node.right is not None:
                        children.append(node.right)
                    level.append(node.val)
            else:
                while len(parents) > 0:
                    node = parents.pop()
                    if node.right is not None:
                        children.append(node.right)
                    if node.left is not None:
                        children.append(node.left)
                    level.append(node.val)

            result.append(level)

            if len(children) == 0:
                break

            parents = children

        return result


@pytest.mark.parametrize(
    'root,expected', [
        (
            TreeNode(3, TreeNode(9, None, None), TreeNode(20, TreeNode(15, None, None), TreeNode(7, None, None))),
            [[3], [20, 9], [15, 7]]
        ),
        (
            TreeNode(1,
                     TreeNode(1,
                              TreeNode(1,
                                       TreeNode(1, None, None),
                                       TreeNode(2, None, None)),
                              TreeNode(2,
                                       TreeNode(3, None, None),
                                       TreeNode(4, None, None))),
                     TreeNode(2,
                              TreeNode(3,
                                       TreeNode(5, None, None),
                                       TreeNode(6, None, None)),
                              TreeNode(4,
                                       TreeNode(7, None, None),
                                       TreeNode(8, None, None)))
                     ),
            [[1], [2, 1], [1, 2, 3, 4], [8, 7, 6, 5, 4, 3, 2, 1]]
        ),
    ]
)
def test_correctness(root: TreeNode, expected: Sequence[Sequence[int]]):
    observed = Solution.compute(root)
    assert list(observed) == expected, f'Expected {expected}, not {observed}'
