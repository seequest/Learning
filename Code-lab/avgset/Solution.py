""" [Avgset]()

Given an array with non negative numbers, divide the array into two parts such that the average of both the parts is
equal.

Return both parts, if they exist. Otherwise, return an empty list.

Example:

Input:
integers = [1, 7, 15, 29, 11, 9]

average(integers) = sum(integers) / len(integers) = 12
deviation(integers) = [-11, -5, +3, +17, -1, -3]
sum(deviations) = 0

Output:
[9 15] [1 7 11 29]

The average of part is (15+9)/2 = 12,
average of second part elements is (1 + 7 + 11 + 29) / 4 = 12

NOTE 1: If a solution exists, you should return a list of exactly 2 lists of integers A and B which follow the
following condition:

* numElements in A <= numElements in B
* If numElements in A = numElements in B, then A is lexicographically smaller than B.

NOTE 2: If multiple solutions exist, return the solution where length(A) is minimum. If there is still a tie, return the one where A is lexicographically smallest.

NOTE 3: Array will contain only non negative numbers.

Observations
------------

integers = [1, 7, 15, 29, 11, 9]

average(integers) = sum(integers) / len(integers) = 12
deviation(integers) = [-11, -5, +3, +17, -1, -3]
sum(deviations) = 0

Task: Find the shortest list of integers whose deviations sum to zero.

Brute force:
1. Consider single items, then pairs of items, then triplets, etc. starting with the largest (?)
number
performance polynomial complexity: O(n^n)

2.

References
----------

1. [Lexicographical order](https://en.wikipedia.org/wiki/Lexicographical_order)

"""
from collections import deque
from typing import Sequence
import pytest


class Solution(object):
    @staticmethod
    def compute(integers: Sequence[int]) -> Sequence[Sequence[int]]:

        average: float = sum(integers) / len(integers)

        if not average.is_integer():
            return []

        average: int = int(average)
        integers = sorted(integers)
        stack = deque()

        # TODO: make use of fact that positive deviations must be paired with negative deviations to equal zero

        for i, item in enumerate(integers):
            deviation = item - average
            if deviation == 0:
                return [[item], [integers[j] for j in range(len(integers)) if j != i]]
            stack.append((i, deviation, [i]))

        while len(stack) > 0:
            i, sum_deviations, items = stack.popleft()
            for j in range(i + 1, len(integers)):
                item = integers[j]
                new_items = items + [j]
                new_sum_deviations = sum_deviations + (item - average)
                if new_sum_deviations == 0:
                    item_set = frozenset(new_items)
                    result = [
                        list(integers[k] for k in new_items),
                        list(integers[k] for k in range(0, len(integers)) if k not in new_items)
                    ]
                    return result
                stack.append((j, new_sum_deviations, new_items))

        return []


@pytest.mark.parametrize(
    'integers,expected', [
        ([1, 7, 15, 29, 11, 9], [[9, 15], [1, 7, 11, 29]]),
    ]
)
def test_correctness(integers: Sequence[int], expected: Sequence[Sequence[int]]) -> None:
    observed = Solution.compute(integers)
    assert observed == expected, f'Expected {expected}, not {observed}'
