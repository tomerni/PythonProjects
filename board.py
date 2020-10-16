class Board:
    """
    Board class. Creates an object from Board type that has 3 properties -
    list with the content of the board, the length of the board and a dict
    with the cars objects on the board. This object is used in the game rush
    hour and have few functions that lets the user get information about the
    board and few functions that are specific for the game.
    """
    GOAL_LOCATION = (3, 7)
    BOARD_LENGTH = 7
    ROWS_TEMP_1 = ([None] * BOARD_LENGTH)
    ROWS_TEMP_2 = ([None] * (BOARD_LENGTH + 1))

    def __init__(self):
        lst = []
        for i in range(self.BOARD_LENGTH):
            if i == self.GOAL_LOCATION[0]:
                lst.append(self.ROWS_TEMP_2[:])
            else:
                lst.append(self.ROWS_TEMP_1[:])
        self.board = lst[:]
        self.__cars = {}
        self.__length = self.BOARD_LENGTH

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        final_str = ''
        for i in range(self.BOARD_LENGTH):
            row = ''
            for j in range(self.BOARD_LENGTH + 1):
                if j == self.BOARD_LENGTH:
                    if i != self.GOAL_LOCATION[0]:
                        row += " "
                    else:
                        if self.board[i][j] is None:
                            row += '*'
                        else:
                            row += self.board[i][j]
                else:
                    if self.board[i][j] is None:
                        row += '_ '
                    else:
                        row += self.board[i][j] + ' '
            row += '\n'
            final_str += row
        return final_str[:-1]

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        lst = [(i, j) for i in range(self.BOARD_LENGTH) for j in
               range(self.BOARD_LENGTH)]
        lst.append(self.GOAL_LOCATION)
        return lst

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        lst = []
        for car in self.__cars.keys():
            moves = self.__cars[car].possible_moves()
            for move in moves.keys():
                cords_of_move = self.__cars[car].movement_requirements(move)
                if cords_of_move[0] == self.target_location():
                    lst.append([self.__cars[car].get_name(), move, moves[move]])
                elif cords_of_move[0] not in self.cell_list():
                    continue
                elif self.cell_content(cords_of_move[0]) is not None:
                    continue
                else:
                    lst.append((self.__cars[car].get_name(), move, moves[move]))
        return lst

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        return self.GOAL_LOCATION

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if self.board[coordinate[0]][coordinate[1]] is None:
            return None
        return self.board[coordinate[0]][coordinate[1]]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        car_cord = car.car_coordinates()
        if car.get_name() in self.__cars.keys():
            return False
        for cord in range(len(car_cord)):
            if car_cord[cord] not in self.cell_list() or \
                    self.cell_content(car_cord[cord]) is not None:
                return False
        self.__update_cars(car)
        self.__update_location(car)
        return True

    def __update_cars(self, car):
        """
        Adding the new car on the board to the car dict.
        :param car: car object of car to add
        """
        self.__cars[car.get_name()] = car

    def __update_location(self, car):
        """
        Updates the car location after a move on the board.
        :param car: car object of car to update in the board
        """
        cords = car.car_coordinates()
        for cord in cords:
            self.board[cord[0]][cord[1]] = car.get_name()

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.__cars.keys():
            return False
        car = self.__cars[name]
        possible_moves = car.possible_moves()
        if movekey not in possible_moves:
            return False
        else:
            target_cord = car.movement_requirements(movekey)
            if target_cord[0] != self.GOAL_LOCATION and (target_cord[0] not in
                                                         self.cell_list() or
                                                         self.cell_content(
                                                             target_cord[
                                                                 0]) is not
                                                         None):
                return False
            else:
                old_cord = car.car_coordinates()
                car.move(movekey)
                new_cord = car.car_coordinates()
                for i in new_cord:
                    if i in old_cord:
                        old_cord.remove(i)
                for j in range(len(old_cord)):
                    self.board[old_cord[j][0]][old_cord[j][1]] = None
                self.__update_location(car)
                return True
