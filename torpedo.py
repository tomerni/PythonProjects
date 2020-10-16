class Torpedo:
    """
    This is a torpedo object. The torpedo has 7 variables - location in the
    X and Y axis, speed in the X and Y axis, heading, the turn he was created
    and the radius. You can get all of the variables using the get methods and
    you can change to location of the torpedo using the change_location()
    method.
    """

    RADIUS = 4

    def __init__(self, location_x, location_y, speed_x, speed_y, heading, turn):
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__location_x = location_x
        self.__location_y = location_y
        self.__heading = heading
        self.__turn = turn
        self.__radius = self.RADIUS

    def get_location(self):
        """
        :return: Tuple with the location
        """
        return self.__location_x, self.__location_y

    def get_speed(self):
        """
        :return: Tuple with the speed
        """
        return self.__speed_x, self.__speed_y

    def get_heading(self):
        """
        :return: The heading of the torpedo
        """
        return self.__heading

    def get_turn(self):
        """
        :return: The turn that the torpedo was created
        """
        return self.__turn

    def get_radius(self):
        """

        :return: The radius of the torpedo
        """
        return self.__radius

    def change_location(self, new_location):
        """
        Sets the location according to the new location
        :param new_location: Tuple with the new location of the torpedo
        """
        self.__location_x = new_location[0]
        self.__location_y = new_location[1]