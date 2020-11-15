#!/usr/bin/env python3
"""
Parser input file.
"""

from typing import List, Tuple, Optional

from .book import Book, create_book
from .reader import Reader, create_reader
from .state import State
from .libraries import LibraryCreator


class InputParser:
    """
    Input parser. Builder of State
    """

    lc: Optional[LibraryCreator]
    books: List[Book]
    readers: List[Tuple[int, Reader]]
    max_weeks: int

    def __init__(self):
        self.lc = None
        self.books = []
        self.readers = []
        self.max_weeks = -1
        self.parser = {
            "R": self.__util_reader,
            "B": self.__util_book,
            "L": self.__util_library,
            "T": self.__util_time,
        }

    def __util_reader(self, line: List[str]) -> None:
        self.readers.append(create_reader(line, self.max_weeks))

    def __util_book(self, line: List[str]) -> None:
        self.books.append(create_book(line))

    def __util_library(self, line: List[str]) -> None:
        if self.lc is None:
            self.lc = LibraryCreator(len(line) - 1)
        self.lc.parse_line(line)

    def __util_time(self, line: List[str]) -> None:
        self.max_weeks = int(line[0])

    def parse_line(self, line: str) -> None:
        """
        Parses a line of the input file
        """
        ls = line.split()
        self.parser[ls[0]](ls[1:])

    def get_state(self) -> State:
        """
        Gets initial state
        """
        bks: List[Book] = [Book(-1, -1, -1)] * len(self.books)
        for book in self.books:
            bks[book.id_book] = book

        rds: List[Reader] = [Reader({}, -1, -1)] * len(self.readers)
        for id_, reader in self.readers:
            rds[id_] = reader

        return State(self.lc.transition, bks, rds)


def parse_input(input_file: str) -> State:
    """
    Parses input file as a State. If it seems weird is because
    it is. I should extract an object from this.
    """
    parser = InputParser()
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            parser.parse_line(line)

    return parser.get_state()
