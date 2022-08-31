"""_summary_

VELKI
ENAIM
LASTA
KITIM
IMAMO


"""

from dataclasses import asdict
from pathlib import Path
import sys
import itertools
import fnmatch


def read_file_to_list(
    file_name,
) -> list:
    """_Opens file with given file name. Assumes file is in the same folder.
    File name is given as an parameter for script execution.
    Returns list with words as elements._

    Args:
        file_name (str): name of a file to open.

    Returns:
        words_list (list): containing words as elements
    """
    words_list = []
    with open(Path(file_name), "r", encoding="utf-8") as file:
        for line in file:
            words_list.append(line)
    file.close()
    return words_list


def write_line_to_file(file_name, line):
    hs = open(file_name, "a")
    hs.write(line + "\n")
    hs.close()


def make_magic_squares(words_list, word_number, output_file) -> list:
    """Returns list of lists with words starting

    Args:
        words_list (_type_): _description_
        word_number (_type_): _description_

    Returns:
        list: _description_

    VELKI
    ENAIM
    LASTA
    KITIM
    IMAMO

    """

    first_word = [words_list[word_number].rstrip()]  # that's the list of length 1

    if first_word:
        second_words = find_next_word(words_list, f"{first_word[0][1]}*")
        if second_words:
            for word_of_second_words in second_words:
                third_words = find_next_word(
                    words_list, f"{first_word[0][2]}{word_of_second_words[2]}*"
                )
                if third_words:
                    for word_of_third_words in third_words:
                        forth_words = find_next_word(
                            words_list,
                            f"{first_word[0][3]}{word_of_second_words[3]}{word_of_third_words[3]}*",
                        )
                        if forth_words:
                            for word_of_forth_words in forth_words:
                                fifth_words = find_next_word(
                                    words_list,
                                    f"{first_word[0][4]}{word_of_second_words[4]}{word_of_third_words[4]}{word_of_forth_words[4]}*",
                                )
                                if fifth_words:
                                    for word_of_fifth_words in fifth_words:
                                        print(
                                            f"{first_word[0]}\n{word_of_second_words}\n{word_of_third_words}\n{word_of_forth_words}\n{word_of_fifth_words}\n"
                                        )
                                        write_line_to_file(output_file, first_word[0])
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
                                else:
                                    pass
                        else:
                            pass
                else:
                    pass
        else:
            print(f"No second words found in file {words_list}")
            sys.exit(1)

    else:
        print(f"No words found in file {words_list}")
        sys.exit(1)


def find_next_word(words_list, part_string):
    return_list = fnmatch.filter(words_list, part_string)
    return [s.strip() for s in return_list]


if __name__ == "__main__":
    lista = read_file_to_list("5.txt")
    words_lists = make_magic_squares(lista, 1527, "out.txt")
    print(words_lists)
#    for i in enumerate(lista):
#        words_lists = make_magic_squares(lista, i[0])
#        asd = words_mix(words_lists)
#        check_sq(asd)
