""" ExtraHop Programming Problem

Written by David Noble <david@thenobles.us>.

This module was developed and tested under Python 3.6 on macOS Sierra.

"""

import io
import random
import re

from collections import deque
from string import ascii_lowercase
from typing import Deque, Iterator, List, Optional, MutableSet, Sequence, Tuple


def find_longest_word(grid: 'Grid', words: List[str]) -> Optional[Tuple[str, Tuple[Tuple[int, int]]]]:
    """ Find the longest word from a list of words that can be produced from an 8 x 8 grid using grid movement rules

    Words on the grid are located using this set of rules:
    
    1.	Start at any position in the grid, and use the letter at that position as the first letter in the candidate 
        word.
        
    2.	Move to a position in the grid that would be a valid move for a knight in a game of chess, and add the letter 
        at that position to the candidate word.
        
    3.	Repeat step 2 any number of times.
    
    Length ties are broken by alphabetic sort order. Hence, for example, if `foo` and `bar` are 
    
    * in the list of words and
    * the longest words to be found on a graph
    
    this function will return `bar` as its result.

    Grid representation
    ===================
    
    A grid is represented by the `Grid` class which encapsulates a small number of grid movement/lookup operations and
    comes with a set of methods that are useful for testing: `Grid.generate`, `Grid.load`, and `Grid.save`. See the
    `Grid` class for specifics.

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
        
    The coordinates written are zero-based, not unit-based as presented in `PythonCodingProblem.docx`. 
    
    """

    def find_path(index: int, origin: Tuple[int, int]) -> Optional[Deque[Tuple[int, int]]]:
        """ Perform a recursive search for the tail end of a case-folded word from a position on the current grid 

        We economize on stack space by relying on variables in the closure of this function. It is worth noting
        that words, even very long words in languages like German aren't that long. Hence, stack space
        should not be an issue. 
        
        Sidebar 
        -------
        According to the [BBC](http://www.bbc.com/news/world-europe-22762040) the longest German word was just lost 
        after an EU law change. This word is 65 characters long, one more than the number of cells in a grid:: 
        
            Rindfleischetikettierungsueberwachungsaufgabenuebertragungsgesetz  

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
                path = find_path(index + 1, position)
                if path is not None:
                    path.appendleft(position)
                    return path
            if eliminated:
                eliminated.add(position)
            else:
                eliminations[index - 1] = {position}

        return None

    words = sorted(words, key=lambda x: (-len(x), x))

    for word in words:

        case_folded_word = word.casefold()
        end = len(case_folded_word) - 1
        first_letter = case_folded_word[0]
        eliminations: List[Optional[MutableSet[Tuple[int, int]]]] = [None] * (len(case_folded_word) - 1)

        for position in grid.occurrences(first_letter):
            path = find_path(1, position) if end > 0 else deque()
            if path is not None:
                path.appendleft(position)
                return word, tuple(path)

    return None


class Grid(object):
    """ Represents an 8 x 8 grid--presumably--containing letters drawn from one or more alphabets
    
    Grid entries are case folded when the grid is instantiated to ensure that case-insensitive comparisons can be made 
    with any (?) alphabet.
     
    """
    __slots__ = ('_grid',)  # saves space; good practice for objects with no dynamic membership requirements

    def __init__(self, grid: Sequence[str]):

        assert len(grid) == Grid.size
        self._grid = []

        for row in grid:
            row = re.sub(r'\s+', '', row).casefold()
            assert len(row) == Grid.size
            self._grid.append(row)

    def __getitem__(self, position: Tuple[int, int]) -> str:
        """ Get the letter in a cell on the current grid
        
        This method only partially implements `self[key]` semantics. Most notably slicing is not supported.
        
        :param position: row, column coordinates of a cell on the current grid
        :type position: Tuple[int, int]
        
        :return: The letter at 'position' on the current grid.   
         
        """
        return self._grid[position[0]][position[1]]

    def __str__(self):
        """ Get a human readable string representation of the current grid
         
        :return: A human readable string representation of the current grid
        :rtype: str
        
        """
        return '\n'.join(' '.join(column for column in row) for row in self._grid)

    @classmethod
    def generate(cls, words: Iterator[str]) -> 'Grid':
        """ Generate a grid containing a set of words that can be found using grid movement rules
        
        Use this method to create test grids. An error message is produced for each word that cannot be put on the grid.
        Randomly generated ASCII characters are used to put into unfilled cells.

        :param words: An iterator over the set of words to be put on to the grid.
        :type words: Iterator[str]
        
        :return: A grid object containing the words together with random ASCII fill characters.
        :rtype: Grid
        
        """
        missing_data = chr(0)
        data = [[missing_data] * Grid.size for i in range(0, Grid.size)]

        for word in words:
            origins = [(x, y) for x in range(0, Grid.size) for y in range(0, Grid.size)]
            random.shuffle(origins)
            word = word.casefold()
            success = False

            for row, column in origins:
                index = 0
                while index < len(word):
                    moves = [move for move in cls._moves]
                    random.shuffle(moves)
                    for x, y in moves:
                        x, y = row + x, column + y
                        if 0 <= x < Grid.size and 0 <= y < Grid.size:
                            if data[x][y] in (missing_data, word[index]):
                                data[x][y] = word[index]
                                row, column = x, y
                                success = True
                                index += 1
                                break
                    if not success:
                        break
                if success:
                    break

            if not success:
                print('could not find a place for', word)

        for row in data:
            for column in range(0, Grid.size):
                if row[column] == missing_data:
                    row[column] = random.choice(ascii_lowercase)  # Cop-out on unicode letters :(

        return Grid([' '.join(row) for row in data])

    @classmethod
    def load(cls, filename: str) -> 'Grid':
        """ Load a grid from a file
        
        :param filename: Name of a file containing a grid.
        :type filename: str
        
        :return: A Grid object
        :rtype: Grid
         
        """
        with io.open(filename) as f:
            lines = f.readlines()
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
        for row, letters in enumerate(self._grid, 0):
            column = -1
            while True:
                column = letters.find(letter, column + 1)
                if column < 0:
                    break
                yield row, column

    def save(self, filename: str) -> None:
        """ Save the current grid to a file 
        
        :param filename: Name of the file to which the current grid should be saved.
        :type filename: str
        
        :return: :const:`None`
        
        """
        with io.open(filename, 'w') as ostream:
            for row in self._grid:
                print(*(letter for letter in row), file=ostream, sep=' ')

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
