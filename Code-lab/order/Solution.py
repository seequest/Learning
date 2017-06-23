""" [Order]()

You are given the following :

* A positive number N

* heights: A list of heights of N persons standing in a queue

* in_fronts: A list of numbers corresponding to each person (P) that gives the number of persons who are taller than P
and standing in front of P

You need to return list of actual order of persons’s height.

Guarantees:

* Heights will be unique.

Example

Input:
    0 1 2 3 4 5
    heights:
    5 3 2 6 1 4
    in_fronts:
    0 1 2 0 3 2

Output:
    Actual order is:
    5 3 2 6 1 4

because it specifies the rank of each person in the queue:

    heights[5] = 1
    heights[3] = 2
    heights[2] = 3
    heights[6] = 4
    heights[1] = 5
    heights[4] = 6


So, you can see that for the person with height 5, there is no one taller than him who is in front of him, and hence
in_fronts has 0 for him.

For person with height 3, there is 1 person ( Height : 5 ) in front of him who is taller than him.

You can do similar inference for other people in the list.

"""
from typing import Deque, Sequence
from collections import deque
import pytest


class Solution(object):

    @staticmethod
    def compute(heights: Sequence[int], in_fronts: Sequence[int]) -> Sequence[int]:

        assert len(heights) == len(in_fronts)
        count = len(heights)
        result = deque()
        i = 0

        return result

    @staticmethod
    def order(heights: Sequence[int], in_fronts: Sequence[int]) -> Sequence[int]:
        assert len(heights) == len(in_fronts)
        ahead = Deque[int]()
        behind = Deque[int]()

        for i in range(len(heights)):
            if in_fronts[i] == 0:
                if len(ahead) == 0 or heights[ahead[0]] < heights[i]:
                    ahead.append(i)
                else:
                    ahead.appendleft(i)
            else:
                if len(behind) == 0 or heights[behind[0]] < heights[i]:
                    behind.append(i)
                else:
                    behind.appendleft(i)

        return list(i + 1 for i in behind) + list(i + 1 for i in ahead)


@pytest.mark.parametrize(
    'heights, in_fronts, expected', [
        ([2, 3, 5, 6, 1, 4], [2, 1, 0, 0, 3, 2], [5, 3, 2, 1, 6, 4]),
        ([86, 77], [0, 1], [86, 77]),
        ([5, 3, 2, 6, 1, 4], [0, 1, 2, 0, 3, 2], [5, 3, 2, 1, 6, 4]),
    ]
)
def test_correctness(heights: Sequence[int], in_fronts: Sequence[int], expected: Sequence[int]):
    observed = Solution.compute(heights, in_fronts)
    assert observed == expected
    print(f'Ordered heights: {[heights[position - 1] for position in observed]}')
