########################
# FILE : wordsearch.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex5 2019-2020
# DESCRIPTION: Search the words in the matrix according to the directions
########################
import sys
import os

VALID_DIRECTIONS = 'udrlwxyz'


def check_directions(directions):
    """
    Cheks if the directions are valid
    :param directions: String with the directions input
    :return: True if valid, else False
    """
    # Checks for an empty directions
    if directions == '':
        return False
    # Checks for valid directions according to  VALID_DIRECTIONS
    for i in directions:
        if i not in VALID_DIRECTIONS:
            return False
    return True


def check_file_existence(location):
    """
    Checks if the file exists in the given location
    :param location: The path of the file
    :return: True if the file exist, else False
    """
    return os.path.isfile(location)


def check_input_args(args):
    """
    Checks if the parameters that were given in the command line are valid
    :param args: List of the parameters given from the command line
    :return: If the input is valid returns None, else returns a message to
    the user according to mistake.
    """
    # Checks for invalid number of parameters
    if len(args) != 4:
        return "Invalid number of parameters given"
    # Checks for invalid directions string
    if not check_directions(args[3]):
        return "Invalid directions string"
    # Checks for the word file in the given location
    if not check_file_existence(args[0]):
        return "The word file is not in the given location"
    # Checks for the matrix file in the given location
    if not check_file_existence(args[1]):
        return "The matrix file is not in the given location"
    # Valid input
    return None


def read_wordlist_file(filename):
    """
    Opens the word list file and transfers its content to a string
    :param filename: The filename of the words list
    :return: List with the words
    """
    with open(filename, 'r') as words_file:
        words_list = words_file.read().split('\n')[:-1]
        return words_list


def read_matrix_file(filename):
    """
    Opens the matrix file and transforms its content to a list
    :param filename: The file of the matrix
    :return: two-dimensions list with the values of the matrix
    """
    with open(filename, 'r') as words_file:
        rows = words_file.read().split('\n')[:-1]
        matrix = [row.split(',') for row in rows]
        return matrix


def create_word_dict(word_list):
    """
    Creates a dict that the keys are the words in the list and values are 0
    :param word_list: The list of the words
    :return: Dictionary of the words
    """
    word_dict = {}
    for word in word_list:
        word_dict[word] = 0
    return word_dict


def search_down_col(word, col):
    """
    Searches the word in the given column downward
    :param word: The word that is being searched
    :param col: The column that is being checked
    :return: The word appears number
    """
    appears_counter = 0
    current_row = 0
    # Running until the word is longer then the rows reminded
    while current_row <= len(col) - len(word):
        correct_letters_counter = 0
        # Checking every letter of the word
        for index in range(current_row, current_row + len(word)):
            # Correct word
            if col[index] == word[correct_letters_counter]:
                correct_letters_counter += 1
            # Incorrect word
            else:
                break
        # Found 1 appearance of the word
        if correct_letters_counter == len(word):
            appears_counter += 1
            current_row += 1
        else:
            current_row += 1
    return appears_counter


def search_down_matrix(matrix, word):
    """
    Searches the word in the given matrix downward
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    appears_counter = 0
    # Using the search_down_col to search the word in every column
    for col in range(len(matrix[0])):
        current_col = [matrix[row][col] for row in range(len(matrix))]
        # Adds the appears in the column
        appears_counter += search_down_col(word, current_col)
    return appears_counter


def search_up_col(word, col):
    """
    Searches the word in the given column to the upward
    :param word: The word that is being searched
    :param col: The column that is being checked
    :return: The word appears number
    """
    appears_counter = 0
    current_row = len(col) - 1
    # Running until the word is longer then the rows reminded
    while current_row >= len(word) - 1 >= 0:
        correct_letters_counter = 0
        # Checking every letter of the word
        for index in range(current_row, current_row - len(word), -1):
            # Correct letter
            if col[index] == word[correct_letters_counter]:
                correct_letters_counter += 1
            # Incorrect word
            else:
                break
        # Found 1 appearance of the word
        if correct_letters_counter == len(word):
            appears_counter += 1
            current_row -= 1
        else:
            current_row -= 1
    return appears_counter


def search_up_matrix(matrix, word):
    """
    Searches the word in the given matrix upward
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    appears_counter = 0
    # Using the search_up_col to search the word in every column
    for col in range(len(matrix[0])):
        current_col = [matrix[row][col] for row in range(len(matrix))]
        # Adds the appears in the column
        appears_counter += search_up_col(word, current_col)
    return appears_counter


