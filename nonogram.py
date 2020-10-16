########################
# FILE : ex8.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex8 2019-2020
# DESCRIPTION: Functions that solve nonograms
########################
import ex8_helper as helper

def get_row_variations(row, blocks):
    """
    return the possible variations of the row according to the blocks
    :param row: the given row
    :param blocks: the constrains
    :return: List with all of the possible variations
    """
    result = []
    if not blocks:
        result.append([0 for i in row])
    else:
        _get_row_helper(row, blocks, result, 0, len(row), len(blocks))
    return result


def _get_row_helper(row, blocks, result, row_index, row_length, blocks_length):
    """
    recursive function that finds the optional rows according to the given
    constrains
    :param row: the current row
    :param blocks: the constrains
    :param result: list with the results of the combinations
    :param row_index
    :param row_length
    :param blocks_length
    :return: list with all of the possible rows according to the constrains
    """
    if row_index == row_length:
        if get_constraints(row) == blocks:
            result.append(row[:])
        return
    const = get_constraints(row[:row_index])
    if const:
        const_len = len(const)
        if const_len > blocks_length or row_length - row.count(0) < sum(
                blocks) or \
                sum(const) > sum(blocks) or const[-1] > blocks[const_len - 1]:
            return
    if row[row_index] == 0 or row[row_index] == 1:
        _get_row_helper(row, blocks, result, row_index + 1, row_length,
                        blocks_length)
    else:
        for i in [0, 1]:
            row[row_index] = i
            _get_row_helper(row, blocks, result, row_index + 1, row_length,
                            blocks_length)
        row[row_index] = -1


def get_constraints(row):
    """
    creates a list with the constrains of the row
    :param row: the given row
    :return: list with the constrains of the row
    """
    new_lst = [0]
    for i in row:
        if i == 1:
            new_lst[-1] += 1
        else:
            new_lst.append(0)
    const = []
    for value in new_lst:
        if value != 0:
            const.append(value)
    return const


def get_intersection_row(rows):
    """
    checks the rows for a place that is for sure 0 or 1
    :param rows: all of the possible rows
    :return: row with the intersections
    """
    if not rows:
        return []
    final_list = []
    index = 0
    while index < len(rows[0]):
        counter_0 = 0
        counter_1 = 0
        for i in rows:
            if i[index] == 0:
                counter_0 += 1
            if i[index] == 1:
                counter_1 += 1
        if counter_0 == len(rows):
            final_list.append(0)
        elif counter_1 == len(rows):
            final_list.append(1)
        else:
            final_list.append(-1)
        index += 1
    return final_list


def conclude_from_rows_constraints(board, constraints):
    """
    changes the board according the constrains of the rows
    :param board: the current board
    :param constraints: the constrains
    """
    rows_index = 0
    while rows_index < len(board):
        variations_list = get_row_variations(board[rows_index],
                                             constraints[rows_index])
        board[rows_index] = get_intersection_row(variations_list)
        rows_index += 1


def conclude_from_cols_constraints(board, constraints):
    """
    changes the board according the constrains of the cols
    :param board: the current board
    :param constraints: the constrains
    """
    switched_board = switch_cols_rows(board)
    intersections = []
    for i in range(len(switched_board)):
        variations = get_row_variations(switched_board[i], constraints[i])
        intersections.append(get_intersection_row(variations))
    col_index = 0
    while col_index < len(constraints):
        row_index = 0
        while row_index < len(board):
            board[row_index][col_index] = intersections[col_index][row_index]
            row_index += 1
        col_index += 1


def _conclude_helper(board, constraints):
    """
    changes the board according the constrains of the rows and cols
    :param board: the current board
    :param constraints: the constrains
    """
    # First run
    n = 0
    while True:
        # Conclude from rows
        if n % 2 == 0:
            current_minus = count_minus_1(board)
            conclude_from_rows_constraints(board, constraints[0])
            new_minus_counter = count_minus_1(board)
            if (current_minus == new_minus_counter or new_minus_counter == 0) \
                    and n != 0:
                break
            else:
                n += 1
        # Conclude from cols
        if n % 2 == 1:
            current_minus = count_minus_1(board)
            conclude_from_cols_constraints(board, constraints[1])
            new_minus_counter = count_minus_1(board)
            if current_minus == new_minus_counter or new_minus_counter == 0:
                break
            else:
                n += 1


def switch_cols_rows(board):
    """
    switch between the rows and the cols
    :param board: the current board
    :return: the board with cols as rows
    """
    cols_as_rows = []
    cols_index = 0
    while cols_index < len(board[0]):
        rows_index = 0
        col_as_row = []
        while rows_index < len(board):
            col_as_row.append(board[rows_index][cols_index])
            rows_index += 1
        cols_as_rows.append(col_as_row)
        cols_index += 1
    return cols_as_rows


def conclude_from_constraints(board, constraints):
    """
    conclude from the constrains
    :param board: the current board
    :param constraints: the constrains
    :return: None
    """
    if not board:
        return None
    _conclude_helper(board, constraints)
    return None


def count_minus_1(board):
    """
    counts the appearances of -1
    :param board: the current board
    :return: the number of -1
    """
    sum = 0
    for i in board:
        sum += i.count(-1)
    return sum


def solve_easy_nonogram(constraints):
    """
    solves easy nonograms
    :param constraints: the constrains
    :return: the solved board
    """
    board = [[-1 for i in range(len(constraints[1]))] for j in
             range(len(constraints[0]))]
    conclude_from_constraints(board, constraints)
    return board


constraints = [[
    [1, 1, 1, 1, 2, 1, 1, 1, 1],
    [2],
    [1, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 1, 1, 6, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 1],
    [1, 1, 10, 1, 1],
    [1, 1, 2, 1, 1],
    [1, 14, 1],
    [1, 2, 1],
    [18],
    [2],
    [1, 2],
    [5, 2, 1],
    [3, 4, 5],
    [1, 6, 3],
    [8, 1],
],
    [
        [1, 8, 1],
        [1, 2],
        [1, 6, 1, 4],
        [1, 1, 2],
        [1, 4, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 2, 1, 1, 1, 2],
        [1, 1, 1, 1, 3],
        [16],
        [16],
        [1, 1, 1, 1, 3],
        [1, 2, 1, 1, 1, 2],
        [1, 1, 1, 1],
        [1, 4, 1, 1, 1],
        [1, 1, 2],
        [1, 6, 1, 4],
        [1, 2],
        [1, 8, 1],
    ]]

helper.print_board(solve_easy_nonogram(constraints))