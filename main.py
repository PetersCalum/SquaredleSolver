from __future__ import annotations

import math
import sys


class Letter:
    """
    Instance of a single letter on the board, along with all the valid neighbours (in each diagonal and orthogonal
    direction) it connects to.
    """

    def __init__(self, value: str):
        self.neighbours = []
        self.value = value

    def add_neighbour(self, neighbour: Letter) -> None:
        self.neighbours.append(neighbour)

    def get_neighbours(self) -> list:
        return self.neighbours

    def get_value(self) -> str:
        return self.value


def find_words(board_list: list, max_length: int, words_list: set) -> list:
    """
    Finds all the words present in the given board.
    :param board_list: List of Letters in the board
    :param max_length: maximum length of word to find
    :param words_list: List of potentially-valid words to find
    :return: a list of all words found in this board.
    """
    if max_length < 4:
        return []
    sub_words = [set()]
    for letters in range(1, max_length):
        parts = map(lambda word: word[:letters], words_list)
        right_length_parts = filter(lambda word: len(word) == letters, parts)
        unique = set(right_length_parts)
        sub_words.append(unique)
    found = []
    for start_letter in board_list:
        for neighbour in start_letter.get_neighbours():
            used = [start_letter, neighbour]
            start_word = start_letter.get_value() + neighbour.get_value()
            if start_word in sub_words[2]:
                found = found + find_words_from_chain(neighbour, start_word, max_length, words_list, sub_words, used)
    return list(set(found))


def find_words_from_chain(last_letter: Letter, sub_word: str, max_length: int, words_list: set, sub_words: list,
                          used: list) -> list:
    """
    Recursively explores the board from the last letter given and current chain of letters.
    :param last_letter: the last letter added to the chain
    :param sub_word: the currently constructed word chain.
    :param max_length: maximum length of word to find
    :param words_list: List of potentially-valid words to find
    :param sub_words: list of letter sets--every 2, 3, 4, 5, etc. letter string that is either a valid word or
    a prefix to a valid word.
    :param used: A list of the letter objects already used in the current chain (e.g. a board might have two e's)
    :return: a list of words found from the current chain"""
    found = []
    for neighbour in last_letter.get_neighbours():
        if neighbour in used:
            continue
        new_used = used + [neighbour]
        next_word = sub_word + neighbour.get_value()
        # all squaredle words are at least four letters in length
        if len(next_word) > 3 and next_word in words_list:
            found.append(next_word)
        if len(next_word) < max_length and next_word in sub_words[len(next_word)]:
            found = found + find_words_from_chain(neighbour, next_word, max_length, words_list, sub_words, new_used)
    return found


def load_words(file: str = 'words_alpha.txt') -> set:
    """
    opens and reads the words file
    :param file: filepath to a letter list
    :return: set of english words
    """
    with open(file) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


def get_board(board_string):
    size = math.sqrt(len(board_string))
    if size.is_integer():
        size = int(size)
        board = [[Letter(board_string[x * size + y]) for x in range(size)] for y in range(size)]
        possibilities = [(1, 0), (0, 1), (1, 1),
                         (-1, 0), (0, -1), (-1, -1),
                         (-1, 1), (1, -1)]
        for i in range(size):
            for j in range(size):
                for p in possibilities:
                    if 0 <= i + p[0] < size and 0 <= j + p[1] < size:
                        board[i][j].add_neighbour(board[i + p[0]][j + p[1]])
        return [let for x in board for let in x]
        # return flattened board
    else:
        quit()


if __name__ == '__main__':
    english_words = load_words() if len(sys.argv) < 4 else load_words(sys.argv[3])
    # pad with non-letter characters to make a square
    inputs = [".myj."
              "mabup" \
              "rclzs" \
              "geazt" \
              ".kba.", 10] if len(sys.argv) == 1 else [sys.argv[1], int(sys.argv[2])]
    board = get_board(inputs[0])
    words = find_words(board, (inputs[1]), english_words)
    words.sort()
    for word_length in range(4, inputs[1]+1):
        word_set = list(filter(lambda word: len(word) == word_length, words))
        print(f"Words of Length {word_length}:")
        print(len(word_set))
        for i in range(len(word_set) // 10 + 1):
            if (i + 1) * 10 < len(word_set):
                print(word_set[i * 10:(i + 1) * 10])
            else:
                print(word_set[i * 10:])
