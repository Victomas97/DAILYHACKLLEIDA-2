#!/usr/bin/env python3

import unittest

from src.book import Book, create_book


class BookTest(unittest.TestCase):
    """
    Book test
    """

    def setUp(self):
        self.book = Book(1, 3, 0)
        self.book2 = Book(0, 3, 1)

    def test_book_creation(self):
        """
        Tests book creation
        """
        self.assertEqual(0, self.book._location)
        self.assertEqual(1, self.book.id_book)
        self.assertEqual(0, self.book._internal_time)
        self.assertEqual(1, self.book2._location)
        self.assertEqual(0, self.book2.id_book)
        self.assertEqual(0, self.book2._internal_time)

    def test_move(self):
        """
        Tests move action
        """

        self.assertEqual(0, self.book._location)
        self.book.move(1, 5)
        self.assertEqual(1, self.book._location)
        self.assertEqual(5, self.book._internal_time)
        self.book.move(0, 3)
        self.assertEqual(0, self.book._location)
        self.assertEqual(8, self.book._internal_time)

    def test_read(self):
        """
        Test read action
        """
        self.assertEqual(0, self.book._internal_time)
        self.book.read(3, 0)
        self.assertEqual(3, self.book._internal_time)
        self.book.read(5, 1)
        self.assertEqual(5, self.book._internal_time)
        try:
            self.book.read(1, 2)
            self.fail()
        except AssertionError:
            pass

    def test_move_then_read(self):
        """
        Tests move and then read
        """
        self.assertEqual(0, self.book._internal_time)
        self.book.move(1, 5)
        self.assertEqual(1, self.book._location)
        self.assertEqual(5, self.book._internal_time)
        self.book.read(8, 3)
        self.assertEqual(8, self.book._internal_time)


class CreateBookTest(unittest.TestCase):
    """
    Test create_book, which will we used to parse
    the book.
    """

    def setUp(self):
        self.line = "B 0 0 5"

    def test_create(self):
        """
        Test creates, which is a util to parse
        """
        book = create_book(self.line.split(" ")[1:])
        self.assertEqual(Book(0, 0, 5), book)
