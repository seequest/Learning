""" [Power](https://codelab.interviewbit.com/problems/power/)

Find if Given number is power of 2 or not.
More specifically, find if given number can be expressed as 2^k where k >= 1.

Input:

number length can be more than 64, which mean number can be greater than 2 ^ 64 (out of long long range)
Output:

return 1 if the number if a power of 2 else return 0

Example:

Input : 128
Output : 1

"""
import pytest


class Solution(object):

    @staticmethod
    def is_power_of_2(number: int) -> bool:
        assert number > 0
        return (number & (number ^ (number - 1))) == number


@pytest.mark.parametrize(
    'number,expected', [
        (0b1, True),
        (0b10, True),
        (0b11, False),
        (0b100, True),
        (0b1000, True),
        (0b10000, True),
        (0b100000, True),
        (0b1000000, True),
        (0b10000000, True),
        (0b100000000, True),
        (0b1000000000, True),
        (0b10000000000, True),
        (0b100000000000, True),
        (0b1000000000000, True),
        (0b10000000000000, True),
        (0b100000000000000, True),
        (0b1000000000000000, True),
        (0b10000000000000000, True),
        (0b100000000000000000, True),
        (0b1000000000000000000, True),
        (0b10000000000000000000, True),
        (0b100000000000000000000, True),
        (0b1000000000000000000000, True),
        (0b10000000000000000000000, True),
        (0b100000000000000000000000, True),
        (0b1000000000000000000000000, True),
        (0b1000000000000000000000000000000, True),  # 31-bits
        (0b10000000000000000000000000000000, True),  # 32-bits
        (0b10000000000000000100000000000000, False),
        (0b1000000000000000000000000000000000000000000000000000000000000000, True),  # 64-bits
        (0b1000000000000000000000000000000000000000000000000100000000000000, False),
        (0x80000000000000000000000000000000, True),  # 128-bits
        (0x80000000000000010000000000000000, False),  # 128-bits
    ]
)
def test_correctness(number: int, expected: int):
    observed = Solution.is_power_of_2(number)
    assert observed == expected, f'Expected to find that {bin(number)} {"is" if expected else "is not"} a power of 2'
