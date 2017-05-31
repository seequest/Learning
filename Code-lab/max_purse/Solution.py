""" [Maxcoin](https://codelab.interviewbit.com/problems/maxcoin/)

There are N coins (Assume N is even) in a line. Two players take turns to take a coin from one of the ends of the line until there are no more coins left. The player with the larger amount of money wins. Assume that you go first.

Write a program which computes the maximum amount of money you can win.

Example:

suppose that there are 4 coins which have value
1 2 3 4
now you are first so you pick 4
then in next term
next person picks 3 then
you pick 2 and
then next person picks 1
so total of your money is 4 + 2 = 6
next/opposite person will get 1 + 3 = 4
so maximum amount of value you can get is 6


Algorithm for a player move
---------------------------
Let F(i, j) represent the maximum value the user can collect from i'th coin to j'th coin.

    F(i, j) => max(
        Vi + min(F(i + 2, j), F(i + 1, j - 1)),
        Vj + min(F(i + 1, j - 1), F(i, j - 2))
    )

"""
import pytest

from itertools import product
from typing import Any, List, Sequence, Tuple


class Solution(object):

    @staticmethod
    def optimal_strategy(coins: Sequence[int]) -> int:

        count = len(coins)
        table: List[List[int]] = list([0] * count for i in range(count))

        def value_of(i: int, j: int) -> int:
            return table[i][j] if i <= j else 0

        for index in range(count):
            row = 0

            for column in range(index, count):

                x = value_of(row + 2, column)
                y = value_of(row + 1, column - 1)
                z = value_of(row, column - 2)

                table[row][column] = max(coins[row] + min(x, y), coins[column] + min(y, z))
                row += 1

        return table[0][count - 1]

    @staticmethod
    def naive_strategy(coins: Sequence[int]) -> int:
        tail = len(coins) - 1
        head = 0
        purse = [0, 0]

        player = 0

        while head <= tail:
            coin, head, tail = Solution._select_coin(coins, head, tail)
            purse[player] += coin
            player ^= 1

        return max(*purse)

    @staticmethod
    def _select_coin(coins: Sequence[int], head: int, tail: int) -> Tuple[int, int, int]:
        if coins[head] > coins[tail]:
            coin = coins[head]
            head += 1
        else:
            coin = coins[tail]
            tail -= 1
        return coin, head, tail


@pytest.mark.parametrize('strategy,args', product(['naive_strategy', 'optimal_strategy'], [
    (22, [8, 15, 3, 7]),
    (4, [2, 2, 2, 2]),
    (42, [20, 30, 2, 2, 2, 10]),
    (501, [1, 100, 500, 10]),
    (6, [1, 2, 3, 4]),
    (15, [5, 3, 7, 10]),
]))
def test_correctness(strategy: str, args: Any) -> None:
    expected, coins = args
    observed = getattr(Solution, strategy)(coins)
    assert observed == expected, f'{strategy}: expected {expected}, not {observed}'
