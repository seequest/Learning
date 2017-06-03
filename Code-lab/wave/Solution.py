""" [Wave]()

Given an array of integers, sort the array [in-place] into a wave like array and return it,
In other words, arrange the elements into a sequence such that a1 >= a2 <= a3 >= a4 <= a5.....

Example

Given [1, 2, 3, 4]

One possible answer : [2, 1, 4, 3]
Another possible answer : [4, 1, 3, 2]
NOTE : If there are multiple answers possible, return the one that's lexicographically smallest.
So, in example case, you will return [2, 1, 4, 3]

Observations
------------

1. This problem reduces to sorting number pairs.

2. Lexicographically smallest => assuming the index of N represent the sort order of the array we should sort the pairs
   like this:

    (N(1), N(0)), ((N(3), N(1)), (N(5), N(4), ..., N(len(input)-1, N(len(input)-2)

3. One might use a system sort routine and then swap pairs of entries.

"""
from typing import Sequence
import pytest


class Solution(object):

    @staticmethod
    def compute(integers: Sequence[int]) -> Sequence[int]:

        answer = sorted(integers)

        for i in range(0, (len(answer) >> 1) << 1, 2):
            number = answer[i]
            answer[i] = answer[i + 1]
            answer[i + 1] = number

        return answer


@pytest.mark.parametrize(
    'integers,expected', [
        ([5, 4, 3, 2, 1], [2, 1, 4, 3, 5]),
        ([4, 3, 2, 1], [2, 1, 4, 3]),
        ([1, 0], [1, 0]),
        ([0, 1])
    ]
)
def test_correctness(integers: Sequence[int], expected: Sequence[int]):
    observed = Solution.compute(integers)
    assert list(observed) == expected
