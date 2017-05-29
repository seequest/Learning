""" [Bulbs](https://codelab.interviewbit.com/problems/bulbs/)

N light bulbs are connected by a wire. Each bulb has a switch associated with it, however due to faulty wiring, a switch
also changes the state of all the bulbs to the right of current bulb. Given an initial state of all bulbs, find the
minimum number of switches you have to press to turn on all the bulbs. You can press the same switch multiple times.

Note : 0 represents the bulb is off and 1 represents the bulb is on.

Example:

Input : [0 1 0 1]
Return : 4

Explanation :
    press switch 0 : [1 0 1 0]
    press switch 1 : [1 1 0 1]
    press switch 2 : [1 1 1 0]
    press switch 3 : [1 1 1 1]

"""
from typing import MutableSequence


class Solution(object):

    @staticmethod
    def turn_on(bulbs: MutableSequence[int]) -> int:

        if len(bulbs) == 0:
            return 0

        if len(bulbs) == 1:
            return 1 if bulbs[0] else 0

        start = 0
        count = 0
        value = 0

        while True:
            try:
                start = bulbs.index(value, start)
            except ValueError:
                break
            count += 1
            value = 0 if value is 1 else 1

        return count


Solution.turn_on(bulbs=[1, 1, 0, 0, 1, 1, 0, 0, 1])
Solution.turn_on(bulbs=[1, 1, 1, 1, 1, 1, 1, 1, 1])
Solution.turn_on(bulbs=[0, 0, 0, 0, 0, 0, 0, 0, 0])
