""" [Gas]()

There are N gas stations along a circular route, where the amount of gas at station i is gas[i].

You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from station i to its next station
(i+1). You begin the journey with an empty tank at one of the gas stations.

Return the minimum starting gas station’s index if you can travel around the circuit once, otherwise return -1.

You can only travel in one direction. i to i+1, i+2, ... n-1, 0, 1, 2..
Completing the circuit means starting at i and ending up at i again.

Example :

Input :
      Gas :   [1, 2]
      Cost :  [2, 1]

Output : 1

If you start from index 0, you can fill in gas[0] = 1 amount of gas. Now your tank has 1 unit of gas. But you need
cost[0] = 2 gas to travel to station 1.

If you start from index 1, you can fill in gas[1] = 2 amount of gas. Now your tank has 2 units of gas. You need
cost[1] = 1 gas to get to station 0. So, you travel to station 0 and still have 1 unit of gas left over. You fill in
gas[0] = 1 unit of additional gas, making your current gas = 2. It costs you cost[0] = 2 to get to station 1, which you
do and complete the circuit.

Observations
------------

1. Must be able to move from i to i + 1 ... and then back to i without running out of gas

"""
from typing import Any, Sequence

import pytest


class Solution(object):

    @staticmethod
    def compute_1(gas: Sequence[int], cost: Sequence[int]) -> Any:
        # O(n^2)

        assert len(gas) == len(cost)

        for i in range(0, len(gas)):
            tank = 0
            for j in range(0, len(gas)):
                j = (i + j) % len(gas)
                tank -= cost[j]
                tank += gas[j]
                if tank < 0:
                    break
            if tank >= 0:
                return i

        return -1

    @staticmethod
    def compute_2(gas: Sequence[int], cost: Sequence[int]) -> Any:
        """

        Computes the difference between the available gas and the gas required to circumnavigate the track::

            total = sum(gas[i] - cost[i] for i in range(0, len(gas))

        Simultaneously computes the station at which the gas level is lowest when circumnavigating the track when
        starting from index zero.

        :return: index of the station one ahead of the station where we've got the lowest gas level, if there's
        enough gas to circumnavigate the track (i.e., when `total >= 0`); otherwise -1.
        :rtype: int

        """
        # O(n)
        assert len(gas) == len(cost)

        minimum = tank = 0
        index = -1

        for i in range(0, len(gas)):
            tank += gas[i] - cost[i]
            if tank < minimum:
                minimum = tank
                index = i

        return index + 1 if tank >= 0 else -1


@pytest.mark.parametrize(
    'gas, cost, expected', [
        (
            [
                 39, 959, 329, 987, 951, 942, 410, 282, 376, 581, 507, 546, 299, 564, 114, 474, 163, 953, 481, 337, 395,
                679,  21, 335, 846, 878, 961, 663, 413, 610, 937,  32, 831, 239, 899, 659, 718, 738,   7, 209
            ],
            [
                 39, 862, 783, 134, 441, 177, 416, 329,  43, 997, 920, 289, 117, 573, 672, 574, 797, 512, 887, 571, 657,
                420, 686, 411, 817, 185, 326, 891, 122, 496, 905, 910, 810, 226, 462, 759, 637, 517, 237, 884
            ],
            -1
        ),
        ([1, 2], [2, 1], 1),
        (
            [
                 98, 204, 918,  18,  17,  35, 739, 913,  14,  76, 555, 333, 535, 653, 667,  52, 987, 422, 553, 599, 765,
                494, 298,  16, 285, 272, 485, 989, 627, 422, 399, 258, 959, 475, 983, 535, 699, 663, 152, 606, 406, 173,
                671, 559, 594, 531, 824, 898, 884, 491, 193, 315, 652, 799, 979, 890, 916, 331,  77, 650, 996, 367,  86,
                767, 542, 858, 796, 264,  64, 513, 955, 669, 694, 382, 711, 710, 962, 854, 784, 299, 606, 655, 517, 376,
                764, 998, 244, 896, 725, 218, 663, 965, 660, 803, 881, 482, 505, 336, 279
            ],
            [
                 98, 273, 790, 131, 367, 914, 140, 727,  41, 628, 594, 725, 289, 205, 496, 290, 743, 363, 412, 644, 232,
                173,   8, 787, 673, 798, 938, 510, 832, 495, 866, 628, 184, 654, 296, 734, 587, 142, 350, 870, 583, 825,
                511, 184, 770, 173, 486,  41, 681,  82, 532, 570,  71, 934,  56, 524, 432, 307, 796, 622, 640, 705, 498,
                109, 519, 616, 875, 895, 244, 688, 283,  49, 946, 313, 717, 819, 427, 845, 514, 809, 422, 233, 753, 176,
                 35,  76, 968, 836, 876, 551, 398,  12, 151, 910, 606, 932, 580, 795, 187
            ],
            32
        )
    ]
)
def test_correctness(gas, cost: Sequence[Any], expected: Any) -> None:
    observed = Solution.compute_2(gas, cost)
    assert observed == expected, f'Expected {expected}, not {observed}'
