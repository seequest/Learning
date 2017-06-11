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
from typing import Dict, Iterator, List, Optional, Sequence, Tuple
from fractions import Fraction
from statistics import mean

import pytest


class Solution(object):

    @staticmethod
    def compute(integers: Sequence[int]) -> Sequence[Sequence[int]]:

        # Compute average as a fraction--for precision--and then normalize and sort integers

        average: Fraction = Fraction(sum(integers), len(integers))
        denominator: int = average.denominator

        if denominator > 1:
            integers = sorted(integer * denominator for integer in integers)
        else:
            integers = sorted(integers)

        average: int = average.numerator

        # Look for the shortest sequence of integers whose total matches the average we computed

        for count in range(1, (len(integers) >> 1) + 1):

            total = count * average

            if denominator > 1 and total % denominator != 0:
                continue

            combination = next(Solution._combinations(integers, total, count), None)

            if combination:
                iterator = iter(integers)
                value = next(iterator)
                subset = []

                for compare in combination:

                    while value < compare:
                        subset.append(value)
                        value = next(iterator)

                    value = next(iterator, None)

                if value is not None:
                    subset.append(value)
                    subset.extend(iterator)

                if denominator == 1:
                    result = [list(combination), subset]
                else:

                    def divide(v: List[int]) -> List[int]:
                        for i in range(len(v)):
                            v[i] //= denominator
                        return v

                    result = [divide(list(combination)), divide(subset)]

                return result

        return []

    @staticmethod
    def _combinations(values: Sequence[int], total: int, count: int) -> Iterator[Sequence[int]]:

        cache: Dict[Tuple[int, int, int], Optional[Sequence[int]]] = {}
        cache_hits: int = 0

        # noinspection PyShadowingNames
        def find(start: int, subtotal: int, count: int) -> Optional[Tuple[int, ...]]:
            match = start, subtotal, count
            try:
                result = cache[match]
                nonlocal cache_hits
                cache_hits += 1
                return result
            except KeyError:
                pass

            value = values[start]
            result = None

            if count == 1 and value == subtotal:
                result = (start,)
            elif count > 1 and value < subtotal:
                subtotal -= value
                count -= 1
                for index in range(start + 1, len(values) - count + 1):
                    result = find(index, subtotal, count)
                    if result is not None:
                        result = (start,) + result
                        break

            cache[match] = result
            return result

        for start in range(len(values) - count + 1):
            indexes = find(start, total, count)
            if indexes is None:
                continue
            yield [values[i] for i in indexes]


@pytest.mark.parametrize(
    'integers,expected', [
        ([1, 7, 15, 29, 11, 9], [[9, 15], [1, 7, 11, 29]]),
        (
                [16, 42, 18, 48, 26, 45, 46, 26, 25, 7, 7, 48, 30, 10, 10, 3, 1, 11, 33, 14, 21, 15],
                [
                    [1, 3, 7, 7, 10, 10, 26, 45, 46, 48, 48],
                    [11, 14, 15, 16, 18, 21, 25, 26, 30, 33, 42]
                ]
        ),
        (
                [12, 23, 38, 3, 45, 14, 33, 37, 35, 50, 27, 8, 5, 47, 12, 43, 2, 49, 39, 30, 18, 46, 7, 27],
                [
                    [2, 3, 5, 7, 8, 27, 38, 43, 46, 47, 49, 50],
                    [12, 12, 14, 18, 23, 27, 30, 33, 35, 37, 39, 45]
                ]
        ),
        ([1, 7, 15, 29, 10, 8, 13, 13], [[8, 13, 15], [1, 7, 10, 13, 29]]),
        ([47, 14, 30, 19, 30, 4, 32, 32, 15, 2, 6, 24], [[2, 4, 32, 47], [6, 14, 15, 19, 24, 30, 30, 32]]),
        (
                [33, 0, 19, 49, 29, 29, 28, 41, 36, 40, 24, 34, 35, 26, 1, 0, 27, 12, 13, 50, 4, 0, 45, 39, 26],
                [
                    [0, 0, 29, 49, 50],
                    [0, 1, 4, 12, 13, 19, 24, 26, 26, 27, 28, 29, 33, 34, 35, 36, 39, 40, 41, 45]
                ]
        ),
        (
                [5, 16, 3, 4, 5, 2, 16, 49, 10, 35, 33, 14, 30, 40, 22, 7, 24, 38, 47, 19, 42],
                []
        ),
    ]
)
def test_correctness(integers: Sequence[int], expected: Sequence[Sequence[int]]) -> None:
    observed = Solution.compute(integers)
    if len(observed) == 2:
        assert len(expected) == 2
        assert mean(integers) == mean(expected[0])
        assert mean(integers) == mean(expected[1])
    assert observed == expected, f'Expected {expected}, not {observed}'
