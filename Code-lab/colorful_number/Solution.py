""" [Colorful](https://codelab.interviewbit.com/problems/colorful/)

For Given Number N find if its COLORFUL number or not

Return 0/1

COLORFUL number:

A number can be broken into different contiguous sub-sequence parts.
Suppose, a number 3245 can be broken into parts like 3 2 4 5 32 24 45 324 245.
And this number is a COLORFUL number, since the product of every digit of a contiguous sub-sequence is different
Example:

N = 23
2 3 23
2 -> 2
3 -> 3
23 -> 6

This number is a COLORFUL number since product of every digit of a sub-sequence are different.

Output : 1

Solution
--------
1. Compute two contiguous sub-sequences.
2. Compare them pairwise
3. Move to the next pair, if they're different

"""
import pytest
from typing import Sequence


class Solution(object):

    @staticmethod
    def is_colorful(number: int) -> bool:
        assert number >= 0

        if number <= 10:
            return True

        digits = []

        while number > 0:
            digits.append(number % 10)
            number //= 10

        def product_of(numbers: Sequence[int]) -> int:
            n = numbers[0]
            for i in range(1, len(numbers)):
                n *= numbers[i]
            return n

        digits.reverse()
        products = set()

        for end in range(0, len(digits)):
            for start in range(0, len(digits) - end):
                sequence = digits[start: start + end + 1]
                product = product_of(sequence)
                if product in products:
                    return False
                products.add(product)

        return True


@pytest.mark.parametrize(
    'number,expected', [
        (213, False),
        (123, False),
        (23, True),
        (3245, True)
    ]
)
def test_correctness(number: int, expected: bool):
    observed = Solution.is_colorful(number)
    assert observed is expected
