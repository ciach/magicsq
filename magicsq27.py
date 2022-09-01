#!/usr/bin/env python
"""
Creates magic squares from words from input file

Desired usage:
    magicsq.py INPUT_FILE OUTPUT_FILE

"""

from pathlib import Path
from sys import exit as sys_exit
from fnmatch import filter as fn_filter

# from rich.traceback import install
# from rich.progress import track

# install()


def read_file_to_list(
    file_name,
):
    """_Opens file with given file name. Assumes file is in the same folder.
    File name is given as an parameter for script execution.
    Returns list with words as elements._

    Args:
        file_name (str): name of a file to open.

    Returns:
        words_list (list): containing words as elements
    """
    words_list = []
    try:
        with open(Path(file_name), "r", encoding="utf-8") as file:
            for line in file:
                words_list.append(line)
        file.close()
    except TypeError:
        print("TypeError: input file not defined!")
        sys_exit(1)
    return words_list


def write_line_to_file(file_name, line):
    """Writes line to file with a new line

    Args:
        file_name (str): File name to write to
        line (str): Content to write to file

    Returns
    -------
    Nothing
    """

    with open(file_name, "a", encoding="utf8") as file:
        file.write(line + "\n")
    file.close()


def make_magic_squares(words_list, output_file):
    """Returns list of lists with words starting

    Args:
        words_list (_type_): _description_
        word_number (_type_): _description_

    Returns:
        str: number of magic squares created

    """

    # first_word = [words_list[word_number].rstrip()]  # that's the list of length 1
    no_of_magic_sq = 0
    # for first_word in track(words_list, description="Processing..."):
    for first_word in words_list:
        if first_word:
            second_words = find_next_word(words_list, first_word[1] + "*")
            if second_words:
                for word_of_second_words in second_words:
                    third_words = find_next_word(
                        words_list, first_word[2] + word_of_second_words[2] + "*"
                    )
                    if third_words:
                        for word_of_third_words in third_words:
                            forth_words = find_next_word(
                                words_list,
                                first_word[3]
                                + word_of_second_words[3]
                                + word_of_third_words[3]
                                + "*",
                            )
                            if forth_words:
                                for word_of_forth_words in forth_words:
                                    fifth_words = find_next_word(
                                        words_list,
                                        first_word[4]
                                        + word_of_second_words[4]
                                        + word_of_third_words[4]
                                        + word_of_forth_words[4]
                                        + "*",
                                    )
                                    if fifth_words:
                                        for word_of_fifth_words in fifth_words:
                                            write_line_to_file(
                                                output_file, first_word.rstrip()
                                            )
                                            write_line_to_file(
                                                output_file, word_of_second_words
                                            )
                                            write_line_to_file(
                                                output_file, word_of_third_words
                                            )
                                            write_line_to_file(
                                                output_file, word_of_forth_words
                                            )
                                            write_line_to_file(
                                                output_file, word_of_fifth_words + "\n"
                                            )
                                            no_of_magic_sq += 1
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
            else:
                print("No second words found in file!")

        else:
            print("No words found in file!")
            sys_exit(1)
    return "Number of magic squares: " + str(no_of_magic_sq)


def find_next_word(words_list, part_string):
    """Finds string in words_list which is maching the pattern from part_string

    Args:
        words_list (list): list of words to check
        part_string (str): patter to match

    Returns:
        list: of words matching pattern
    """

    return_list = fn_filter(words_list, part_string)
    return [s.strip() for s in return_list]


if __name__ == "__main__":
    lista = read_file_to_list("5.txt")
    print(make_magic_squares(lista, "out2.txt"))
