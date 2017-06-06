""" [Factorial](https://codelab.interviewbit.com/problems/factorial/)

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

   This formula generalizes to any number base. For bases that are a power of a prime we have::

        z_{b}(n) = ⌊(1/m)∑⌊(n/p^k)⌋|k≥1⌋, where b = p^m, where p is prime

   The summation counts the number of factors of p in n!. For base b = 16 = 2^4, n = 100 this equation reduces to this::

        z_{16}(100) = ⌊1/4(⌊100/2⌋ + ⌊100/4⌋ + ⌊100/8⌋ + ⌊100/16⌋ + ⌊100/32⌋ + ⌊100/64⌋)⌋
                    = ⌊1/4(50 + 25 + 12 + 6 + 3 + 1)⌋
                    = ⌊97/4⌋
                    = 24

    When the base is not a power of a prime, counting the trailing zeroes is a little harder, but it can be done using
    exactly the same ideas. For base b = 10 = 2 * 5, n = 100 we have::

        z_{10}(100) = ⌊1/1(⌊100/5⌋ + ⌊100/25⌋)⌋
                    = ⌊(20 + 4)⌋
                    = ⌊97/4⌋
                    = 24

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
