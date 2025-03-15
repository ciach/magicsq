#!/usr/bin/env python3
"""
Creates magic squares (word squares) from words from an input file.

Usage:
    python3 magicsq.py INPUT_FILE OUTPUT_FILE
"""


import itertools
from pathlib import Path
import sys
from rich.progress import track


def read_file_to_list(file_name: str) -> list:
    """Reads words from the given file, returning a list of stripped, lower-case words."""
    try:
        with open(Path(file_name), "r", encoding="utf-8") as file:
            words = [line.strip().lower() for line in file if line.strip()]
        return words
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(f"Error reading file {file_name}: {e}")
        sys.exit(1)


def build_prefix_dict(words: list) -> dict:
    """
    Builds a dictionary that maps every possible prefix (including the empty string)
    to a list of words that start with that prefix.
    """
    prefix_dict = {}
    # Assume all words have the same length
    n = len(words[0])
    for word, i in itertools.product(words, range(n + 1)):
        prefix = word[:i]
        prefix_dict.setdefault(prefix, []).append(word)
    return prefix_dict


def backtrack(square: list, n: int, prefix_dict: dict, results: list):
    """
    Recursively builds a magic square (word square) by adding words row by row.
    Each new row is chosen based on the current column prefixes.
    """
    if len(square) == n:
        # Completed square, add a copy of it to results.
        results.append(square.copy())
        return

    # Build the prefix for the next row: for column i, take the i-th character
    index = len(square)
    prefix = "".join(word[index] for word in square)
    # Retrieve all candidate words that have the current prefix.
    for candidate in prefix_dict.get(prefix, []):
        square.append(candidate)
        backtrack(square, n, prefix_dict, results)
        square.pop()


def make_magic_squares(words_list: list, output_file: str) -> str:
    """
    Generates magic squares (word squares) using the given list of words and writes
    them to the specified output file.
    """
    if not words_list:
        print("No words found!")
        sys.exit(1)

    # Assume we are building squares of the length of the first word.
    n = len(words_list[0])
    # Filter to ensure all words are of the same length.
    words = [word for word in words_list if len(word) == n]
    if not words:
        print(f"No words of length {n} found!")
        sys.exit(1)

    print(f"Found {len(words)} words of length {n}")

    # Precompute the prefix dictionary.
    prefix_dict = build_prefix_dict(words)
    results = []

    # Use each word as the starting row.
    for word in track(words, description="Processing..."):
        backtrack([word], n, prefix_dict, results)

    # Write results to the output file in a batch.
    with open(output_file, "w", encoding="utf-8") as f:
        for square in results:
            f.write("\n".join(square) + "\n\n")

    return f"Number of magic squares: {len(results)}"


if __name__ == "__main__":
    # Example usage: python3 magicsq.py 5.txt out2.txt
    if len(sys.argv) != 3:
        print("Usage: python3 magicsq.py INPUT_FILE OUTPUT_FILE")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    words_list = read_file_to_list(input_file)
    result = make_magic_squares(words_list, output_file)
    print(result)
