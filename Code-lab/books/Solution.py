""" [Books](https://codelab.interviewbit.com/problems/books/)

References
----------
1. [Partition problem](https://en.wikipedia.org/wiki/Partition_problem)

"""
import pytest

from typing import List, Optional, Sequence, Tuple, Union


class Solution(object):

    class Assignment(object):

        __slots__ = ('books', 'page_count')

        def __init__(self, books: range, page_count: Union[int, Sequence[int]]):
            self.page_count = page_count if isinstance(page_count, int) else sum(page_count[i] for i in books)
            self.books = books

        def __str__(self):
            return f'books: {self.books}, page_count: {self.page_count}'

    @staticmethod
    def assign_books(page_counts: Sequence[int], student_count: int):

        if not (0 < student_count <= len(page_counts)):
            return -1

        if student_count == 1:
            return sum(page_counts)

        if student_count == len(page_counts):
            return max(page_counts)

        target_book_count = (len(page_counts) // student_count) + (1 if len(page_counts) % student_count else 0)
        target_page_count = sum(page_counts) // student_count  # equitable assignment is the best we can do

        assignments: List[Solution.Assignment] = [None] * student_count
        book_count = len(page_counts)
        maximum_page_count = 0
        overwhelmed = None
        book = 0

        for student in range(0, student_count):
            page_count = 0

            for index in range(book, book_count):
                if index >= book + target_book_count or page_count >= target_page_count:
                    index -= 1
                    break
                page_count += page_counts[index]

            if page_count > maximum_page_count:
                maximum_page_count = page_count
                overwhelmed = student

            assignments[student] = Solution.Assignment(range(book, index + 1), page_count)
            book = index + 1

        while True:
            result = Solution._redistribute(assignments, overwhelmed, page_counts)
            if result < 0:
                break
            overwhelmed = result

        return assignments[overwhelmed].page_count

    @staticmethod
    def _redistribute(assignments: List[Assignment], overwhelmed: int, page_counts: Sequence[int]):

        big_assignment = assignments[overwhelmed]

        if len(big_assignment.books) < 2:
            return -1  # someone's got to get this book; it's indivisible

        def get_winner(candidates: Sequence[Tuple[int, int]]) -> Optional[int]:

            if len(candidates) == 0:
                return None

            winner, minimum = candidates[0]

            for i in range(1, len(candidates)):
                student, page_count = candidates[i]
                if page_count < minimum:
                    winner, minimum = student, page_count

            return winner

        def reconfigure(winner: int, overwhelmed: int) -> int:

            if winner < overwhelmed:

                for student in range(overwhelmed, winner, -1):

                    assignment_1 = assignments[student]
                    start = assignment_1.books.start + 1
                    stop = assignment_1.books.stop
                    page_count = assignment_1.page_count - page_counts[start - 1]
                    assignments[student] = Solution.Assignment(range(start, stop), page_count)

                    assignment_2 = assignments[student - 1]
                    start = assignment_2.books.start
                    stop = assignment_2.books.stop + 1
                    page_count = assignment_2.page_count + page_counts[stop - 1]
                    assignments[student - 1] = Solution.Assignment(range(start, stop), page_count)

            else:

                for student in range(overwhelmed, winner, +1):

                    assignment_1 = assignments[student]
                    start = assignment_1.books.start
                    stop = assignment_1.books.stop - 1
                    page_count = assignment_1.page_count - page_counts[stop - 1]
                    assignments[student] = Solution.Assignment(range(start, stop), page_count)

                    assignment_2 = assignments[student - 1]
                    start = assignment_2.books.start
                    stop = assignment_2.books.stop + 1
                    page_count = assignment_2.page_count + page_counts[stop - 1]
                    assignments[student - 1] = Solution.Assignment(range(start, stop), page_count)

            big_assignment = assignments[0]
            overwhelmed = 0

            for student in range(1, len(assignments)):
                assignment = assignments[student]
                if assignment.page_count > big_assignment.page_count:
                    big_assignment = assignment
                    overwhelmed = student

            return overwhelmed

        def shift_left():
            candidates = []

            for student in range(overwhelmed, 0, -1):

                assignment_1 = assignments[student]
                assignment_2 = assignments[student - 1]

                start = assignment_1.books.start

                page_count_1 = assignment_1.page_count - page_counts[start]
                page_count_2 = assignment_2.page_count + page_counts[start]

                if page_count_1 < big_assignment.page_count and page_count_2 < big_assignment.page_count:
                    candidates.append((student - 1, max(page_count_1, page_count_2)))

            return candidates

        def shift_right():
            candidates = []

            for student in range(overwhelmed, len(assignments) - 1):
                assignment_1 = assignments[student]
                assignment_2 = assignments[student + 1]

                start = assignment_1.books.stop - 1

                page_count_1 = assignment_1.page_count - page_counts[start]
                page_count_2 = assignment_2.page_count + page_counts[start]

                if page_count_1 < big_assignment.page_count and page_count_2 < big_assignment.page_count:
                    candidates.append((student + 1, max(page_count_1, page_count_2)))

            return candidates

        rh_winner = get_winner(shift_right())
        lh_winner = get_winner(shift_left())

        if rh_winner is not None and lh_winner is not None:
            if lh_winner < rh_winner:
                rh_winner = None
            else:
                lh_winner = None

        if rh_winner is not None:
            return reconfigure(rh_winner, overwhelmed)

        if lh_winner is not None:
            return reconfigure(lh_winner, overwhelmed)

        return -1


@pytest.mark.parametrize(
    'page_count,student_count,expected', [
        ([23, 34, 21, 45, 3, 68, 43, 55], 3, 116),
        ([12, 34, 67, 90], 2, 113),
        ([12, 34, 67, 90], 3, 90),
    ]
)
def test_correctness(page_count: Sequence[int], student_count: int, expected: int) -> None:
    observed = Solution.assign_books(page_count, student_count)
    assert observed == expected
