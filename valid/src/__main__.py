#!/usr/bin/env python3
"""
Main module of the creator.
Example of how to use it on the command line:
$ python -m src inputfile outputfile

The output will be either an assert exception, providing
the line that it happened, or Score is {score}

Example of an error in the output file:
TODO

"""

import argparse
from functools import reduce
from .parse_input import parse_input


def main():
    """
    Main
    """
    parser = argparse.ArgumentParser(description="Validates and scores an output file")
    parser.add_argument(
        "inputfile", type=str, help="Input file that was processed to make the output"
    )
    parser.add_argument("output", type=str, help="Output file to be scored")
    args = parser.parse_args()
    state = parse_input(args.inputfile)
    with open(args.output) as fd:
        reduce(lambda acc, x: acc.process_line(x), enumerate(fd.readlines()), state)
    print(f"The Score is {state._score}")


if __name__ == "__main__":
    main()
