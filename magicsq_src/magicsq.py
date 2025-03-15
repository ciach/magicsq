#!/usr/bin/env python3
"""
Creates magic squares (word squares) from words from an input file.

Usage:
    python3 magicsq.py INPUT_FILE OUTPUT_FILE
"""

import argparse
import itertools
import logging
import sys
import json
from collections import defaultdict
from pathlib import Path
from typing import List, Dict

from rich.progress import track


def read_file_to_list(file_name: str) -> List[str]:
    """Reads words from the given file, returning a list of stripped, lower-case words."""
    try:
        with open(Path(file_name), "r", encoding="utf-8") as file:
            words = [line.strip().lower() for line in file if line.strip()]
        return words
    except (FileNotFoundError, PermissionError, IOError) as e:
        logging.error("Error reading file %s: %s", file_name, e)
        sys.exit(1)


def build_prefix_dict(words: List[str]) -> Dict[str, List[str]]:
    """
    Builds a dictionary that maps every possible prefix (including the empty string)
    to a list of words that start with that prefix.
    """
    prefix_dict = defaultdict(list)
    # Assume all words have the same length.
    n = len(words[0])
    for word, i in itertools.product(words, range(n + 1)):
        prefix = word[:i]
        prefix_dict[prefix].append(word)
    return prefix_dict


def backtrack(
    square: List[str],
    n: int,
    prefix_dict: Dict[str, List[str]],
    results: List[List[str]],
):
    """
    Recursively builds a magic square (word square) by adding words row by row.
    Each new row is chosen based on the current column prefixes.
    """
    if len(square) == n:
        results.append(square.copy())
        return

    index = len(square)
    prefix = "".join(word[index] for word in square)
    for candidate in prefix_dict.get(prefix, []):
        square.append(candidate)
        backtrack(square, n, prefix_dict, results)
        square.pop()


def make_magic_squares(words_list: List[str], output_file: str) -> str:
    """
    Generates magic squares (word squares) using the given list of words and writes
    them to the specified output file in JSON format.

    Output example:
    {
        "1": {
            "0": "adept",
            "1": "dolar",
            "2": "elita",
            "3": "patos",
            "4": "trasa"
        },
        ...
    }
    """
    if not words_list:
        logging.error("No words found!")
        sys.exit(1)

    n = len(words_list[0])
    words = [word for word in words_list if len(word) == n]
    if not words:
        logging.error("No words of length %d found!", n)
        sys.exit(1)

    logging.info("Found %d words of length %d", len(words), n)

    prefix_dict = build_prefix_dict(words)
    results: List[List[str]] = []

    for word in track(words, description="Processing..."):
        backtrack([word], n, prefix_dict, results)

    # Convert the list of squares to the desired JSON format.
    # Each square is mapped using string keys that represent the row numbers.
    magic_squares = {}
    for idx, square in enumerate(results, start=1):
        magic_squares[str(idx)] = {str(i): word for i, word in enumerate(square)}

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(magic_squares, f, indent=4, ensure_ascii=False)
    except IOError as e:
        logging.error("Error writing to output file %s: %s", output_file, e)
        sys.exit(1)

    return f"Number of magic squares: {len(results)}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create magic squares (word squares) from an input file."
    )
    parser.add_argument("input_file", help="The input file with words")
    parser.add_argument("output_file", help="The output file to write magic squares")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()

    words_list = read_file_to_list(args.input_file)
    result = make_magic_squares(words_list, args.output_file)
    logging.info(result)


if __name__ == "__main__":
    main()
