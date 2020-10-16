import math


class Ship:
    """
    This is a ship object. The ship has 6 variables - speed in the X and Y axis
    , location in the X and Y axis, heading and the radius of the ship.
    You can get the values of the variables using the get methods and change
    the speed, location and heading using the set methods - change_speed(),
    change_location(), change_heading().
    """
    RADIUS = 1

    def __init__(self, speed_x, speed_y, location_x, location_y, heading):
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__location_x = location_x
        self.__location_y = location_y
        self.__heading = heading
        self.__radius = self.RADIUS

    def get_speed(self):
        """
        :return: Tuple with the speed of the ship
        """
        return self.__speed_x, self.__speed_y

    def get_location(self):
        """
        :return: Tuple with the location of the ship
        """
        return self.__location_x, self.__location_y

    def get_heading(self):
        """
        :return: The heading of the ship
        """
        return self.__heading

    def get_radius(self):
        """
        :return: The radius of the ship
        """
        return self.__radius

    def change_heading(self, degrees):
        """
        Sets the new heading according to the degrees
        :param degrees: The degrees that the heading should be changed
        """
        self.__heading += degrees

    def change_speed(self):
        """
        Sets the speed according to the formula
        """
        self.__speed_x += math.cos(math.radians(self.__heading))
        self.__speed_y += math.sin(math.radians(self.__heading))

    def change_location(self, new_location):
        """
        Sets the location according to the new location
        :param new_location: Tuple with the new location of the ship
        """
        self.__location_x = new_location[0]
        self.__location_y = new_location[1]