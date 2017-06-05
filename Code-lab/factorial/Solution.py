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

2. The number of trailing zeros in a number is equal to the number of times it's divisible by 10. In the case of a
   factorial number this is equal to the number of times the number n in n! is divisible by 5.

   Example: 5! = 5 * 4 * 3 * 2 * 1
                 -               -

   Example: 10! = 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1
                  --                               -
                  10 / 5 = 2

                = 3,628,800

   Example: 20! = 20 * 19 * 18 * 17 * 16 * 15 * 14 * 13 * 12 * 11 * 10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1
                  --                                                                         -
                  20 / 5 = 4

                = 2,432,902,008,176,640,000

           100! = 93,326,215,443,944,152,681,699,238,856,266,700,490,715,968,264,381,621,468,592,963,895,217,599,993,
                  229,915,608,941,463,976,156,518,286,253,697,920,827,223,758,251,185,210,916,864,
                  000,000,000,000,000,000,000,000

                  100 / 5 = 20
                   20 / 5 =  4
                            --
                            24

   This formula generalizes to any number base.

References
----------
1. [Purplemath: Factorials and Trailing Zeroes](http://www.purplemath.com/modules/factzero.htm)
2. [Mathematics Stack Exchange: Number of trailing zeros in a factorial in base ‘b’](https://goo.gl/PpFtkr)
3. [Come on code on: Number of zeroes and digits in N Factorial in Base B](https://goo.gl/KPYsGW)

"""
import pytest


class Solution(object):

    @staticmethod
    def compute(integer: int) -> int:
        assert integer >= 0
        n = 0

        while integer >= 5:
            integer //= 5
            n += integer

        return n


@pytest.mark.parametrize(
    'n,expected', [
        (23, 4),
        (5, 1),
    ]
)
def test_correctness(n: int, expected: int):
    observed = Solution.compute(n)
    assert observed == expected, f'Expected {expected}, not {observed}'
