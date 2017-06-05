""" [LengthLast](https://codelab.interviewbit.com/problems/lengthlast/)

Given a string s consists of upper/lower-case alphabets and empty space characters ' ', return the length of last word
in the string.

If the last word does not exist, return 0.

Note: A word is defined as a character sequence consists of non-space characters only.

Example:

Given s = "Hello World",

return 5 as length("World") = 5.

Please make sure you try to solve this problem without using library functions. Make sure you only traverse the string once.

18 min.

"""
import pytest


class Solution(object):

    @staticmethod
    def compute(words: str) -> int:
        length = len(words)
        if length > 0:
            for end in range(length - 1, -1, -1):
                if words[end] != ' ':
                    for start in range(end, -1, -1):
                        if words[start] == ' ':
                            return end - start
                    return end + 1
        return 0


@pytest.mark.parametrize(
    'words,expected', [
        ('compute clever alternative', len('alternative')),
        ('   compute clever alternative', len('alternative')),
        ('compute   clever  alternative', len('alternative')),
        ('compute clever alternative   ', len('alternative')),
        ('', 0),
        ('            ', 0),
        ('a', 1),
        ('   a', 1),
        ('a     ', 1),
    ]
)
def test_correctness(words: str, expected: int):
    observed = Solution.compute(words)
    assert observed == expected, f'Expected {expected}, not {observed}'
