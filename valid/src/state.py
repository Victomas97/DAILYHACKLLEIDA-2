#!/usr/bin/env python3
"""
State class declaration
"""
from typing import List, Tuple

from .book import Book
from .reader import Reader


class State:
    """
    State of the output line at the given line.
    """

    _transition: List[List[int]]
    _books: List[Book]
    _readers: List[Reader]
    _score: int

    def __init__(
        self,
        transition: List[List[int]],
        books: List[Book],
        readers: List[Reader],
    ):
        """
        Init does not parse file to avoid IO, so it is easy to test.
        """
        self._transition = transition
        self._books = books
        self._readers = readers
        self._score = 0

    def process_line(self, line: Tuple[int, str]) -> "State":
        """
        :param line : Tuple[int, str] where int is the number of the line,
        and str is the string to parse. It is provided the number of the line
        to show better errors in the messages.
        :return Either Exception State, where Exception
        is: line not correctly formated | state is not possible.
        """
        num_line, line_str = line
        linesplit = line_str.split()
        assert (
            len(linesplit) == 3
        ), f"Line has less or more arguments: num arguments-> {len(linesplit)} in line {num_line}"
        if linesplit[1] == "m":
            self._move_book(linesplit, num_line)
            return self
        if linesplit[1] == "r":
            self._read_book(linesplit, num_line)
            return self
        assert False, f"Not a valid action in line {num_line}"

    def _read_book(self, linesplit: List[str], num_line: int):
        book_id = int(linesplit[0])
        reader_id = int(linesplit[2])
        assert book_id < len(
            self._books
        ), f"Book id is not a valid identification in line: {num_line}"
        assert reader_id < len(
            self._readers
        ), f"Reader id is not a valid id in line {num_line}"
        book = self._books[book_id]
        score, end_time = self._readers[reader_id].read(
            book, book._internal_time, num_line
        )
        book.read(end_time, num_line)
        self._score += score

    def _move_book(self, linesplit: List[str], num_line: int):
        book_id = int(linesplit[0])
        new_loc = int(linesplit[2])
        assert book_id < len(
            self._books
        ), f"Book id is not a valid identification in line: {num_line}"
        assert new_loc < len(
            self._transition
        ), f"New location is not a valid id in line {num_line}"
        book = self._books[book_id]
        book.move(new_loc, self._transition[book.get_location()][new_loc])

    def __str__(self):
        return (
            f"State(transition={self._transition}, "
            + f"books={self._books}, readers=self._readers, "
            + f"score={self._score})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, State)
            and self._transition == other._transition
            and self._books == other._books
            and self._readers == other._readers
            and self._score == other._score
        )
