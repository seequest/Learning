""" [Maxset]()


Find out the maximum sub-array of non negative numbers from an array.
The sub-array should be continuous. That is, a sub-array created by choosing the second and fourth element and skipping the third element is invalid.

Maximum sub-array is defined in terms of the sum of the elements in the sub-array. Sub-array A is greater than sub-array B if sum(A) > sum(B).

Example:

A : [1, 2, 5, -7, 2, 3]
The two sub-arrays are [1, 2, 5] [2, 3].
The answer is [1, 2, 5] as its sum is larger than [2, 3]
NOTE: If there is a tie, then compare with segment's length and return segment which has maximum length
NOTE 2: If there is still a tie, then return the segment with minimum starting index

Observations
------------
1. track start of current sequence
2. mark end of current sequence at first negative number of end of numbers array
3. compare sum of current sequence to current max sequence (denote initial max sequence with start=-1, end=-1, sum=-1

"""
from typing import Sequence
import pytest

from collections import namedtuple

SubArray = namedtuple('SubArray', ('start', 'end', 'sum'))


class Solution(object):

    @staticmethod
    def compute(integers: Sequence[int]):

        if len(integers) == 0:
            return []

        maximum = SubArray(start=-1, end=-1, sum=-1)
        length = len(integers)
        start = 0

        while start < length:

            # advance

            while integers[start] < 0:
                start += 1
                if start == length:
                    return integers[maximum.start: maximum.end] if maximum.start >= 0 else []

            # lookahead

            end = start

            while integers[end] >= 0:
                end += 1
                if end == length:
                    break

            # compute sum and reset maximum as appropriate

            sub_array = SubArray(start, end, sum(integers[i] for i in range(start, end)))

            if sub_array.sum > maximum.sum:
                maximum = sub_array
            elif sub_array.sum == maximum.sum and sub_array.end - sub_array.start > maximum.end - maximum.start:
                maximum = sub_array

            start = end

        return integers[maximum.start: maximum.end]


@pytest.mark.parametrize(
    'integers,expected', [
        ([-846930886, -1714636915, 424238335, -1649760492], [424238335]),
        ([1, 2, 5, -7, 2, 3], [1, 2, 5]),
    ]
)
def test_correctness(integers: Sequence[int], expected: Sequence[int]):
    observed = Solution.compute(integers)
    assert list(observed) == expected, f'Expected {expected}, not {observed}'
