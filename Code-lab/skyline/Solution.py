""" [Skyline]()


"""
from typing import Sequence
from collections import namedtuple
import pytest


Line = namedtuple('Line', ('left', 'right', 'height'))


class Solution(object):

    @staticmethod
    def compute(lines: Sequence[Line]) -> Sequence[Line]:

        if len(lines) < 2:
            return lines

        lines = sorted(lines)
        result = [lines[0]]

        for i in range(1, len(lines)):

            previous_line = result[-1]
            current_line = lines[i]

            if current_line.left >= previous_line.right:

                if current_line.left > previous_line.right:
                    result.append(Line(previous_line.right, current_line.left, 0))  # fills gap in skyline

                result.append(current_line)

            elif current_line.left == previous_line.left:

                if current_line.height > previous_line.height:
                    result[-1] = Line(current_line.left, current_line.right, current_line.height)
                    if previous_line.right > current_line.right:
                        result.append(Line(current_line.right, previous_line.right, previous_line.height))
                elif current_line.right > previous_line.right:
                    result.append(Line(previous_line.right, current_line.right, current_line.height))

            elif current_line.left > previous_line.left:

                if current_line.height > previous_line.height:
                    result[-1] = Line(previous_line.left, current_line.left, previous_line.height)
                    result.append(current_line)
                    if current_line.right < previous_line.right:
                        result.append(Line(current_line.right, previous_line.right, previous_line.height))
                elif current_line.right > previous_line.right:
                    result.append(Line(previous_line.right, current_line.right, current_line.height))

            else:

                # Look backwards to cover the full scope of the current line

                height = current_line.height
                right = current_line.right
                left = current_line.left
                length = len(result)
                end = len(result)
                i = end - 1

                while result[i].left > left:
                    
                    if result[i].height < height:
                        i -= 1
                    else:
                        current_line = Line(result[i].right, right, height)

                        if end == length and i == length - 1:
                            result.append(current_line)
                        else:
                            del result[i + 2: end]
                            result[i + 1] = Line(current_line)

                        while left < result[i].left and result[i].height > height:
                            i -= 1

                        right = result[i].right
                        end = i + 1

                if result[i].height < height:
                    result[i] = Line(left=result[i].left, right=left, height=result[i].height)
                else:
                    left = result[i].right

                if end - i > 1:
                    del result[i + 2: end]
                    result[i + 1] = Line(left, right, height)

        return result

    @staticmethod
    def alt_compute(lines: Sequence[Line]) -> Sequence[Line]:

        if len(lines) < 2:
            return lines

        def merge(left: Sequence[Line], right: Sequence[Line]):
            pass

        return []

    @staticmethod
    def print_skyline(lines: Sequence[Line]):
        for line in lines:
            for i in range(line.right - line.left):
                print('|', ' ' * line.height, '|')


@pytest.mark.parametrize(
    'lines, expected', [
        (
            [
                Line(1, 5, 11), Line(2, 7, 6), Line(3, 9, 13)
            ],
            [
                Line(1, 3, 11), Line(3, 9, 13)
            ]
        ),
        (
            [
                Line(1, 5, 11), Line(2, 7, 6), Line(3, 9, 13), Line(12, 16, 7), Line(14, 25, 3), Line(19, 22, 18),
                Line(23, 29, 13), Line(24, 28, 4)
            ],
            [
                Line(1, 3, 11), Line(3, 9, 13), Line(9, 12, 0), Line(12, 16, 7), Line(16, 19, 3), Line(19, 22, 18),
                Line(22, 23, 3), Line(23, 29, 13)
            ]
        ),
        (
            [
                Line(1, 5, 11), Line(1, 6, 10), Line(2, 7, 6), Line(3, 9, 13), Line(12, 16, 7), Line(14, 25, 3),
                Line(19, 22, 18), Line(23, 29, 13), Line(24, 28, 4)
            ],
            [
                Line(1, 3, 11), Line(3, 9, 13), Line(9, 12, 0), Line(12, 16, 7), Line(16, 19, 3), Line(19, 22, 18),
                Line(22, 23, 3), Line(23, 29, 13)
            ]
        ),
        (
            [
                Line(1, 5, 11), Line(1, 6, 12), Line(2, 7, 6), Line(3, 9, 13), Line(12, 16, 7), Line(14, 25, 3),
                Line(19, 22, 18), Line(23, 29, 13), Line(24, 28, 4)
            ],
            [
                Line(1, 3, 12), Line(3, 9, 13), Line(9, 12, 0), Line(12, 16, 7), Line(16, 19, 3), Line(19, 22, 18),
                Line(22, 23, 3), Line(23, 29, 13)
            ]
        ),
        (
            [
                Line(1, 5, 11), Line(1, 6, 10), Line(2, 7, 6), Line(3, 9, 13), Line(12, 16, 7), Line(14, 25, 3),
                Line(19, 22, 18), Line(23, 29, 13), Line(24, 28, 4)
            ],
            [
                Line(1, 3, 11), Line(3, 9, 13), Line(9, 12, 0), Line(12, 16, 7), Line(16, 19, 3), Line(19, 22, 18),
                Line(22, 23, 3), Line(23, 29, 13)
            ]
        ),
        (
            [Line(0, 3, 3), Line(1, 4, 4), Line(2, 7, 1), Line(5, 6, 5)],
            [Line(0, 1, 3), Line(1, 4, 4), Line(4, 5, 1), Line(5, 6, 5), Line(6, 7, 1)]
        ),
    ]
)
def test_correctness(lines: Sequence[Line], expected: Sequence[int]):
    observed = Solution.compute(lines)
    try:
        assert observed == expected
    except AssertionError:
        raise
    Solution.print_skyline(observed)
