#!/usr/bin/env python3
"""
Reader class declaration.
"""
from typing import List, Dict, Tuple

from .book import Book

Time = int


class Reader:
    """
    Reprensents the state of a reader at a state.
    """

    _books: Dict[int, Time]
    _location: int
    _timing: List[int]

    def __init__(self, books: Dict[int, Time], location: int, max_weeks: int):
        self._books = books
        self._location = location
        self._timing = [0] * max_weeks

    def read(self, book: Book, start_time: int, line_number: int) -> Tuple[int, int]:
        """
            Reads book.
        :param book: Book -> book to be read.
        :param start_time: int -> start_time. The reading will start as
          soon as it can.
        :return [score, end_time] -> returns score to update the state and
            end time to update the book.
        """
        assert book.id_book in self._books, f"Book not interested in line {line_number}"
        assert (
            book._location == self._location
        ), f"Book is not in {self._location}, instead is in {book._location}, in line {line_number}"
        bdata = self._books[book.id_book]
        max_time = len(self._timing)
        for j in range(start_time, max_time):
            if self._timing[j] < 3 and self.is_readable(bdata, j):
                del self._books[book.id_book]
                return self.__if_readable(bdata, book, j)
        del self._books[book.id_book]
        return 0, start_time  # test it

    def is_readable(self, bdata, time):
        """
        Is readable
        """
        max_time = len(self._timing)
        end_time = time + bdata
        for j in range(time, min(end_time, max_time)):
            if self._timing[j] >= 3:
                return False
        return True

    def __if_readable(self, bdata: Time, book: Book, time: Time) -> Tuple[int, int]:
        """
        If readable
        """
        max_time = len(self._timing)
        end_time = time + bdata
        score = 0 if end_time > max_time else book.score
        for j in range(time, min(end_time, max_time)):
            self._timing[j] += 1
        return score, end_time

    def __str__(self):
        return f"Book(books={self._books}, location={self._location}, _timing={self._timing})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Reader)
            and self._location == other._location
            and self._books == other._books
            and self._timing == other._timing
        )


def create_reader(line: List[str], max_weeks: int) -> Tuple[int, Reader]:
    """
    Creates a reader by the [line]. It does not
    discard the first letter, so line.split()[1:].
    :param: line.split()[1:]
    :return parsed Tuple[id, Reader].
    """
    id_ = int(line[0])
    loc_ = int(line[1])
    books = {int(k): int(v) for k, v in zip(line[2::2], line[3::2])}
    return id_, Reader(books, loc_, max_weeks)
