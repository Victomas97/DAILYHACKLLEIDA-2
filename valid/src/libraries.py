#!/usr/bin/env python3
from typing import List


class LibraryCreator:
    """
    Library utils to create the transition matrix
    """

    transition: List[List[int]]

    def __init__(self, libraries: int):
        self.transition = [[]] * libraries

    def parse_line(self, line: List[str]):
        """
        Parse Library with id id_ and line of transitions as
        transline
        :param id_: int : id of the library
        :param transline: List[int]: line of transitions
        adds transline
        """
        ls = [int(x) for x in line]
        self.transition[ls[0]] = ls[1:]
