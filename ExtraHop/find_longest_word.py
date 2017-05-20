from typing import Deque, Iterator, List, Optional, MutableSet, Tuple
from collections import deque


def find_longest_word(grid: List[str], words: List[str]) -> Optional[Tuple[str, List[Tuple[int, int]]]]:

    assert len(grid) == _grid_size and all(len(row) == _grid_size for row in grid)
    words = sorted(words, key=lambda word: len(word), reverse=True)

    for word in words:
        case_folded_word = word.casefold()
        first_letter = case_folded_word[0]
        eliminations: List[Optional[MutableSet[Tuple[int, int]]]] = [None] * (len(case_folded_word) - 1)
        for row in range(0, _grid_size):
            column = -1
            while True:
                column: int = grid[row][column + 1:].find(first_letter)
                if column < 0:
                    break  # next row
                path = deque()
                if _find_path(case_folded_word, 1, grid, (row, column), path, eliminations):
                    path.appendleft((row, column))
                    return word, path

    return None


_grid_size = 8
grid_area = _grid_size * _grid_size


def _coordinate(row: int, column: int) -> Tuple[int, int]:
    return column + 1, row + 1


def _find_path(
        word: str,
        index: int,
        grid: List[str],
        origin: Tuple[int, int],
        path: Deque[Tuple[int, int]],
        eliminations: List[MutableSet[Tuple[int, int]]]
) -> bool:

    if len(eliminations) == _grid_size * _grid_size:
        return False

    letter: str = word[index]

    for position in _moves_from(origin):
        eliminated = eliminations[index - 1]
        if eliminated and position in eliminated:
            continue
        if letter == grid[position[0]][position[1]]:
            if index == len(word) - 1:
                path.appendleft(position)
                return True
            if _find_path(word, index + 1, grid, position, path, eliminations):
                path.appendleft(position)
                return True
        if eliminated:
            eliminated.add(position)
        else:
            eliminations[index - 1] = {position}

    return False


def _moves_from(origin: Tuple[int, int]) -> Iterator[Tuple[int, int]]:

    row, column = origin

    for move in [
        (-1, +2),  # lt 1 up 2
        (-1, -2),  # lt 1 dn 2
        (-2, +1),  # lt 2 up 1
        (-2, -1),  # lt 2 dn 1
        (+1, +2),  # rt 1 up 2
        (+1, -2),  # rt 1 dn 2
        (+2, +1),  # rt 2 up 1
        (+2, -1),  # rt 2 dn 1
    ]:
        x, y = row + move[0], column + move[1]
        if 0 <= x < _grid_size and 0 <= y < _grid_size:
            yield x, y


if __name__ == '__main__':
    import sys

    test_grid: List[str] = [
        "qwertnui",
        "opaadfgh",
        "tklzxcvb",
        "nmrwfrty",
        "uiopasdf",
        "ghjolzxc",
        "vbnmqwer",
        "tyuiopas"
    ]

    print(find_longest_word(test_grid, sys.argv[1:]))
