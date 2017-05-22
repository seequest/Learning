#!/usr/bin/env python36

""" ExtraHop Programming Problem--

Written by David Noble <david@thenobles.us>.

This module was developed and tested under Python 3.6 on macOS Sierra. Please ask for Python 2.7 code or code that
will run under Python 2.7 or Python 3.6, if you would prefer it. I mention this because I see that your deprecated
Python SDK is written for Python 2.7.3 or higher, but not Python 3.x.

mypy 0.511 clean

"""

import io
import random
import re

from collections import deque
from string import ascii_lowercase
from typing import Deque, Dict, Iterator, List, Mapping, Optional, MutableSet, Sequence, Tuple


def find_longest_word(grid: 'Grid', words: List[str]) -> Optional[Tuple[str, Tuple[Tuple[int, int], ...]]]:
    """ Find the longest word from a list of words that can be produced from an 8 x 8 grid using grid movement rules

    Words on the grid are located using this set of rules:
    
    1.	Start at any position in the grid, and use the letter at that position as the first letter in the candidate 
        word.
        
    2.	Move to a position in the grid that would be a valid move for a knight in a game of chess, and add the letter 
        at that position to the candidate word.
        
    3.	Repeat step 2 any number of times.
    
    This function preserves the contents of the `words` list. Length ties are broken by alphabetic sort order. Hence, 
    for example, if `foo` and `bar` are 
    
    * in the list of words and
    * the longest words to be found on a graph
    
    :func:`find_longest_word` will return `'bar'` and a tuple of the coordinates of its letters in the grid as its 
    result.

    Parameters
    ----------

    :param grid: A grid presumably filled with letters from some alphabet.
    :type grid: Grid
    
    :param words: A list of words that might be produced from letters on the 'grid' using grid moves.
    :type words: List[str]
    
    :return: Longest word that can be produces from letters on the 'grid' using grid moves; or :const:`None`, if no word
    can be produced from letters on the 'grid'.
    :rtype: Optional[Tuple[str, Tuple[Tuple[int, int]]]]
        
    Implementation notes
    ====================

    A grid should be thought of as a directed graph. The cells of a grid are its vertices. The movements that are 
    permitted from a cell on the graph are edges. The vertices are labeled by row, column coordinates and contain a 
    single piece of data: a letter drawn from some alphabet. Producing a word from the letters contained by the cells 
    on a grid amount to a graph traversal in the search for a path that traces out the word.
    
    In this solution we represent a grid with `Grid` class which encapsulates the small number of movement and lookup 
    operations that are required to trace out such a path. The `Grid` class also comes with a set of methods useful for
    testing: `Grid.generate`, `Grid.load`, and `Grid.save`. See the `Grid` class for specifics.
    
    Algorithm
    ---------
    `find_longest_word` non-destructively sorts words by length and alphabetic order. It then iterates over the set of
    positions from which a word might start as determined by `Grid.occurrences`. The search for a word from a starting 
    position is conducted by a local recursive function: `find_path`. All potential paths may be considered, but the 
    search is done depth-first and so the first complete path found will be taken. The order in which paths are 
    considered is fixed. This is based on the order of `Grid._moves`.
    
    One might have considered more advanced/exotic data structures and algorithms. We chose to keep the code and data 
    structures simple with an assumption that grid (graph) traversal operations are not performance critical. We are 
    content, for example, to consider all moves from a grid position sequentially without providing auxiliary lookup 
    capabilities or more advanced data structures. These might or might not be required based on space or time 
    requirements.
    
    An alternative
    --------------
    For each cell create a map of the coordinates of all reachable cells: a map of `Map[str, Tuple[int, int]]` keyed by
    letter. When moving from one letter of a word to another, consider only those cells with the required letter. As in
    this code, rule out known fruitless paths; those visited previously and found to be dead ends. 
    
    To speed searches over time one might also store (memoize) words/word stems; pre-populating some and building up 
    others over time. One might for example, create such a map of words/word stems from the output of `Grid.generate`. 
    Other words or word paths unknown to the author might likely be discovered over time.
    
    Here's a Wikipedia article that **might** be useful, should it be determined that this naive implementation is 
    insufficient from a time perspective.
    
    * [String searching algorithm](https://en.wikipedia.org/wiki/String_searching_algorithm)

    Command line
    ============
    
    This function may be executed from the command line using this syntax::
    
        python find_longest_word.py --grid <filename> <word>...
    
    Alternatively you may create a command argument file and reference it like this::
    
        python @<command-file-name>
        
    A command file should contain one argument per line as illustrated in `Programming-language-names.args`, included
    with this code::
     
        --grid
        grid-1
        ALGOL
        FORTRAN
        Simula

    Output includes the word found and the sequence of coordinates of the letters of the word found on the input grid.
    You will see that this command::
     
        python @Programming-language-names.args
        
    produces this output::
    
        ('FORTRAN', ((3, 4), (5, 3), (3, 2), (2, 0), (3, 2), (1, 3), (0, 5)))
        
    The coordinates written are zero-based row, column values, not unit-based column, row values as presented in 
    `PythonCodingProblem.docx`. 
    
    """

    def find_path(index: int, origin: Tuple[int, int]) -> Optional[Deque[Tuple[int, int]]]:
        """ Perform a recursive search for the tail end of a case-folded word from a position on the current grid 

        This local function economizes on stack space by relying on variables in its closure and short-circuiting 
        recursion along previously traversed paths. It is worth noting that words, even very long words in languages
        like German aren't that long. Stack space should not be an issue and the code is straight forward with this
        recursive implementation.

        Sidebar 
        -------
        According to the [BBC](http://www.bbc.com/news/world-europe-22762040) the longest German word was just lost 
        after an EU law change. It is 65 characters long, one more than the number of cells in a grid:: 
        
            Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz  

        In our experiments the `Grid.generate` function has not yet found a placement for this word in a grid; though
        there is a non-zero probability that the current implementation could. Alternatively one could update
        `Grid.generate` to consider all possible starting places and all possible paths from each of them. We leave
        this as an exercise.
                       
        Parameters
        ----------
        
        :param index: Index into the current case-folded word. 
        :type index: int
        
        :param origin: Grid coordinates from which to start the search.
        :type origin: Tuple[int, int]
        
        :return: Sequence of coordinates of the letters of the tail end of the cased-folded word starting at index or
        :const:`None`, if the current case-folded word cannot be found.
        :rtype: Optional[Tuple[Tuple[int, int]]] 

        """
        letter: str = case_folded_word[index]

        for position in grid.moves_from(origin):
            eliminated = eliminations[index - 1]
            if eliminated and position in eliminated:
                continue
            if letter == grid[position]:
                if index == end:
                    return deque((position,))
                path: Deque[Tuple[int, int]] = find_path(index + 1, position)
                if path is not None:
                    path.appendleft(position)
                    return path
            if eliminated:
                eliminated.add(position)
            else:
                eliminations[index - 1] = {position}

        return None

    words = sorted((word for word in words if word), key=lambda x: (-len(x), x))

    for word in words:

        case_folded_word: str = word.casefold()  # type: ignore
        end: int = len(case_folded_word) - 1
        first_letter: str = case_folded_word[0]
        eliminations: List[Optional[MutableSet[Tuple[int, int]]]] = [None] * (len(case_folded_word) - 1)

        for position in grid.occurrences(first_letter):
            path: Optional[Deque[Tuple[int, int]]] = find_path(1, position) if end > 0 else deque()
            if path is not None:
                path.appendleft(position)
                return word, tuple(path)

    return None


