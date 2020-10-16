class Car:
    """
    Car class. Creates an object from Car type that has 4 properties - name,
    length, location and orientation. The class has few functions that are used
    to get information about it or to check how it could be moved.
    """
    MOVES_DICT = {
        'r': [0, 1],
        'l': [0, -1],
        'u': [-1, 0],
        'd': [1, 0]
    }

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        if self.__orientation:
            return [(self.__location[0], self.__location[1] + i) for i
                    in range(self.__length)]
        return [(self.__location[0] + i, self.__location[1]) for i
                in range(self.__length)]

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        if self.__orientation:
            return {
                'r': "You can go right",
                'l': "You can go left"
            }
        else:
            return {
                'u': "You can go up",
                'd': "You can go down"
            }

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        if movekey == 'd':
            return [(self.__location[0] + self.__length, self.__location[1])]
        elif movekey == 'u':
            return [(self.__location[0] - 1, self.__location[1])]
        elif movekey == 'r':
            return [(self.__location[0], self.__location[1] + self.__length)]
        elif movekey == 'l':
            return [(self.__location[0], self.__location[1] - 1)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False
        self.__update_location(movekey)
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name

    def __update_location(self, movekey):
        """
        Updates the car location variable
        :param movekey: A string representing the key of the required move.
        """
        self.__location = (self.__location[0] + self.MOVES_DICT[movekey][0],
                           self.__location[1] + self.MOVES_DICT[movekey][1])
