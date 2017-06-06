""" [Interleave](https://codelab.interviewbit.com/problems/interleave/)

Given s1, s2, s3, find whether s3 is formed by the interleaving of s1 and s2.

Example,
Given:

s1 = "aa bc c",
s2 = "db bc a",
When s3 = "aa db bc bc ac", return true.

aa
db
bc
bc
a
c

s1 = "aa b c c",
s2 = "db b c a",
When s3 = "aa db b b ac cc", return false.

aa
db
b
b

Return 0 / 1 ( 0 for false, 1 for true ) for this problem

Observations
------------

1. Assumption: s1 and s2 are the same length, n
   Bad assumption: s1 and s2 may be any two lengths

2. If s3 is an interleaving of s1 and s2, the length of s3 is len(s1) + len(s2)

3. We can match any substring of s1 with any substring of s2

   substring(s1) + substring(s2)  # OK

4. We can reverse the order of the substrings of s1 and s2

   substring(s2) + substring(s1)  # OK

5. We cannot reverse a substring

   reverse(substring(s1))         # NOT OK

6. The substring lengths must be the same
   Bad assumption: the substring lengths may be any size, including zero

   0 <= len(substring(s1)) <= len(s1)
   0 <= len(substring(s2)) <= len(s2)
   len(substring(s1)) > 0 or len(substring(s2)) > 0

"""
from typing import Deque, Optional, Tuple

import pytest
from collections import deque


class Solution(object):

    @staticmethod
    def compute(string_1: str, string_2: str, string_3: str) -> int:

        if len(string_3) != len(string_1) + len(string_2):
            return 0

        match, sequence = Solution.find(string_3, string_1, string_2)
        return 1 if match is True else 0

    @staticmethod
    def find(interleaving: str, string_1: str, string_2: str) -> Tuple[bool, Optional[Deque[Tuple[str, str]]]]:

        if len(string_1) == 0 and len(string_2) == 0:
            return True, deque()

        if len(string_1) == 0:
            return (True, deque((string_2, ''))) if interleaving == string_2 else (False, None)

        if len(string_2) == 0:
            return (True, deque((string_1, ''))) if interleaving == string_1 else (False, None)

        for length_1 in range(1, len(string_1) + 1):
            substring_1 = string_1[0: length_1]

            for length_2 in range(1, len(string_2) + 1):
                substring_2 = string_2[0: length_2]

                if interleaving.startswith(substring_1 + substring_2):
                    length = len(substring_1) + len(substring_2)
                    match, sequence = Solution.find(interleaving[length:], string_1[length_1:], string_2[length_2:])
                    if match:
                        sequence.appendleft((substring_1, substring_2))
                        return True, sequence

                if interleaving.startswith(substring_2 + substring_1):
                    length = len(substring_1) + len(substring_2)
                    match, sequence = Solution.find(interleaving[length:], string_1[length_1:], string_2[length_2:])
                    if match:
                        sequence.appendleft((substring_2, substring_1))
                        return True, sequence

        return False, None


@pytest.mark.parametrize(
    'set_1,set_2,set_3,expected', [
        ('aabcc', 'dbbca', 'aadbbcbcac', 1),
        ('aabcc', 'dbbca', 'aadbbbaccc', 0),
        (
            'noUdRp97xFvpifeSXGwOjcVNhHo9N2D',
            '6iZItw9A3fj86uYx04tvWKLtl9BK',
            'n6ioUdRpZ97ItwxF9Av3fj86upYxif0eS4XtvWKLtlG9wOBKjcVNhHo9N2D',
            1
        ),
        (
            'gvoGOejMO8utLrKUs2ZEU',
            'J',
            'gJvoGOejMO8utLrKUs2ZEU',
            1
        ),
    ]
)
def test_correctness(set_1: str, set_2: str, set_3: str, expected: int) -> None:
    observed = Solution.compute(set_1, set_2, set_3)
    assert observed == expected, f'Expected {expected}, not {observed}'
