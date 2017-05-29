import sys
from itertools import repeat
from typing import Iterator, Optional, Sized, Tuple, Union


class BitArray(Sized):

    __slots__ = ('_array', '_size')

    def __init__(self, size: int, value: Union[bool, int]) -> None:
        length = (size + 7) >> 3
        if value == 0:
            self._array = bytearray(length)
        else:
            self._array = bytearray(repeat((0xFF if value is True else value & 0xFF), length))
        self._size = size

    def __getitem__(self, item: int) -> bool:
        if not 0 <= item < self._size:
            raise IndexError()
        return (self._array[item >> 3] & (1 << (item & 0b111))) != 0

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, item: int, value: bool) -> None:
        if not (0 <= item < self._size):
            raise IndexError()
        if value:
            self._array[item >> 3] |= (1 << (item & 0b111))
        else:
            self._array[item >> 3] &= 0b11111111 ^ (1 << (item & 0b111))

    def items(self, value: bool, start: int, stop: int = None) -> Iterator[int]:

        size = self._size

        if not (0 <= start < size and 0 <= start < size):
            raise IndexError()

        # TODO: optimize using more elaborate bit operations

        array = self._array
        bit = start & 0b111
        index = start >> 3
        number = start

        stop = size if stop is None else min(stop, size)

        while number < stop:
            byte = array[index]

            while bit < 8:
                state = (byte & (1 << bit)) != 0
                if state is value:
                    number = (index << 3) + bit
                    if number > stop:
                        return
                    yield number
                bit += 1

            bit = 0
            index += 1
            number = index << 3


class Solution:

    @staticmethod
    def prime_sum(value: int) -> Tuple[int, int]:

        if Solution._is_prime is None:
            Solution._is_prime = Solution.generate_primes(10**7)

        if value < 4 or (value & 1) != 0 or value >= len(Solution._is_prime):
            raise ValueError()

        for low in range(1, (value >> 1) + 1):
            if Solution._is_prime[low]:
                high = value - low
                if Solution._is_prime[high]:
                    return low, high

        assert False, 'Failed to compute prime sum(' + str(value) + ')'

    @staticmethod
    def generate_primes(number: int) -> BitArray:

        is_prime = BitArray(number + 1, 0b10101010)
        is_prime[0] = is_prime[1] = False
        is_prime[2] = True

        def mark_composites(*args: int) -> None:
            stop = len(is_prime)
            for step in args:
                for i in range(step << 1, stop, step):
                    is_prime[i] = False

        mark_composites(3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)

        for candidate in is_prime.items(True, 101):
            i = 5

            while i * i <= candidate:
                if (candidate % i) == 0 or (candidate % (i + 2)) == 0:
                    candidate = is_prime[candidate] = False
                    break
                i += 6

            if candidate:
                mark_composites(candidate)

        return is_prime

    _is_prime: Optional[BitArray] = None


for n in range(4, sys.maxsize, 2):
    result = Solution.prime_sum(n)
    print(f'{n} = {result[0]} + {result[1]}')
