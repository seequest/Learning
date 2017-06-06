""" [Majority]()

Given an array of size n, find the majority element. The majority element is the element that appears more than
floor(n/2) times.

You may assume that the array is non-empty and the majority element always exist in the array.

Example :

Input : [2, 1, 2]
Return  : 2 which occurs 2 times which is greater than 3/2.

"""
from typing import Any, Sequence

import pytest


class Solution(object):

    @staticmethod
    def compute(values: Sequence[Any]) -> Any:

        stop = len(values) // 2
        maximum = (None, 0)
        counts = {}

        for value in values:
            try:
                count = counts[value]
            except KeyError:
                count = counts[value] = 1
            else:
                count = counts[value] = count + 1
            if count > maximum[1]:
                maximum = (value, count)
            if count > stop:
                break

        assert maximum[1] > stop
        return maximum[0]

    @staticmethod
    def clever_alternative(values: Sequence[Any]) -> Any:
        majority = 0
        count = 1

        for i in range(1, len(values)):
            if values[majority] == values[i]:
                count += 1
            else:
                count -= 1
            if count == 0:
                majority = i
                count = 1

        return values[majority]


@pytest.mark.parametrize(
    'method, values, expected', [
        ('clever_alternative', [1, 1, 2, 1, 2, 3, 1, 3, 1], 1),
        ('clever_alternative', [2, 1, 2], 2),
        ('clever_alternative', [2, 1, 2], 2),
        ('clever_alternative', [1, 1, 1, 2, 2], 1),
        ('compute', [2, 1, 2], 2),
        ('compute', [2, 1, 2], 2),
        ('compute', [1, 1, 1, 2, 2], 1),
    ]
)
def test_correctness(method, values: Sequence[Any], expected: Any) -> None:
    observed = getattr(Solution, method)(values)
    assert observed == expected, f'Expected {expected}, not {observed}'
