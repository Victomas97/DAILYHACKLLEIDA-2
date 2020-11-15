#!/usr/bin/env python3
"""
   Test LibraryCreator

"""

import unittest
from src.libraries import LibraryCreator


class LibraryTest(unittest.TestCase):
    """
    Serves to test a matrix creation
    """

    def setUp(self):
        self.lines = [
            "L 0 0 2 3",
            "L 1 3 0 4",
            "L 2 3 4 0",
        ]

    def test_matrix(self):
        """
        Tests matrix creation
        """
        matrix = [[0, 2, 3], [3, 0, 4], [3, 4, 0]]
        lc = LibraryCreator(3)
        for line in self.lines:
            lc.parse_line(line.split()[1:])
        self.assertEqual(matrix, lc.transition)
