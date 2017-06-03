""" [GCD] ()

Given 2 non negative integers m and n, find gcd(m, n)

GCD of 2 integers m and n is defined as the greatest integer g such that g is a divisor of both m and n.
Both m and n fit in a 32 bit signed integer.

Example

m : 6
n : 9

GCD(m, n) : 3
NOTE : DO NOT USE LIBRARY FUNCTIONS

Observations
-------------
The greatest common denominator, g, of two non-negative numbers has these properties:

    g <= min(m, n)
    is odd, if m or n are odd

We need not check numbers below min(m, n) / 2

Research
--------
Euclid solved this problem in 300 B.C. This algorithm converges in many fewer steps than the prime factorizations
algorithm. "In practice, [the prime factorizations algorithm] is only feasible for small numbers; computing prime
factorizations in general takes far too long. One might consider working from a table of prime numbers in the range
of a 32-bit signed integer. There are just 455,042,511 prime numbers below 10,000,000,000 > 2,147,483,647 = 2**31 - 1,
the maximum value of a non-negative 32-bit signed integer.

Factoid
-------
[2**31 - 1](https://en.wikipedia.org/wiki/2,147,483,647) is itself a prime number. It is one of only four known double
Mersenne numbers, a number of the form:

    2 ** (2**p - 1) - 1, where p is a prime number

To see this note that:

    2 ** 31 - 1 = 2 ** (2 ** 5 - 1) - 1
    5 is a prime number

"""
from typing import Tuple
import pytest


class Solution(object):

    @staticmethod
    def compute(m: int, n: int) -> Tuple[int, int]:

        assert m >= 0 and n >= 0

        if m == n:
            return m, 0

        if m == 0 or n == 0:
            return max(m, n), 0

        if (m & 1) == 0 and (n & 1) == 0:
            m1 = m & (m ^ (m - 1))
            n1 = n & (n ^ (n - 1))

            if m == m1 and n == n1:
                return min(m, n), 0

        iterations = 0
        gcd = min(m, n)
        n = max(m, n)

        while True:
            iterations += 1
            n %= gcd
            if n == 0:
                break
            if n < gcd:
                m = gcd
                gcd = n
                n = m

        return gcd, iterations


@pytest.mark.parametrize(
    'm,n,expected', [
        # Zero is the greatest common denominator of itself
        (0, 0, 0),
        # The greatest common denominator of any number (n) and zero is n
        (0, 2, 2),
        (2, 0, 2),
        # The greatest common denominator of any two primes (P1 and P2) is 1
        (2, 3, 1),
        (3, 2, 1),
        (11, 13, 1),
        (13, 11, 1),
        # The greatest common denominate of any two powers of 2 is the minimum of the two powers of 2 and special cased
        (2 ** 31, 2 ** 30, 2 ** 30),
        (2 ** 30, 2 ** 31, 2 ** 30),
        # In all other cases the greatest common denominator is the product of the primes they have in common
        (2 * 7 * 13, 2 * 7 * 11 * 11, 2 * 7),
        (2 * 7 * 11 * 11, 2 * 7 * 13, 2 * 7),
        (2 * 2 * 13 * 13 * 11, 2 * 2 * 13 * 13, 2 * 2 * 13 * 13),
        (2**32 - 1, 13 * 11 * 7 * 5 * 3 * 2, 15),  # largest 32-bit number
        (13 * 11 * 7 * 5 * 3 * 2, 2**32 - 1, 15),  # ditto
    ]
)
def test_correctness(m: int, n: int, expected: int) -> None:
    observed, iterations = Solution.compute(m, n)
    assert observed == expected, f'Expected that gcd({m}, {n}) => {expected}, not {observed}'
