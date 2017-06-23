""" [Arrange2]()

You are given a sequence of black and white horses, and a set of K stables numbered 1 to K. You have to accommodate the
horses into the stables in such a way that the following conditions are satisfied:

You fill the horses into the stables preserving the relative order of horses. For instance, you cannot put horse 1 into
stable 2 and horse 2 into stable 1. You have to preserve the ordering of the horses.

No stable should be empty and no horse should be left unaccommodated.

Take the product (number of white horses * number of black horses) for each stable and take the sum of all these
products. This value should be the minimum among all possible accommodation arrangements.

Example:

Input: {WWWB} , K = 2
Output: 0

Explanation:
We have 3 choices {W, WWB}, {WW, WB}, {WWW, B}
for first choice we will get 1*0 + 2*1 = 2.
for second choice we will get 2*0 + 1*1 = 1.
for third choice we will get 3*0 + 0*1 = 0.

Of the 3 choices, the third choice is the best option.

If a solution is not possible, then return -1

"""
from typing import List, Sequence, Tuple, Union
import sys
import pytest

Assignments = Tuple[int, List[List[int]]]


class Solution(object):

    @staticmethod
    def compute(horses: str, stables: int, list_assignments: bool = False) -> Union[int, Tuple[int, Sequence[str]]]:
        horses = horses.strip()
        if len(horses) < stables:
            return -1
        assignments = Solution.assign(horses, stables)
        return assignments[0] if list_assignments is False else (assignments[0], Solution.to_list(assignments, horses))

    @staticmethod
    def assign(horses: str, stables: int) -> Assignments:

        minimums = {}

        def cost(horse: int, stable: int):

            try:
                minimum = minimums[(horse, stable)]
                pass
            except KeyError:
                remaining_stables = stables - stable
                remaining_horses = len(horses) - horse

                if remaining_stables == 1:
                    total = len(horses) - horse
                    count = sum(1 for i in range(horse, len(horses)) if horses[i] == 'B')
                    minimum = count * (total - count), [[count, total - count]]
                elif remaining_horses == remaining_stables:
                    minimum = 0, [[1, 0] if horses[horse] == 'B' else [0, 1] for horse in range(horse, len(horses))]
                else:
                    minimum = sys.maxsize, []
                    current_stable = [0, 0]

                    for i in range(horse, len(horses) - 1):
                        color = 0 if horses[i] == 'B' else 1
                        current_stable[color] += 1
                        result = cost(i + 1, stable + 1)
                        value = result[0] + (current_stable[0] * current_stable[1])
                        if value < minimum[0]:
                            minimum = value, [current_stable.copy()] + result[1]

                minimums[(horse, stable)] = minimum

            return minimum

        return cost(0, 0)

    @staticmethod
    def to_list(assignments: Assignments, horses: str):
        result = []
        start = 0
        for stable in assignments[1]:
            end = start + stable[0] + stable[1]
            result.append(horses[start:end])
            start = end
        return result


@pytest.mark.parametrize(
    'horses, stables, expected', [
        ('WBWB\n', 2, (2, ['W', 'BWB'])),
        ('WWWB', 2, (0, ['WWW', 'B'])),
    ]
)
def test_correctness(horses: str, stables: int, expected: int):
    observed = Solution.compute(horses, stables, list_assignments=True)
    assert observed == expected
