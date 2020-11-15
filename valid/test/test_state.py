#!/usr/bin/env python3
"""
Test State
"""

import unittest
from src.state import State
from src.book import Book
from src.reader import Reader


class StateTest(unittest.TestCase):
    """
    test state
    """

    def setUp(self):
        self.transition = [[0, 2, 3], [3, 0, 4], [3, 4, 0]]
        self.books = [
            Book(0, 1, 5),
            Book(1, 0, 3),
            Book(2, 1, 10),
            Book(3, 1, 2),
            Book(4, 2, 8),
        ]
        self.readers = [
            Reader({0: 3, 1: 2}, 0, 10),
            Reader({1: 1, 2: 10, 3: 3}, 0, 10),
            Reader({0: 1, 1: 1, 2: 1, 3: 1, 4: 1}, 1, 10),
            Reader({2: 5, 4: 5}, 2, 10),
        ]

        self.state = State(self.transition, self.books, self.readers)

    def process_move_book(self):
        """
        Process move successfully
        """
        line = (0, "3 m 0")
        line2 = (1, "2 m 4")
        state2 = self.state.process_line(line)
        self.assertEqual(0, state2._books._location)
        state2 = state2.process_line(line)
        # will return self so I can use reduce does not check.
        self.assertEqual(0, state2._books._location)

    def process_move_not_exist(self):
        """
        Process move unsuccessful
        """
        line = (2, "5 m 0")
        try:
            self.state.process_line(line)
            self.fail()
        except AssertionError:
            pass

    def process_read_book(self):
        line = (3, "1 r 1")
        st = self.state.process_line(line)
        self.assertEqual(3, st._score)

    def process_read_non_existent_reader(self):
        line = (4, "1 r 4")
        try:
            self.state.process_line(line)
            self.fail()
        except AssertionError:
            pass

    def process_read_non_existent_book(self):
        line = (5, "5 r 3")
        try:
            self.state.process_line(line)
            self.fail()
        except AssertionError:
            pass

    def process_read_not_score(self):
        self.readers[1]._timing = [3] * 10
        line = (6, "1 r 1")
        st = self.state.process_line(line)
        self.assertEqual(0, st.score)

    def process_read_not_same_location(self):
        line = (7, "0 r 1")
        try:
            self.state.process_line(line)
            self.fail()
        except AssertionError:
            pass