class Grid(object):
    """ Represents an 8 x 8 grid--presumably--containing letters drawn from one or more alphabets
    
    Grid entries are case folded when the grid is instantiated to ensure that case-insensitive comparisons can be made 
    with any (?) alphabet.
    
    Implementation notes
    --------------------
    A grid is internally represented as a List[List[str]]. A cell on the grid is accessed by its zero-based row, column
    coordinate: a `Tuple[int, int]`. All grids are 8 x 8 as indicated by the value of `Grid.size`: `8`.
    
    """
    __slots__ = ('_grid',)  # saves space; good practice for objects with no dynamic membership requirements

    def __init__(self, grid: Sequence[str]) -> None:

        assert len(grid) == Grid.size
        self._grid: List[List[str]] = []

        for record in grid:
            record = Grid._replace_whitespace('', record).casefold()  # type: ignore
            assert len(record) == Grid.size
            self._grid.append([c for c in record])

    def __getitem__(self, position: Tuple[int, int]) -> str:
        """ Get the letter in a cell on the current grid
        
        This method only partially implements `self[key]` semantics. Most notably slicing is not supported.
        
        :param position: row, column coordinates of a cell on the current grid
        :type position: Tuple[int, int]
        
        :return: The letter at 'position' on the current grid.
        :rtype: str
        
        :raises IndexError: If 'position' does not specify a location on the current grid.
         
        """
        return self._grid[position[0]][position[1]]

    def __str__(self) -> str:
        """ Get a human readable string representation of the current grid
         
        :return: A human readable string representation of the current grid
        :rtype: str
        
        """
        return '\n'.join(' '.join(column for column in row) for row in self._grid)

    @classmethod
    def generate(cls, words: Iterator[str]) -> Tuple['Grid', Mapping[str, Tuple[str, Tuple[Tuple[int, int],...]]]]:
        """ Generate a grid containing a set of words that can be found using grid movement rules
        
        Use this method to create test grids. An error message is produced for each word that cannot be put on the grid.
        Randomly generated ASCII characters are used to fill cells not filled by the words or--as explained in the 
        code--partial words we put on the grid.

        The implementation of this method is rudimentary, but useful for producing test grids and verifying correctness.
        
        Parameters
        ----------
        
        :param words: An iterator over the set of words to be put on to the grid.
        :type words: Iterator[str]
        
        :return: A grid object containing the words or partial words we put on the grid mixed with random ASCII fill
        characters.
        :rtype: Grid

        Example
        -------
        To see this method in action run these statements from a Python 3.6 REPL. A variable number of letters from
        the German word "Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz" will be placed on the
        grid::
        
            from find_longest_word import Grid, find_longest_word
            grid, paths = Grid.generate([
                'foo', 'bar', 'Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz'
            ])
            find_longest_word(grid, ['foo', 'bar', 'rindfleischetikettierun'])
            grid.save('grid-4')
          
        We're OK with this given our intent: generate some useful test grids. As indicated in the above REPL session 
        output you will find the results of example this REPL session in `grid-4'. We did not save the paths created
        for the words.
        
        """
        paths: Dict[str, Tuple[str, Tuple[Tuple[int, int], ...]]] = {}
        missing_data = chr(0)
        data = [[missing_data] * Grid.size for i in range(0, Grid.size)]

        for word in words:

            # Put this word on the grid starting at a random location

            origins = [(x, y) for x in range(0, Grid.size) for y in range(0, Grid.size)]
            path: List[Tuple[int, int]] = None
            row, column = None, None
            random.shuffle(origins)

            case_folded_word = word.casefold()  # type: ignore

            def put(letter: str, x: int, y: int) -> bool:
                if data[x][y] in (missing_data, letter):
                    data[x][y] = letter
                    return True
                return False

            index = 0

            for row, column in origins:
                if put(case_folded_word[0], row, column):
                    path = [None] * len(case_folded_word)
                    path[0] = row, column
                    index = 1
                    break

            if index == 0:
                print('could not find a place for any of the letters from', case_folded_word)
                paths[word] = None
            else:
                while index < len(case_folded_word):

                    # Try to put the letter at word[index] on the grid using a sequence of random grid moves
                    # One might try alternative paths the way function find_longest_word does, but we'll
                    # scope that out of this exercise and accept two things:
                    #
                    # * By selecting the first random letter placement that works and not trying alternatives path ways
                    #   out chance of failure is high.
                    # * In the failure case this algorithm will leave partial words on the grid.
                    #
                    # We're OK with this given our intent for this method: generate some random grids for testing.

                    moves = [move for move in cls._moves]
                    random.shuffle(moves)
                    put_letter = False

                    for x, y in moves:
                        x, y = row + x, column + y
                        if 0 <= x < Grid.size and 0 <= y < Grid.size:
                            if put(case_folded_word[index], x, y):
                                path[index] = row, column = x, y
                                put_letter = True
                                index += 1
                                break

                    if not put_letter:
                        break

                if index < len(case_folded_word):
                    print(
                        'only placed', index,  'out of', len(case_folded_word), 'letters from', case_folded_word,
                        ':', case_folded_word[:index]
                    )

                paths[word] = case_folded_word[:index], tuple(path[:index])

        for record in data:
            for column in range(0, Grid.size):
                if record[column] == missing_data:
                    record[column] = random.choice(ascii_lowercase)  # we do not use a larger alphabet like latin-1 :(

        return Grid([' '.join(row) for row in data]), paths

    @classmethod
    def load(cls, filename: str) -> 'Grid':
        """ Load a grid from a file
        
        :param filename: Name of a file containing a grid.
        :type filename: str
        
        :return: A Grid object
        :rtype: Grid
         
        """
        with io.open(filename) as istream:
            lines: List[str] = istream.readlines()
        return cls(lines)

    @classmethod
    def moves_from(cls, origin: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
        """ Enumerate the coordinates of cells that can be reached from a cell on the current grid
         
        Use this method to obtain the position of each element that can be legally reached from origin. Off-grid moves
        are--as one should expect--excluded from the enumeration.
        
        :param origin: A position on the current grid specified as a row, column coordinate
        :type origin: Tuple[int, int]

        :return: An iterator over the coordinates of cells that can be reached from 'origin'.
        :rtype: Iterator[Tuple[int, int]]
                
        """
        row, column = origin

        for move in cls._moves:
            x, y = row + move[0], column + move[1]
            if 0 <= x < cls.size and 0 <= y < cls.size:
                yield x, y

    def occurrences(self, letter: str) -> Iterator[Tuple[int, int]]:
        """ Enumerate the coordinates of each occurrence of a letter on the current grid
        
        :param letter: A letter which might or might not be on the grid.
        :type letter: str
         
        :return: An iterator over the coordinates of those cells containing 'letter'
        :rtype: Iterator[Tuple[int, int]]

        """
        for row, record in enumerate(self._grid, 0):
            column = -1
            while True:
                try:
                    column = record.index(letter, column + 1)
                except ValueError:
                    break
                yield row, column

    def save(self, filename: str) -> None:
        """ Save the current grid to a file 
        
        :param filename: Name of the file to which the current grid should be saved.
        :type filename: str
        
        :return: :const:`None`
        
        """
        with io.open(filename, 'w') as ostream:
            ostream.write(str(self))

    size = 8

    # region Protected

    _moves = [
        (-1, +2),  # lt 1 up 2
        (-1, -2),  # lt 1 dn 2
        (-2, +1),  # lt 2 up 1
        (-2, -1),  # lt 2 dn 1
        (+1, +2),  # rt 1 up 2
        (+1, -2),  # rt 1 dn 2
        (+2, +1),  # rt 2 up 1
        (+2, -1),  # rt 2 dn 1
    ]

    _replace_whitespace = re.compile('\s+').sub

    # endregion


if __name__ == '__main__':

    from argparse import ArgumentParser
    import sys

    parser = ArgumentParser(
        description='Find the longest word from a list of words that can be produced from an 8 x 8 grid of letters',
        fromfile_prefix_chars='@'
    )

    parser.add_argument('--grid', required=True)
    parser.add_argument('words', nargs='+')

    arguments = parser.parse_args(sys.argv[1:])

    print(find_longest_word(Grid.load(arguments.grid), arguments.words))
