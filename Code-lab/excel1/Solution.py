""" [Excel1](https://codelab.interviewbit.com/problems/excel1/)

Given a column title as appears in an Excel sheet, return its corresponding column number.

Example:

    A -> 1

    B -> 2

    C -> 3

    ...

    Z -> 26

    AA -> 27

    AB -> 28

"""
import pytest


class Solution(object):

    @staticmethod
    def compute(column: str) -> int:
        number = 0
        place = 1

        for digit in reversed(column):
            value = ord(digit) - Solution.one
            number += place * value
            assert 0 <= value <= 26
            place *= 26

        return number

    one = ord('A') - 1


@pytest.mark.parametrize(
    'column,expected', [
        ('A', 1),
        ('Z', 26),
        ('AA', 27),
        ('ZZ', 702),
        ('AAA', 703),
    ]
)
def test_correctness(column: str, expected: int) -> None:
    observed = Solution.compute(column)
    assert observed == expected, f'Expected column {column} = {expected}, not {observed}'
