import math


def make_chains_from_square(board_input: list, chain_length: int, board_input_size: int, current_square: (int, int),
                            current_chain: str, used_squares: list) -> list:
    """
    recursively called to build up all chains starting from a particular square
    :param board_input: board to make word chains from
    :param chain_length: maximum length of word to find
    :param board_input_size: size of the board on one size
    :param current_square: square that's currently selected
    :param current_chain: 'word' that has been found so far
    :param used_squares: squares already visited in making this chain
    :return: a list containing a word (if the maximum length has been met) or all words found starting from this square
    """
    if len(current_chain) == chain_length:
        return [current_chain]
    else:
        chains = []
        # hardcode permutations to save time--all coordinates adjacent to the current square (including diagonally)
        possibilities = [(1, 0), (0, 1), (1, 1),
                         (-1, 0), (0, -1), (-1, -1),
                         (-1, 1), (1, -1)]
        for possibility in possibilities:
            next_square = tuple(map(lambda i, j: i + j, current_square, possibility))
            if next_square not in used_squares and next_square[0] >= 0 and next_square[1] >= 0 \
                    and next_square[0] < board_input_size and next_square[1] < board_input_size:
                next_chain = current_chain + board_input[next_square[0]][next_square[1]]
                next_used_squares = used_squares[:]
                next_used_squares.append(current_square)
                chains = chains + (make_chains_from_square(board_input, chain_length, board_input_size, next_square,
                                                           next_chain, next_used_squares))
        return chains


def make_chains(board_input: list, chain_length: int, board_input_size: int) -> list:
    """
    :param board_input: board to  make word chains out of
    :param chain_length: maximum length of word to find
    :param board_input_size: size of the board on one size
    :return: a list of all possible letter combinations that length on the board
    """

    possible_words = []
    for i in range(board_input_size):
        for j in range(board_input_size):
            # start at top left and work along.
            current_chain = board_input[i][j]
            starting_square = (i, j)
            possible_words += (make_chains_from_square(board_input, chain_length, board_input_size, starting_square,
                                                       board_input[i][j], [(i, j)]))

    return possible_words
    # Use a breakpoint in the code line below to debug your script.


def load_words() -> set:
    """
    opens and reads the words file
    :return: set of english words
    """
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


def filter_words(words_list: list, valid_words: set) -> set:
    """
    takes a list of 'words' and filters it to contain only valid english words
    :param words_list: list of words we want filtered
    :param valid_words: set of valid english words
    :return: a filtered set containing only english words
    """
    filtered_list = []
    for word in words_list:
        if word in valid_words:
            filtered_list += [word]
    return set(filtered_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # input letters left-right, top-bottom
    english_words = load_words()
    letter_input = "everrzomodolfiuy"
    board_size = int(math.sqrt(len(letter_input)))
    board = [['a' for i in range(board_size)] for j in range(board_size)]
    for i in range(board_size):
        for j in range(board_size):
            board[i][j] = letter_input[i * board_size + j]
    for word_length in range(4, 9):
        word_set = list(filter_words(make_chains(board, word_length, board_size), english_words))
        word_set.sort()
        print(f"Words of Length {word_length}:")
        print(len(word_set))
        for i in range(len(word_set)//10+1):
            if (i+1)*10 < len(word_set):
                print(word_set[i*10:(i+1)*10])
            else:
                print(word_set[i*10:])
