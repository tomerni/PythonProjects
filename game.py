########################
# FILE : game.py
# WRITER: Tomer Nissim, tomerni, 313232845
# EXERCISE: intro2cs1 Ex9 2019-2020
# DESCRIPTION: Rush hour game
########################


class Game:
    """
    Creates a game object that lets the user play a rush hour game. The object
    has two properties - board which contains a Board object and a tuple with
    the game wining position. The object has a few functions that control the
    game, gets inputs from the user and checks for win.
    """
    VALID_NAMES = ['Y', 'B', 'O', 'G', 'W', 'R']
    VALID_MOVES = ['r', 'l', 'd', 'u']
    MIN_LENGTH = 2
    MAX_LENGTH = 4
    VALID_ORIENTATION = [0, 1]

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board
        self.__target = self.board.target_location()

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        while True:
            possible_moves = self.board.possible_moves()
            print('Those are all of your valid moves:')
            for move in possible_moves:
                print(f'{move[0]} - {move[2]} ({move[1]})')
            user_input = input("Enter the move: ")
            if user_input == '!':
                print('Exiting')
                return False
            if not self.__check_input(user_input):
                print("This is an illegal move, please try again")
                continue
            car_name, car_move = user_input[0], user_input[2]
            # Check for winner move
            if self.board.board[self.__target[0]][self.__target[1] - 1] == \
                    car_name and self.__check_move(possible_moves, car_name,
                                                   car_move) \
                    and car_move == 'r':
                self.board.move_car(car_name, car_move)
                print(self.board)
                print("You won!")
                return False
            # Valid move
            if self.board.move_car(car_name, car_move):
                print(self.board)
                return True
            else:
                print("This is an illegal move, please try again")
                continue

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # Checks for early win
        if self.__check_win():
            print(self.board)
            print("You won!")
            return
        flag = True
        while flag:
            flag = self.__single_turn()

    def __check_input(self, user_input):
        """
        Checks if the user input is valid.
        :param user_input: The input from the user
        :return: True if valid, False otherwise
        """
        if len(user_input) > 3 or ',' not in user_input:
            return False
        car_name, car_move = user_input[0], user_input[2]
        if car_name not in self.VALID_NAMES or car_move not in \
                self.VALID_MOVES:
            return False
        return True

    def __check_win(self):
        """
        Checks for win while adding the cars, without doing any move
        :return: True for win, False otherwise
        """
        goal = self.board.target_location()
        if self.board.board[goal[0]][goal[1]] is not None:
            return True
        return False

    def __check_move(self, moves_list, car_name, move):
        """

        :param car_name:
        :param move:
        :return:
        """
        for i in moves_list:
            if i[0] == car_name and i[1] == move:
                return True
        return False


if __name__ == "__main__":
    import helper
    import sys
    import board
    import car
    game_board = board.Board()
    json = helper.load_json(sys.argv[1])
    # Initiating the board according to the json
    for i in json.keys():
        length, location, orientation = json[i]
        if not 2 <= length <= 4 or orientation not in [0, 1] or i not in \
                ['Y', 'B', 'O', 'G', 'W', 'R'] or tuple(location) not in \
                game_board.cell_list():
            print(f"Did not succeed to put {i} in the board")
        else:
            current_car = car.Car(i, length, tuple(location), orientation)
            add_flag = game_board.add_car(current_car)
            if add_flag:
                print(f"Succeeded to put {i} in the board")
            else:
                print(f"Did not succeed to put {i} in the board")
    game = Game(game_board)
    print(game.board)
    game.play()