def search_right_row(word, row):
    """
    Searches the word in the given row to the right
    :param row: The row that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    appears_counter = 0
    current_col = 0
    # Running until the word is longer then the columns reminded
    while current_col <= len(row) - len(word):
        correct_letters_counter = 0
        # Checking every letter of the word
        for index in range(current_col, current_col + len(word)):
            # Correct letter
            if row[index] == word[correct_letters_counter]:
                correct_letters_counter += 1
            # Incorrect word
            else:
                break
        # Found 1 appearance of the word
        if correct_letters_counter == len(word):
            appears_counter += 1
            current_col += 1
        else:
            current_col += 1
    return appears_counter


def search_right_matrix(matrix, word):
    """
    Searches the word in the given matrix to the right
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    if word == '':
        return 0
    appears_counter = 0
    # Using the search_right_row to search the word in every row
    for row in range(len(matrix)):
        current_row = [matrix[row][col] for col in range(len(matrix[0]))]
        # Adds the appears in the row
        appears_counter += search_right_row(word, current_row)
    return appears_counter


def search_left_row(word, row):
    """
    Searches the word in the given row to the left
    :param row: The row that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    appears_counter = 0
    current_col = len(row) - 1
    # Running until the word is longer then the columns reminded
    while current_col >= len(word) - 1 >= 0:
        correct_letters_counter = 0
        # Checking every letter of the word
        for index in range(current_col, current_col - len(word), -1):
            # Checking every letter of the word
            if row[index] == word[correct_letters_counter]:
                correct_letters_counter += 1
            # Incorrect word
            else:
                break
        # Found 1 appearance of the word
        if correct_letters_counter == len(word):
            appears_counter += 1
            current_col -= 1
        else:
            current_col -= 1
    return appears_counter


def search_left_matrix(matrix, word):
    """
    Searches the word in the given matrix to the left
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    if word == '':
        return 0
    appears_counter = 0
    # Using the search_right_row to search the word in every column
    for row in range(len(matrix)):
        current_row = [matrix[row][col] for col in range(len(matrix[0]))]
        # Adds the appears in the row
        appears_counter += search_left_row(word, current_row)
    return appears_counter


def search_right_up_diagonal(word, matrix, row, col):
    """
    Searches the word in the matrix according to the row and col given in the
    right up diagonal
    :param word: The word that is being searched
    :param matrix: The matrix that is being checked
    :param row: The row that is being checked
    :param col: The column that is being checked
    :return: True if the word is in the diagonal that starts from the row and
    col, else False
    """
    current_row = row
    current_col = col
    for letter in word:
        if letter == matrix[current_row][current_col]:
            current_row -= 1
            current_col += 1
        else:
            return False
    return True


def search_right_up_diagonal_matrix(matrix, word):
    """
    Searches the word in the whole matrix in the right up diagonal
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    appears_counter = 0
    checked_row = len(matrix) - 1
    while checked_row >= len(word) - 1 >= 0:
        current_col = 0
        current_row = checked_row
        while current_col <= len(matrix[0]) - len(word):
            if search_right_up_diagonal(word, matrix, current_row,
                                        current_col):
                appears_counter += 1
                current_col += 1
            else:
                current_col += 1
        checked_row -= 1
    return appears_counter


def search_left_up_diagonal(word, matrix, row, col):
    """
    Searches the word in the matrix according to the row and col given in the
    left up diagonal
    :param word: The word that is being searched
    :param matrix: The matrix that is being checked
    :param row: The row that is being checked
    :param col: The column that is being checked
    :return: True if the word is in the diagonal that starts from the row and
    col, else False
    """
    current_row = row
    current_col = col
    for letter in word:
        if letter == matrix[current_row][current_col]:
            current_row -= 1
            current_col -= 1
        else:
            return False
    return True


def search_left_up_diagonal_matrix(matrix, word):
    """
    Searches the word in the whole matrix in the left up diagonal
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    appears_counter = 0
    checked_row = len(matrix) - 1
    while checked_row >= len(word) - 1 >= 0:
        current_col = len(matrix[0]) - 1
        current_row = checked_row
        while current_col >= len(word) - 1:
            if search_left_up_diagonal(word, matrix, current_row, current_col):
                appears_counter += 1
                current_col -= 1
            else:
                current_col -= 1
        checked_row -= 1
    return appears_counter


def search_right_down_diagonal(word, matrix, row, col):
    """
    Searches the word in the matrix according to the row and col given in the
    right down diagonal
    :param word: The word that is being searched
    :param matrix: The matrix that is being checked
    :param row: The row that is being checked
    :param col: The column that is being checked
    :return: True if the word is in the diagonal that starts from the row and
    col, else False
    """
    current_row = row
    current_col = col
    for letter in word:
        if letter == matrix[current_row][current_col]:
            current_row += 1
            current_col += 1
        else:
            return False
    return True


