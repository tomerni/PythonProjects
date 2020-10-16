class Asteroid:
    """
    This is an asteroid object. The object has 6 variables - location and speed
    in the X and Y axis, size and radius. You can get the variables using the
    get methods, and change the location using the change_location() function.
    The asteroid has a method named had_intersection() that checks if he had an
     intersection with a given object.
    """

    def __init__(self, loc_on_x, loc_on_y, speed_on_x, speed_on_y, size):
        self.__loc_on_x_axis = loc_on_x
        self.__speed_on_x_axis = speed_on_x
        self.__loc_on_y_axis = loc_on_y
        self.__speed_on_y_axis = speed_on_y
        self.__size = size
        self.__radius = self.__size * 10 - 5

    def get_radius(self):
        """
        :return: The radius
        """
        return self.__radius

    def get_size(self):
        """
        :return: The size
        """
        return self.__size

    def get_location(self):
        """
        :return: Tuple with the location in the X and Y axis
        """
        return self.__loc_on_x_axis, self.__loc_on_y_axis

    def get_speed(self):
        """
        :return: Tuple with the speed in the X and Y axis
        """
        return self.__speed_on_x_axis, self.__speed_on_y_axis

    def change_location(self, location):
        """
        Changes the location according to the given location
        :param location: Tuple with the new location of the ship
        """
        self.__loc_on_x_axis = location[0]
        self.__loc_on_y_axis = location[1]

    def has_intersection(self, obj):
        """
        Checks for an intersection with the given object
        :param obj: Object from type Ship or Torpedo
        :return: True if an intersection happened, else False
        """
        obj_x, obj_y = obj.get_location()
        distance = ((obj_x - self.__loc_on_x_axis) ** 2 + (
                    obj_y - self.__loc_on_y_axis) ** 2) ** 0.5
        if distance <= self.__radius + obj.get_radius():
            return True
        return False
