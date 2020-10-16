########################
# FILE : ex7.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex7 2019-2020
# DESCRIPTION: Recursive functions
########################


def print_to_n(n):
    """
    Prints the numbers from 1 to n
    :param n: the given number
    """
    if n < 1:
        return
    if n == 1:
        print(n)
    else:
        print_to_n(n - 1)
        print(n)


def digit_sum(n):
    """
    Prints the sum of the digits in the number
    :param n: the given number
    """
    if len(str(n)) == 1:
        print(n)
        return n
    return n % 10 + digit_sum(n // 10)


def is_prime(n):
    """
    Checks if the given number is prime
    :param n: the given number
    :return: True if prime, else False
    """
    if n <= 1:
        return False
    if has_divisor_smaller_than(n, int(n**0.5) + 1):
        return False
    else:
        return True


def has_divisor_smaller_than(n, i):
    """
    Checks if the given number has a divisor
    :param n: the checked number
    :param i: the divisor
    :return: True if the number has a divisor else False
    """
    if i == 1:
        return False
    if n % (i - 1) == 0 and i - 1 != 1:
        return True
    return has_divisor_smaller_than(n, i - 1)


def play_hanoi(hanoi, n, src, dst, temp):
    """
    Solves the hanoi tower puzzle
    :param hanoi: the game board
    :param n: number of disks
    :param src: source tower
    :param dst: destination tower
    :param temp: temp tower
    """
    if n <= 0:
        return
    if n == 1:
        hanoi.move(src, dst)
    else:
        play_hanoi(hanoi, n - 1, src, temp, dst)
        hanoi.move(src, dst)
        play_hanoi(hanoi, n - 1, temp, dst, src)


def print_sequences(char_list, n):
    """
    Prints all of the sequences with length n
    :param char_list: the char list
    :param n: the length of the sequence
    """
    if n < 1:
        return
    elif n == 1:
        print_list(char_list)
    else:
        lst = []
        for char in char_list:
            lst.extend(char_sequences(char, char_list, n))
        print_list(lst)


def print_list(lst):
    """
    Prints the list
    :param lst: the given list
    """
    for i in lst:
        print(i)


def char_sequences(char, char_list, n):
    """
    Creates a list with sequences of the char with the char list
    :param char: the given char
    :param char_list: the given char list
    :param n: the length of the sequence
    :return: list with all of the sequences of the given char
    """
    if n <= 1:
        return char
    lst = []
    for i in char_list:
        lst.extend([char + seq for seq in
                    char_sequences(i, char_list, n - 1)])
    return lst


def no_repetition_char_sequences(char, char_list, n, rep_lst):
    """
    Creates a list with all of the sequences without repetitions of the given
    char
    :param char: the given char
    :param char_list: the given char list
    :param n: the length of the sequence
    :param rep_lst: list with the repetitions
    :return: list with all of the sequences of the given char
    """
    if n <= 1:
        return char
    lst = []
    for i in char_list:
        if i not in rep_lst:
            rep_lst.append(i)
            lst.extend([char + seq for seq in
                        no_repetition_char_sequences(i, char_list, n - 1,
                                                     rep_lst)])
            rep_lst.remove(i)
    return lst


def print_no_repetition_sequences(char_list, n):
    """
    Creates a list with all of the sequences without repetitions
    :param char_list: teh char list
    :param n: the length of the sequence
    """
    if n < 1:
        return
    elif n == 1:
        print_list(char_list)
    else:
        lst = []
        for char in char_list:
            lst.extend(no_repetition_char_sequences(char, char_list, n,
                                                    [char]))
        print_list(lst)


def parentheses(n):
    """
    Creates a list with all of the valid ( ) combinations
    :param n: the number of ()
    :return: list with all of the strings that are valid
    """
    if n == 0:
        return ['']
    all_parentheses = create_parent('(', ['(', ')'], n * 2)
    final_lst = all_parentheses[:]
    for i in all_parentheses:
        if i.count('(') != i.count(')'):
            final_lst.remove(i)
        elif not check_parent(i, 0, 0, n * 2):
            final_lst.remove(i)
    return final_lst


def create_parent(char, char_list, n):
    """
    Creates a list with all of the combinations
    :param char: (
    :param char_list: list with ( )
    :param n: the length of the string
    :return: list with all of the combinations
    """
    if n <= 1:
        return char
    lst = []
    for i in char_list:
        lst.extend([char + seq for seq in
                    char_sequences(i, char_list, n - 1) if
                    (char + seq).count('(') == (char + seq).count(')')])
    return lst


def check_parent(parent, counter1, counter2, n):
    """
    checks if the string is valid
    :param parent: the checked string
    :param counter1: counter of (
    :param counter2: counter of )
    :param n: the place in the string
    :return: True if valid, else False
    """
    if n == 0:
        return True
    if counter1 < counter2:
        return False
    if parent[0] == '(':
        return check_parent(parent[1:], counter1 + 1, counter2, n - 1)
    else:
        return check_parent(parent[1:], counter1, counter2 + 1, n - 1)


def flood_fill(image, start):
    """
    floods the image according to the given location using all of the funcs
    :param image: two dimensional list with the given image
    :param start: the position
    """
    image[start[0]][start[1]] = '*'
    if len(image) <= 1:
        return
    else:
        flood_fill_all(image, start)


def flood_fill_right(image, start):
    """
    floods the row to the right
    :param image: two dimensional list with the given image
    :param start: the position
    """
    if start[1] == len(image[0]):
        return
    if image[start[0]][start[1]] == ".":
        image[start[0]][start[1]] = '*'
        flood_fill_all(image, start)


def flood_fill_left(image, start):
    """
    floods the row to the left
    :param image: two dimensional list with the given image
    :param start: the position
    """
    if start[1] == 0:
        return
    if image[start[0]][start[1]] == ".":
        image[start[0]][start[1]] = '*'
        flood_fill_all(image, start)


def flood_fill_down(image, start):
    """
    floods the col downward
    :param image: two dimensional list with the given image
    :param start: the position
    """
    if start[1] == len(image):
        return
    if image[start[0]][start[1]] == ".":
        image[start[0]][start[1]] = '*'
        flood_fill_all(image, start)


def flood_fill_up(image, start):
    """
    flood the col upward
    :param image: two dimensional list with the given image
    :param start: the position
    """
    if start[1] == 0:
        return
    if image[start[0]][start[1]] == ".":
        image[start[0]][start[1]] = '*'
        flood_fill_all(image, start)


def flood_fill_all(image, start):
    """
    floods to all directions from a given point
    :param image: two dimensional list with the given image
    :param start: the position
    """
    flood_fill_right(image, (start[0], start[1] + 1))
    flood_fill_left(image, (start[0], start[1] - 1))
    flood_fill_down(image, (start[0] + 1, start[1]))
    flood_fill_up(image, (start[0] - 1, start[1]))