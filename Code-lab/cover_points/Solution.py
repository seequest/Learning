""" [Reach](https://codelab.interviewbit.com/problems/reach/)

You are in an infinite 2D grid where you can move in any of the 8 directions :

 (x,y) to 
    (x + 1, y), 
    (x - 1, y), 
    (x, y + 1), 
    (x, y - 1), 
    (x - 1, y - 1), 
    (x + 1, y + 1), 
    (x - 1, y + 1), 
    (x + 1, y - 1) 

You are given a sequence of points and the order in which you need to cover the points. Give the minimum number of steps in which you can achieve it. You start from the first point.

Example :

Input : [(0, 0), (1, 1), (1, 2)]
Output : 2
It takes 1 step to move from (0, 0) to (1, 1). It takes one more step to move from (1, 1) to (1, 2).

"""

from typing import List, Sequence, Tuple


class Solution:

    # noinspection PyShadowingNames
    @staticmethod
    def cover_points(x: Sequence[int], y: Sequence[int]) -> List[Tuple[int, int]]:

        if len(x) != len(y):
            raise ValueError('expected len(x) == len(y)')

        moves: List[Tuple[int, int]] = []

        for i in range(0, len(x) - 1):

            distance = (x[i + 1] - x[i], y[i + 1] - y[i])

            if distance == (0, 0):
                continue

            delta = distance[0] - distance[1]

            if delta > 0:
                # we're moving farther along the x axis than the y axis
                moves.extend(
                    [
                        (-1 if distance[0] < 0 else 1, -1 if distance[1] < 0 else 1)
                    ] * abs(distance[1]) + [
                        (-1 if distance[0] < 0 else 1, 0)
                    ] * abs(delta)
                )
            elif delta == 0:
                # we're moving the same distance along the x and y axis
                moves.extend((
                    [
                        (-1 if distance[0] < 0 else 1, -1 if distance[1] < 0 else 1)
                    ] * abs(distance[0])
                ))
            else:
                # we're moving farther along the y axis than the x axis
                moves.extend((
                    [
                        (-1 if distance[0] < 0 else 1, -1 if distance[1] < 0 else 1)
                    ] * abs(distance[0]) + [
                        (0, -1 if distance[1] < 0 else 1)
                    ] * abs(delta)
                ))

        return moves

    @staticmethod
    def count_steps(x: Sequence[int], y: Sequence[int]) -> Sequence[Tuple[int, int]]:

        if len(x) != len(y):
            raise ValueError('expected len(x) == len(y)')

        steps = 0

        for i in range(0, len(x) - 1):

            steps += max(abs(x[i + 1] - x[i]), abs(y[i + 1] - y[i]))

        return steps


steps = Solution.count_steps(x=[-7, -13], y=[1, -5])
moves = Solution.cover_points(x=[-7, -13], y=[1, -5])

assert steps == len(moves)

print(f'steps = {steps}, moves = {moves}')
