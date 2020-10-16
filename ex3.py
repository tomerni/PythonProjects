########################
# FILE : ex3.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex3 2019-2020
# DESCRIPTION: The functions from ex3
########################

def input_list():
    """This functions gets numbers as inputs from the user until an empty
    string and then returns a list with the numbers and the sum of them"""
    sum = 0
    flag = True
    final_list = []
    while flag:
        str_input = input()
        # Checks for empty string:
        if str_input == "":
            flag = False
        else:
            number = int(str_input)
            # Adds the number to the list:
            final_list.append(number)
            # Adds the number to the sum:
            sum += number
    final_list.append(sum)
    return final_list

def inner_product(vec_1, vec_2):
    """This function gets 2 lists and returns the inner product between them.
    If the lists are not in the same length the function returns None and
    if the lists are empty returns 0"""
    # Checks for different lengths:
    if len(vec_1) != len(vec_2):
        return None
    # Checks for two empty lists:
    elif vec_1 == [] and vec_2 == []:
        return 0
    else:
        sum = 0
        # Runs on the length of the lists:
        for i in range(len(vec_1)):
            sum += vec_1[i]*vec_2[i]
        return sum

def sequence_monotonicity(sequence):
    """This functions gets a list of numbers and returns a list with 4
    boolean statements according to the list monotonicity specifications"""
    # Creates a list with 4 true values:
    mono_list = [True]*4
    # Checks for edge cases:
    if len(sequence) == 1 or len(sequence) == 0:
        return mono_list
    # Runs until the length-1 so that i won't exit the list with i+1:
    for i in range(len(sequence)-1):
        if sequence[i] > sequence[i+1]: #checks monotonicity 0
            mono_list[0] = False
        if sequence[i] >= sequence[i+1]: #checks monotonicity 1
            mono_list[1] = False
        if sequence[i] < sequence[i+1]: #checks monotonicity 2
            mono_list[2] = False
        if sequence[i] <= sequence[i+1]: #checks monotonicity 3
            mono_list[3] = False
    return mono_list

def monotonicity_inverse(def_bool):
    """This function gets a list with 4 boolean values and returns a list
    with the right monotonicity if there is one, else returns None. The
    function uses check_monotonicity_inverse to check if the input is valid"""
    # Checks valid specifications
    if not check_monotonicity_inverse(def_bool):
        return None
    else:
        if def_bool[0] is True and def_bool[1] is not True \
                and def_bool[2] is not True:
            return [1,2,2,4]
        elif def_bool[0] is True and def_bool[1] is True\
                and def_bool[2] is not True:
            return [1,2,3,4]
        elif def_bool[0] is True and def_bool[2] is True:
            return [1,1,1,1]
        elif def_bool[2] is True and def_bool[3] is not True \
                and def_bool[0] is not True:
            return [4,3,3,1]
        elif def_bool[2] is True and def_bool[3] is True \
                and def_bool[0] is not True:
            return [4,3,2,1]
        else:
            return [1,-1,1,-1]

def check_monotonicity_inverse(def_bool):
    """This function checks if the values in the list are valid according
    to the monotonicity specifications. If they are returns True, else
    returns False"""
    if def_bool[0] is True and def_bool[3] is True:
        return False
    if def_bool[1] is True and (def_bool[2] is True or def_bool[3] is True):
        return False
    if def_bool[1] is True and def_bool[0] is False:
        return False
    if def_bool[3] is True and def_bool[2] is False:
        return False
    return True

def primes_for_asafi(n):
    """This function returns list of the first n prime numbers using the
    is_prime function"""
    prime_list = []
    counter = 0
    last_prime_location = 1
    while counter < n:
        # If the loop finds prime number, changes the flag to False:
        prime_flag = True
        while prime_flag:
            if is_prime(last_prime_location, prime_list):
                prime_list.append(last_prime_location)
                prime_flag = False
                # Because 2 is the first prime and the only even one,
                # im jumping only by 1 number
                if last_prime_location == 2:
                    last_prime_location += 1
                # This is how I don't check the even number after the last
                # prime because the prime has to be odd
                else:
                    last_prime_location += 2
            else:
                last_prime_location += 1
        counter += 1
    return prime_list

def is_prime(n,prime_list):
    """This function checks if the given number is prime by checking only
    if he is divided by the prime numbers that have already been found"""
    if n == 1:
        return False
    if n == 2:
        return True
    for i in prime_list:
        if n % i == 0:
            return False
        if i > n**0.5:
            return True

def sum_of_vectors(vec_list):
    """This function gets a list of vectors and returns the sum of them.
    If the given list is empty the functions returns None. If the lists
    insidse the given list are empty the function returns []"""
    final_vec = []
    if vec_list == []:
        return None
    elif vec_list[0] == []:
        return []
    else:
        # Runs only on one index at a time:
        for index_runner in range(len(vec_list[0])): #
            place_sum = 0
            # Runs on all of the lists:
            for lists_runner in range(len(vec_list)):
                place_sum += vec_list[lists_runner][index_runner]
            final_vec.append(place_sum)
    return final_vec

def num_of_orthogonal(vectors):
    """This function returns the number of orthogonal vectors in a given
    list of vectros"""
    orthogonal_counter = 0
    current_list_index = 0
    while current_list_index < len(vectors):
        checked_list = vectors[current_list_index]
        # Checks all the other list besides the current list:
        for j in vectors[(current_list_index+1):]:
            # Checks for orthogonal vectors:
            if inner_product(checked_list,j) == 0: #
                orthogonal_counter +=1
        current_list_index += 1
    return orthogonal_counter