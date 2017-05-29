""" [Diagonal](https://codelab.interviewbit.com/problems/diagonal/)

Given an N x N matrix, return an array of its anti-diagonals. Look at the example for more details:

Example:


Input:

1 2 3
4 5 6
7 8 9

Return the following :

[
  [1],
  [2, 4],
  [3, 5, 7],
  [6, 8],
  [9]
]


Input :
1 2
3 4

Return the following  :

[
  [1],
  [2, 3],
  [4]
]

"""
from typing import Any, Sequence


class Solution(object):
    @staticmethod
    def anti_diagonals(matrix: Sequence[Sequence[Any]]) -> Sequence[Sequence[Any]]:
        length = len(matrix)

        assert all(len(row) == length for row in matrix), f'Expected square matrix of size {length} x {length}'
        result = []

        for i in range(0, length):  # iterate over columns
            diagonal = []
            k = i
            for j in range(0, i + 1):  # iterate over rows
                diagonal.append(matrix[j][k])
                k -= 1
            result.append(diagonal)

        for i in range(1, length):  # iterate over rows
            diagonal = []
            k = length - 1
            for j in range(i, length):  # iterate over columns
                diagonal.append(matrix[j][k])
                k -= 1
            result.append(diagonal)

        return result


anti_diagonals = Solution.anti_diagonals([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(anti_diagonals)
