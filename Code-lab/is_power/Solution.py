""" [Power2](https://codelab.interviewbit.com/problems/power2/)

Given a positive integer which fits in a 32 bit signed integer, find if it can be expressed as A^P where P > 1 and
A > 0. A and P both should be integers.

"""
from math import sqrt


class Solution(object):

    def power(self, number: int) -> bool:

        assert 0 < number <= self.max_int

        if number == 1:
            return True  # infinitely many because 1**n is one for any real number n

        if number == 2:
            return False

        if (number & (number - 1)) == 0:
            return True  # number is a power of two and can therefore be expressed as 2**n

        if number < 9:
            return False

        # all remaining candidates are less than or equal to the sqrt(n) and greater than 2

        candidate = sqrt(number)

        if candidate.is_integer():
            return True

        skip = set()

        for candidate in range(3, int(candidate)):
            if candidate in skip:
                continue
            if number % candidate == 0:
                value = candidate * candidate
                skip.add(value)
                while value < number:
                    value *= candidate
                    skip.add(value)
                if value == number:
                    return True

        return False

    max_int = 2**32 - 1


solution = Solution()

assert solution.power(1)
assert not solution.power(2)
assert not solution.power(3)

for n in range(2, 65535):
    for p in range(2, 65535):
        number = n**p
        if number > Solution.max_int:
            break
        assert solution.power(int(number))
