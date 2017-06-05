""" [Single](https://codelab.interviewbit.com/problems/single/)

Given an array of integers, every element appears twice except for one. Find that single one.

Note: Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

Example :

Input : [1, 2, 2, 3, 1]

Output : 3

Observations
------------
1. One might record each number in a set the first time it's encountered and then remove it, if it's encountered again
   This leaves one element in the set at the end: the lone unpaired member.
   Time complexity: O(n) => acceptable, but not optimal since additional storage is required
2. One might also destructively reorganize the elements in the input, collocating each pair. The algorithm would stop
   early, if no matching element was found.
   Time complexity: O(n ln(n)) => no good
3. Capitalize on a property of the two's complement number system:
   * The bitwise exclusive or of any number with zero is itself.
   * The bitwise exclusive or of any number with itself is zero.
   Since we've got pairs of numbers, we can can and through the array knowing that just one number will not be xor'ed
   with itself. This ensures that just one number's bit pattern is retained: the bit pattern of the one and only one
   unpaired integer.

"""
import pytest
from typing import Sequence


class Solution(object):

    @staticmethod
    def compute(inputs: Sequence[int]) -> int:
        assert len(inputs) != 0 and (len(inputs) & 1) != 0
        visited = set()
        for n in inputs:
            try:
                visited.remove(n)
            except KeyError:
                visited.add(n)
        assert len(visited) == 1
        return visited.pop()

    @staticmethod
    def clever_alternative(inputs: Sequence[int]) -> int:
        # makes use of the fact that
        # * the exclusive or of a number with itself is zero
        # * the exclusive or of a number with zero is itself
        assert len(inputs) != 0 and (len(inputs) & 1) != 0
        result = 0
        for n in inputs:
            result ^= n
        return result


@pytest.mark.parametrize(
    'method,inputs,expected', [
        ('compute', [1, 2, 2, 3, 1], 3),
        ('clever_alternative', [1, 2, 2, 3, 1], 3),
        ('compute', [1], 1),
        ('clever_alternative', [1], 1),
    ]
)
def test_correctness(method: str, inputs: Sequence[int], expected: int):
    observed = getattr(Solution, method)(inputs)
    assert observed == expected, f'Expected {expected}, not {observed}'
