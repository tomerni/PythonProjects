########################
# FILE : hangman.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex4 2019-2020
# DESCRIPTION: Hangman game
########################

import hangman_helper;


def update_word_pattern(word, pattern, letter):
    """
    Updates the pattern according to the letter and the word
    :param word: The word that is being guessed
    :param pattern: The current pattern
    :param letter: The letter that the user guessed
    :return: If the letter is in the word returns tuple with True, the updated
    pattern and the number of appears of the letter in the word.
    Else returns a list with 1 False.
    """
    updated_pattern = ""
    letter_appears_counter = 0
    if letter in word:
        index = 0
        while index < len(word):
            if word[index] == letter:
                updated_pattern += letter
                index += 1
                letter_appears_counter += 1
            else:
                updated_pattern += pattern[index]
                index += 1
        return updated_pattern
    else:
        return pattern


def check_correct_word_guess(word, pattern, guess):
    """
    Checks if the word guess is correct
    :param word: The word that is being guessed
    :param pattern: The current pattern
    :param guess: The word guess that the user entered
    :return: If it is a correct guess returns tuple with True and the score
    that the player got.
    Else returns tuple with False and -1.
    """
    # Correct entire word guess
    if word == guess:
        num_of_underscore = pattern.count("_")
        return True, ((num_of_underscore * (num_of_underscore + 1)) // 2) - 1
    # Incorrect entire word guess
    else:
        return False, -1


def create_empty_pattern(word):
    """
    Creates an empty pattern of _ according to the length of the word
    :param word: The word that is being guessed
    :return: The empty pattern
    """
    pattern = "_" * len(word)
    return pattern


def check_guess(word, guess):
    """
    Checks if the guess is valid
    :param word: The word that is being guessed
    :param guess: The guess of the user
    :return: If the guess is invalid returns a tuple with 2 False.
    If the guess is hint returns tuple with True and "hint", Else if the guess
    is a valid word returns a tuple with True and "word". Else returns a tuple
    with True and "letter".
    """
    # Checks for a hint:
    if guess[0] == hangman_helper.HINT:
        return True, "hint"
    # The guess is a letter:
    elif guess[0] == hangman_helper.LETTER:
        if len(guess[1]) > 1 or not guess[1].islower():
            return False, False
            # Checks for an empty guess:
        if guess[1] == "":
            return False, False
        return True, "letter"
    # Checks if the guess is a word
    elif guess[0] == hangman_helper.WORD:
        return True, "word"
    else:
        return False, False


def win_check(word, pattern):
    """
    Checks if the player won
    :param word: The word that is being guessed
    :param pattern: The current pattern
    :return: Returns True if the pattern is the word, else False
    """
    if word == pattern:
        return True
    return False


def match_word_pattern(word, pattern):
    """
    Checks if the word matches the pattern
    :param word: The word that is being checked
    :param pattern: The current pattern
    :return: If the word matches the pattern returns True, else False
    """
    index = 0
    # Checking every character:
    while index < len(word):
        if pattern[index] != '_' and pattern[index] != word[index]:
            return False
        index += 1
    return True


def filter_wrong_guess(hint, pattern, wrong_guess_list):
    """
    Checks if the possible hint has a wrong letters in it or correct letters
    in the wrong places.
    :param hint: The hint that is being checked
    :param pattern: The current pattern
    :param wrong_guess_list: The list of the wrong letters
    :return: If the word has a wrong letter returns False, else True
    """
    correct_letters = set(pattern.replace('_', ''))
    for correct_letter in correct_letters:
        if hint.count(correct_letter) != pattern.count(correct_letter):
            return False
    for wrong_letter in wrong_guess_list:
        if wrong_letter in hint:
            return False
    return True


def filter_words_list(words, pattern, wrong_guess_list):
    """
    Filters out the words that don't match the pattern or have wrong letters
     in them.
    :param words: The list off all the optional words
    :param pattern: The current pattern
    :param wrong_guess_list: The list of the wrong guesses
    :return: The list of all the optional hints
    """
    optional_words = []
    for word in words:
        # Checks if the length of the word doesn't match the length of pattern:
        if len(word) != len(pattern):
            continue
        # Checks if the word doesn't match the pattern:
        if not match_word_pattern(word, pattern):
            continue
        # Check if the word has wrong letters in it:
        if not filter_wrong_guess(word, pattern, wrong_guess_list):
            continue
        # Otherwise append the word to the optional word hints
        optional_words.append(word)
    return optional_words


def hint_list_cutter(size, hints_list):
    """
    Cuts the length of the hint list so that it will match the given size
    :param size: The size the the list should be in
    :param hints_list: The current hints list
    :return: Short hint list according to the given size
    """
    hints_list_length = len(hints_list)
    # Cuts the hints list according to the specifications:
    final_hint_list = [hints_list[i // size] for i in
                       range(0, hints_list_length * size,
                             hints_list_length)]
    return final_hint_list


def run_single_game(words_list, score):
    """
    Runs a game of hangman using all of the above functions
    :param words_list: The list of words from which the game word is being
    choose.
    :param score: The current score of the player
    :return: The score of the player at the end of the game - 0 if he lost the
    game, else a number greater then 0
    """
    word = hangman_helper.get_random_word(words_list)
    guesses_list = []
    pattern = create_empty_pattern(word)
    # So that first time string print will happen only once:
    first_time_flag = True
    # Main loop of the turn:
    while score > 0:
        # First run print:
        if not guesses_list and first_time_flag:
            hangman_helper.display_state(pattern, guesses_list, score,
                                         "Welcome to the game!")
            first_time_flag = False
        # Gets the guess:
        guess_input = hangman_helper.get_input()
        # Uses check_guess to get information about the guess:
        valid, guess_type = check_guess(word, guess_input)
        # Checks for a clue input:
        if guess_type == "hint":
            score -= 1
            hints = filter_words_list(words_list, pattern, guesses_list)
            # Hint list length is too long so we cut it using hint_list_cutter:
            if len(hints) > hangman_helper.HINT_LENGTH:
                cutted_hints = hint_list_cutter(hangman_helper.HINT_LENGTH,
                                                hints)
                hangman_helper.show_suggestions(cutted_hints)
                # Checks if the player lost because he took a clue:
                if score == 0:
                    break
                else:
                    hangman_helper.display_state(pattern, guesses_list, score,
                                                 "Another round!")
            # Hints list length is ok:
            else:
                hangman_helper.show_suggestions(hints)
                # Checks if the player lost because he took a clue:
                if score == 0:
                    break
                else:
                    hangman_helper.display_state(pattern, guesses_list, score,
                                                 "Another round!")
        # Checks for invalid input:
        elif not valid or (guess_input[1] == "" and guess_input[0] == 1):
            hangman_helper.display_state(pattern, guesses_list, score,
                                         "Invalid guess! Try again")
            continue
        # Checks for an old guess:
        elif guess_input[0] == hangman_helper.LETTER and (guess_input[1] in
                                                          guesses_list or
                                                          guess_input[1] in
                                                          pattern):
            hangman_helper.display_state(pattern, guesses_list, score,
                                         "You have already guessed that!")
            continue
        # Valid input:
        else:
            # Checks for a letter guess:
            if guess_type == "letter":
                update_pattern = update_word_pattern(word, pattern,
                                                     guess_input[1])
                # Checks for correct guess:
                if update_pattern != pattern:
                    score -= 1
                    # The updated pattern after the correct guess:
                    pattern = update_pattern
                    # The number of appearances of the letter in the word
                    appears_num = int(pattern.count(guess_input[1]))
                    # The updated score:
                    score += (appears_num * (appears_num + 1)) // 2
                    # Checks for a win:
                    if win_check(word, pattern):
                        break
                # Wrong letter guess:
                else:
                    score -= 1
                    # Add the guess to the wrong guesses list:
                    guesses_list.append(guess_input[1])
                    # Checks if the player lost:
                    if score == 0:
                        break
            # Word guess:
            else:
                # Using the check_correct_word to update the score because it
                # returns -1 if the guess is incorrect, else
                # returns the amount of points that that player get
                is_win, adding_score = check_correct_word_guess(word, pattern,
                                                                guess_input[1])
                score += adding_score
                # Checks if the player lost
                if score == 0:
                    break
                if is_win:
                    pattern = guess_input[1]
                    break
            hangman_helper.display_state(pattern, guesses_list, score,
                                         "Another round!")
    # The player won:
    if score > 0:
        hangman_helper.display_state(pattern, guesses_list, score,
                                     "You won the game!")
        return score
    # The player lost:
    else:
        hangman_helper.display_state(pattern, guesses_list, score,
                                     f"You lost the game. The word was {word}")
        return score


def main():
    """
    Function that runs a full session of hangman games until the player decide
    to stop
    """
    # Gets the word list from the file:
    WORD_LIST = hangman_helper.load_words()
    # Sets the score to the initial points:
    score = hangman_helper.POINTS_INITIAL
    games_played = 0
    # The main game loop:
    while True:
        games_played += 1
        # Runs a single game:
        game_score = run_single_game(WORD_LIST, score)
        # Checks if the player won:
        if game_score > 0:
            score = game_score
            # Asks the player if he wants to play again:
            play_again = hangman_helper.play_again(
                f"Number of games so far: {games_played}."
                f" Your current score: {score}. "
                f"Want to continue?")
            # Continues to play with the same score and games played:
            if play_again:
                continue
            else:
                break
        # Checks if the player lost:x`
        else:
            # Asks the player if he wants to play again:
            play_again = hangman_helper.play_again(
                f"Number of games survived: {games_played}. "
                f"Start a new series of games?")
            # Continues to play but with 0 games played and the initial score
            if play_again:
                games_played = 0
                score = hangman_helper.POINTS_INITIAL
                continue
            else:
                break


if __name__ == "__main__":
    main()
