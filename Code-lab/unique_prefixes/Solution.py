""" [Prefix](https://codelab.interviewbit.com/problems/prefix/)

Find shortest unique prefix to represent each word in the list.

Example:

Input: [zebra, dog, duck, dove]
Output: {z, dog, du, dov}
where we can see that
zebra = z
dog = dog
duck = du
dove = dov
NOTE : Assume that no word is prefix of another. In other words, the representation is always possible.

"""
import pytest
from collections import deque
from typing import List, Sequence


class Solution(object):

    @staticmethod
    def find_unique_prefixes(words: Sequence[str]) -> Sequence[str]:

        if len(words) == 0:
            return []

        if len(words) == 1:
            return [words[0][0]]

        items = list((index, word) for index, word in enumerate(words))
        queue = deque((('', items),))
        prefixes = {'': items}

        while len(queue):
            current_prefix, current_items = queue.popleft()
            end = len(current_prefix) + 1

            for index, word in current_items:
                prefix = word[0:end]
                try:
                    matches = prefixes[prefix]
                except KeyError:
                    prefixes[prefix] = [(index, word)]
                else:
                    if len(matches) == 1:
                        queue.append((prefix, matches))
                    matches.append((index, word))

            del prefixes[current_prefix]  # known to contain duplicates because it was in the queue

        unique_prefixes: List[str] = [None] * len(words)

        for prefix, items in prefixes.items():
            index, word = items[0]
            unique_prefixes[index] = prefix

        return unique_prefixes


@pytest.mark.parametrize(
    'words,expected', [
        (['bearcat', 'bert'], ['bea', 'ber']),
        (['zebra', 'dog', 'duck', 'dove'], ['z', 'dog', 'du', 'dov'])
    ]
)
def test_correctness(words: Sequence[str], expected: Sequence[str]):
    observed = Solution.find_unique_prefixes(words)
    assert list(observed) == expected
