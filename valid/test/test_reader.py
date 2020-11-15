#!/usr/bin/env python3

import unittest

from src.reader import Reader, create_reader
from src.book import Book


class ReaderTest(unittest.TestCase):
    """
    Reader Test
    """

    def setUp(self):
        self.book_data = {0: 5, 1: 2, 3: 3}
        self.reader = Reader(books=self.book_data, location=1, max_weeks=6)
        self.books = [Book(0, 3, 1), Book(1, 5, 0), Book(2, 4, 1), Book(3, 2, 1)]

    def test_creation(self):
        """
        Tests the creation of a reader.
        """
        self.assertEqual(self.book_data, self.reader._books)
        self.assertEqual(1, self.reader._location)
        self.assertEqual([0, 0, 0, 0, 0, 0], self.reader._timing)

    def test_read(self):
        """
        Test simple read book 0.
        """
        self.reader._timing = [3, 2, 2, 1, 1, 1]
        score, time = self.reader.read(self.books[0], 0, 3)
        self.assertTrue(self.books[0].id_book not in self.reader._books)
        self.assertEqual(3, score)
        self.assertEqual(6, time)
        self.assertEqual([3, 3, 3, 2, 2, 2], self.reader._timing)
        score, time = self.reader.read(self.books[3], 4, 5)
        self.assertTrue(self.books[3].id_book not in self.reader._books)
        self.assertEqual(0, score)
        self.assertEqual(7, time)
        self.assertEqual([3, 3, 3, 2, 3, 3], self.reader._timing)

    def test_another_read(self):
        """
        Test complex read book 0.
        """
        self.reader._timing = [3, 2, 3, 3, 1, 1]
        score, time = self.reader.read(self.books[0], 0, 6)
        self.assertTrue(self.books[0].id_book not in self.reader._books)
        self.assertEqual(0, score)
        self.assertEqual(9, time)

    def test_read_not_interested(self):
        """
        Test if Reader is not interested in books
        """
        try:
            self.reader.read(self.books[2], 0, 0)
            self.fail("Readed book not interested")
        except AssertionError:
            pass

    def test_read_different_location(self):
        """
        Test if Book is in different location.
        """
        try:
            self.reader.read(self.books[1], 0, 1)
            self.fail("Readed book was not in the library")
        except AssertionError:
            pass


class ReaderCreatorTest(unittest.TestCase):
    """
    Tests creator reader.
    """

    def setUp(self):
        self.line = "R 2 1 0 1 1 1 2 1 3 1 4 1"

    def test_reader_creator(self):
        """
        Create reader test
        """
        res = create_reader(self.line.split()[1:], 12)
        expected = (2, Reader({0: 1, 1: 1, 2: 1, 3: 1, 4: 1}, 1, 12))
        self.assertEqual(expected, res)
