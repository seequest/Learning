""" [Factorial]()

Given an integer n, return the number of trailing zeroes in n!.

Note: Your solution should be in logarithmic time complexity.

Example :

n = 5
n! = 120
Number of trailing zeros = 1
So, return 1

Observations
------------
1. 1! = 1, n! = n * (n-1)!, where n > 1
2. The number of trailing zeros in a number is equal to the number of powers of 10 in the factorial
   Example: 5! = 5 * 4 * 2 * 1, where 2 * 5 == 10. Hence there is one trailing zero in 5!

"""
import pytest


class Solution(object):

    @staticmethod
    def compute(n: int) -> int:
        def factorial(n):
            result = 1
            for i in range(n, 1, -1):
                result *= i
            return result
        return 0


@pytest.mark.parametrize(
    'n,expected', [
        (5, 1)
    ]
)
def test_correctness(n: int, expected: int):
    observed = Solution.compute(n)
    assert observed == expected, f'Expected {expected}, not {observed}'