def search_right_down_diagonal_matrix(matrix, word):
    """
    Searches the word in the whole matrix in the right down diagonal
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    if word == '':
        return 0
    appears_counter = 0
    checked_row = 0
    while checked_row <= len(matrix) - len(word):
        current_col = 0
        current_row = checked_row
        while current_col <= len(matrix[0]) - len(word):
            if search_right_down_diagonal(word, matrix, current_row,
                                          current_col):
                appears_counter += 1
                current_col += 1
            else:
                current_col += 1
        checked_row += 1
    return appears_counter


def search_left_down_diagonal(word, matrix, row, col):
    """
    Searches the word in the matrix according to the row and col given in the
    left down diagonal
    :param word: The word that is being searched
    :param matrix: The matrix that is being checked
    :param row: The row that is being checked
    :param col: The column that is being checked
    :return: True if the word is in the diagonal that starts from the row and
    col, else False
    """
    current_row = row
    current_col = col
    for letter in word:
        if letter == matrix[current_row][current_col]:
            current_row += 1
            current_col -= 1
        else:
            return False
    return True


def search_left_down_diagonal_matrix(matrix, word):
    """
    Searches the word in the whole matrix in the left down diagonal
    :param matrix: The matrix that is being checked
    :param word: The word that is being searched
    :return: The word appears number
    """
    if word == '':
        return 0
    appears_counter = 0
    checked_row = 0
    while checked_row <= len(matrix) - len(word):
        current_col = len(matrix[0]) - 1
        current_row = checked_row
        while current_col >= len(word) - 1:
            if search_left_down_diagonal(word, matrix, current_row,
                                         current_col):
                appears_counter += 1
                current_col -= 1
            else:
                current_col -= 1
        checked_row += 1
    return appears_counter


def tuples_from_dict(appears_dict):
    """
    Transforms the dict to a list of tuples
    :param appears_dict: The dictionary with results of the search
    :return: List of tuples, that every tuple contains the word and the
    number of appears
    """
    list_of_tuples = [(key, appears_dict[key]) for key in appears_dict.keys()
                      if appears_dict[key] != 0]
    return list_of_tuples


def find_words_in_matrix(word_list, matrix, directions):
    """
    Uses all of the search functions to find all the appears of every word in
    the matrix according to the directions given.
    :param word_list: The list of words that the user wants to search
    :param matrix: The matrix that is being checked
    :param directions: The directions that the user wants to check
    :return: List of tuples with the words and their appears
    """
    appears_dict = create_word_dict(word_list)
    # Checks for an empty word list or matrix
    if word_list == [] or matrix == []:
        return []
    for word in word_list:
        appears_counter = 0
        for direction in set(directions):
            if direction == 'u':
                appears_counter += search_up_matrix(matrix, word)
            if direction == 'd':
                appears_counter += search_down_matrix(matrix, word)
            if direction == 'r':
                appears_counter += search_right_matrix(matrix, word)
            if direction == 'l':
                appears_counter += search_left_matrix(matrix, word)
            if direction == 'w':
                appears_counter += search_right_up_diagonal_matrix(matrix,
                                                                   word)
            if direction == 'x':
                appears_counter += search_left_up_diagonal_matrix(matrix, word)
            if direction == 'y':
                appears_counter += search_right_down_diagonal_matrix(matrix,
                                                                     word)
            if direction == 'z':
                appears_counter += search_left_down_diagonal_matrix(matrix,
                                                                    word)
        # Adds the appears to the dict
        appears_dict[word] = appears_counter
    return tuples_from_dict(appears_dict)


def write_output_file(results, output_filename):
    """
    Writes the results list to the given file
    :param results: A list of tuple with the search results of the words in the
     matrix
    :param output_filename: The name/path of the output file
    """
    with open(output_filename, 'w') as output:
        if results:
            input_list = [result[0] + ',' + str(result[1]) for result in
                          results]
            input_str = '\n'.join(input_list) + '\n'
            output.write(input_str)
        else:
            output.write('')


def main():
    """
    The main function that gets the input from the command line, runs the
    search function and writes the results to the output file
    :return: If the input in the command line is invalid returns an error
    message
    """
    # Gets the input from the command line
    input_list = sys.argv[1:]
    # Valid input
    if check_input_args(input_list) is None:
        wordlist_file = read_wordlist_file(input_list[0])
        matrix = read_matrix_file(input_list[1])
        directions = input_list[3]
        outputfile = input_list[2]
        output_dict = find_words_in_matrix(wordlist_file, matrix, directions)
        write_output_file(output_dict, outputfile)
    # Invalid input
    else:
        return check_input_args(input_list)


if __name__ == "__main__":
    main()
