"""

Given N and M find all stepping numbers in range N to M

The stepping number:

A number is called as a stepping number if the adjacent digits have a difference of 1.
e.g 123 is stepping number, but 358 is not a stepping number

Example:

N = 10, M = 20
all stepping numbers are 10 , 12
Return the numbers in sorted order.

"""
from collections import deque
from timeit import Timer, timeit
from typing import Sequence


class Solution(object):

    @staticmethod
    def compute_stepping_numbers(n: int, m: int) -> Sequence[int]:

        if m < n:
            m, n = n, m

        result = []

        for number in range(n, m + 1):
            value = abs(number)
            is_stepping = True
            next_digit = value % 10

            while next_digit < value:
                current_digit = next_digit
                value //= 10
                next_digit = value % 10
                if abs(current_digit - next_digit) != 1:
                    is_stepping = False
                    break

            if is_stepping:
                result.append(number)

        return result

    @staticmethod
    def search_stepping_numbers(n: int, m: int) -> Sequence[int]:

        assert 0 <= m and 0 <= n <= m

        if m < 10:
            return list(range(n, m + 1))

        queue = deque()
        result = []

        for number in range(0, 10):
            if n <= number <= m:
                result.append(number)
            if number > 0:
                queue.append(number)

        while len(queue) > 0:
            number = queue.popleft()

            if number > m:
                break

            digit = number % 10

            if digit > 0:
                step_dn = 10 * number + digit - 1
                if n <= step_dn <= m:
                    result.append(step_dn)
                queue.append(step_dn)

            if digit < 9:
                step_up = 10 * number + digit + 1
                if n <= step_up <= m:
                    result.append(step_up)
                queue.append(step_up)

        return result


def test_performance(method: str, m, n) -> Timer:
    return timeit(stmt=f'Solution.{method}({m}, {n})', globals=globals(), number=100)


# Case 1 : [2, 8]

expected = [2, 3, 4, 5, 6, 7, 8]

observed = Solution.search_stepping_numbers(2, 8)
print(f'Solution.search_stepping_numbers(2, 8) = {observed}')

assert observed == expected, f'expected: {expected}'

# Case 2 : [1, 1000]

expected = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98, 101, 121, 123, 210,
    212, 232, 234, 321, 323, 343, 345, 432, 434, 454, 456, 543, 545, 565, 567, 654, 656, 676, 678, 765, 767, 787, 789,
    876, 878, 898, 987, 989
]

observed = Solution.search_stepping_numbers(1, 1000)
print(f'Solution.search_stepping_numbers(1, 1000) = {observed}')

assert observed == expected, f'expected: {expected}'

# Performance

for name in 'compute_stepping_numbers', 'search_stepping_numbers':
    timer = test_performance(method=name, m=1, n=1000000)
    print(f'{name}: {timer}')
