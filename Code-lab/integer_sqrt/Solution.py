""" Compute the integer square root of an integer number

We present two solutions. :func:`isqrt_1` is based on a binary search algorithm. :func:`isqrt_2` uses [Newton-Raphson's 
method](https://goo.gl/khQvnp) for computing square roots. Each algorithm converges rapidly. Newton Raphson's method
is better, especially for very large numbers, but both algorithms are good:
 
    Binary search:
    isqrt_1(9,223,372,036,854,775,807) = 3,037,000,499, converged in 62 iterations
    test_performance: 2.426 seconds / 1,000 iterations
    
    Newton-Raphson method:
    isqrt_2(9,223,372,036,854,775,807) = 3,037,000,499, converged in 36 iterations
    test_performance: 1.801 / 1,000 iterations

    Newton-Raphson takes about 75% of the time that Binary search takes, about a 35% performance boost. 
    
"""

import sys
from math import floor, sqrt
from timeit import timeit
from typing import Callable, Tuple


def isqrt_1(number: int) -> Tuple[int, int]:
    if number < 0:
        raise ValueError(f'Expected a non-negative integer, not {number}')

    if number < 1:
        return 0, 0

    if number < 4:
        return 1, 0

    upper_bound = number >> 1
    lower_bound = 2
    iterations = 0

    while upper_bound - lower_bound > 1:

        midpoint = (lower_bound + upper_bound) >> 1
        value = midpoint * midpoint
        iterations += 1

        if value == number:
            return midpoint, iterations

        if value < number:
            lower_bound = midpoint
        else:
            upper_bound = midpoint

    return lower_bound, iterations


def isqrt_2(number: int) -> Tuple[int, int]:

    if number < 0:
        raise ValueError(f'Expected a non-negative integer, not {number}')

    if number < 1:
        return 0, 0

    if number < 4:
        return 1, 0

    last_result = number >> 1
    iterations = 0

    while True:
        current_result = (last_result + number // last_result) >> 1
        iterations += 1
        if current_result - last_result in (0, 1):
            return last_result, iterations
        last_result = current_result


def test_correctness(isqrt: Callable[[int], Tuple[int, int]]) -> None:

    for number in tuple(range(0, 1000)) + (sys.maxsize,):
        observed, iterations = isqrt(number)
        expected = int(floor(sqrt(number)))
        assert isinstance(observed, int), f'Expected integer_sqrt({number:,}) -> int, not {type(observed).__name__}'
        assert observed == expected, f'Expected integer_sqrt({number:,}) = {expected:,}, not {observed:,}'
        print(f'integer_sqrt({number:,}) = {observed:,}, converged in {iterations} iterations')


def test_performance(isqrt: str) -> None:

    print(timeit(
        stmt=f'''for number in tuple(range(0, 1000)) + (sys.maxsize,): {isqrt}(number)''',
        globals=globals(),
        number=1000
    ))

if __name__ == '__main__':

    test_correctness(isqrt_1)
    test_correctness(isqrt_2)

    test_performance('isqrt_1')
    test_performance('isqrt_2')
