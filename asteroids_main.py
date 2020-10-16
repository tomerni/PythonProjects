from screen import Screen
import sys
from ship import Ship
from torpedo import Torpedo
import math
import random
from asteroid import Asteroid

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """
    This is a Game_Runner object. Responsible for the running of the game,
    contains a method that manages the points of the player in the game,
    contains methods that define the movement of all objects in the game, as
    well as methods for checking whether the objects in the game collided with
    each other. Also - this object contains calls to functions from the SCREEN
    object which aid in the general presentation of the game.
    """

    DEGREES = 7
    TORPEDO_LIFE = 200
    NUMBER_OF_TORPEDOS = 10
    LIFE = 3
    MESSAGE_FOR_INTERSECTION = "You hit an asteroid"
    MESSAGE_FOR_WIN = "You WON!"
    MESSAGE_FOR_LOST = "You LOST!"
    MESSAGE_FOR_EXIT = "You choose to end the game"
    SCORE_DICT = {1: 100,
                  2: 50,
                  3: 20}
    DEFAULT_ASTEROID_SIZE = 3
    OPTIONAL_ASTEROID_SPEED = [-4, -3, -2, -1, 1, 2, 3, 4]

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__asteroids_amount = asteroids_amount
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = self._set_ship()
        self.__torpedos = []
        self.__asteroids = self._set_asteroid(self.__asteroids_amount)
        self.__torpedo_counter = 0
        self.__current_turn = 0
        self.__life = self.LIFE
        self.__score = 0

    def _set_ship(self):
        """
        :return: Ship object with a random location on the screen
        """
        return Ship(0, 0, random.randint(self.__screen_min_x, self.
                                         __screen_max_x),
                    random.randint(self.__screen_min_y, self.__screen_max_y),
                    0.0)

    def _set_asteroid(self, amount):
        """
        Creates the given amount of the asteroids in random places on the
        screen
        :param amount: The number of the asteroids that the game should
        initiate with
        :return: list with all of the asteroids
        """
        asteroids = []
        for ast in range(amount):
            loc_x = random.randint(self.__screen_min_x, self.__screen_max_x)
            loc_y = random.randint(self.__screen_min_y, self.__screen_max_y)
            while (loc_x, loc_y) == self.__ship.get_location():
                loc_x = random.randint(self.__screen_min_x, self.__screen_max_x)
                loc_y = random.randint(self.__screen_min_y, self.__screen_max_y)
            asteroid = Asteroid(loc_x, loc_y,
                                random.choice(self.OPTIONAL_ASTEROID_SPEED),
                                random.choice(self.OPTIONAL_ASTEROID_SPEED),
                                self.DEFAULT_ASTEROID_SIZE)
            asteroids.append(asteroid)
            self.__screen.register_asteroid(asteroid, asteroid.get_size())
        return asteroids

    def asteroid_split(self, asteroid, torspeed):
        """
        Splits or removes the give asteroid according to his size.
        :param asteroid: The asteroid that was hit
        :param torspeed: The speed of the torpedo that hit the asteroid
        """
        if asteroid.get_size() == 1:
            self.__screen.unregister_asteroid(asteroid)
            self.__asteroids.remove(asteroid)
            self.__asteroids_amount -= 1
        if asteroid.get_size() in [2, 3]:
            self.__screen.unregister_asteroid(asteroid)
            self.__asteroids.remove(asteroid)
            location_x, location_y = asteroid.get_location()
            speed_1_x, speed_1_y = self._change_speed_asteroid(asteroid,
                                                              torspeed)
            ast_1 = Asteroid(location_x, location_y, speed_1_x, speed_1_y,
                             asteroid.get_size() - 1)
            ast_2 = Asteroid(location_x, location_y, -speed_1_x, -speed_1_y,
                             asteroid.get_size() - 1)
            self.__asteroids.append(ast_1)
            self.__asteroids.append(ast_2)
            self.__screen.register_asteroid(ast_1, ast_1.get_size())
            self.__screen.register_asteroid(ast_2, ast_2.get_size())
            self.__asteroids_amount += 1

    def _change_speed_asteroid(self, asteroid, torspeed):
        """
        Calculates the speed of the asteroid after he was hit and splitted
        :param asteroid: The asteroid that was hit
        :param torspeed: The speed of the torpedo that hit the asteroid
        :return: Tuple with the new speed of the asteroid
        """
        torpedo_x, torpedo_y = torspeed
        ast_x, ast_y = asteroid.get_speed()
        new_speed_x = (torpedo_x + ast_x) / (ast_x ** 2 + ast_y ** 2) ** 0.5
        new_speed_y = (torpedo_y + ast_y) / (ast_x ** 2 + ast_y ** 2) ** 0.5
        return new_speed_x, new_speed_y

    def _ship_intersection(self):
        """
        Checks if the ship had an intersection with the asteroids. If true
        removes the asteroid and reduces live by 1.
        """
        for ast in self.__asteroids:
            if ast.has_intersection(self.__ship):
                self.__life -= 1
                self.__screen.show_message("hit", self.MESSAGE_FOR_INTERSECTION)
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(ast)
                self.__asteroids.remove(ast)
                self.__asteroids_amount -= 1

    def _torpedo_intersection(self):
        """
        Checks if any of the torpedos had an intersection with any of the
        asteroids
        """
        for torpedo in self.__torpedos:
            for ast in self.__asteroids:
                if ast.has_intersection(torpedo):
                    self._add_score(self.SCORE_DICT[ast.get_size()])
                    self.__screen.set_score(self.__score)
                    self.asteroid_split(ast, torpedo.get_speed())

    def _add_score(self, score):
        """
        Updates the score according to the given score
        :param score: The score that the player got
        """
        self.__score += score

    def _move_asteroid(self):
        """
        Moves the asteroids using the _move_object() method
        """
        for ast in self.__asteroids:
            ast.change_location(self._move_object(ast))

    def _move_object(self, obj):
        """
        Calculates the new location of the object according to the formula
        :param obj: An object from type Ship, asteroid or torpedo
        :return: Tuple with the new location of the object
        """
        delta_x = self.__screen_max_x - self.__screen_min_x
        delta_y = self.__screen_max_y - self.__screen_min_y
        newspot_x = self.__screen_min_x + (obj.get_location()[0] +
                                           obj.get_speed()[
                                               0] - self.__screen_min_x) % delta_x
        newspot_y = self.__screen_min_y + (obj.get_location()[1] +
                                           obj.get_speed()[
                                               1] - self.__screen_min_y) % delta_y
        return newspot_x, newspot_y

    def _move_remove_torpedos(self):
        """
        Moves or removes the torpedos in the game according their variables.
        """
        for torpedo in self.__torpedos:
            if self.__current_turn - torpedo.get_turn() < self.TORPEDO_LIFE:
                torpedo.change_location(self._move_object(torpedo))
                torpedo_location_x, torpedo_location_y = torpedo.get_location()
                self.__screen.draw_torpedo(torpedo, torpedo_location_x,
                                           torpedo_location_y,
                                           torpedo.get_heading())
            else:
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedos.remove(torpedo)
                self.__torpedo_counter -= 1

    def _move_ship(self):
        """
        Moves the ship using the _move_object() method
        """
        self.__ship.change_location(self._move_object(self.__ship))

    def _is_move_pressed(self):
        """
        Checks if any of the moving keys - right, left, up, were pressed.
        If true does the change according to the key
        """
        if self.__screen.is_left_pressed():
            self.__ship.change_heading(self.DEGREES)
        if self.__screen.is_right_pressed():
            self.__ship.change_heading(-self.DEGREES)
        if self.__screen.is_up_pressed():
            self.__ship.change_speed()

    def _is_space(self):
        """
        Checked if space was pressed. If true adds a torpedo to the game.
        """
        x_location, y_location = self.__ship.get_location()
        ship_heading = self.__ship.get_heading()
        if self.__screen.is_space_pressed() and self.__torpedo_counter < \
                self.NUMBER_OF_TORPEDOS:
            torp_speed_x, torp_speed_y = self._calc_torpedo_speed()
            ship_torpedo = Torpedo(x_location, y_location, torp_speed_x,
                                   torp_speed_y, ship_heading,
                                   self.__current_turn)
            self.__torpedos.append(ship_torpedo)
            self.__torpedo_counter += 1
            self.__screen.register_torpedo(ship_torpedo)

    def _calc_torpedo_speed(self):
        """
        Calculates the speed of the torpedo
        :return: Tuple with the speed
        :return: Tuple with the speed
        """
        x_speed, y_speed = self.__ship.get_speed()
        ship_heading = self.__ship.get_heading()
        new_x = x_speed + 2 * math.cos(math.radians(ship_heading))
        new_y = y_speed + 2 * math.sin(math.radians(ship_heading))
        return new_x, new_y

    def _draw_asteroid(self):
        """
        Draws the asteroids according to their location
        :return:
        """
        for ast in self.__asteroids:
            self.__screen.draw_asteroid(ast, ast.get_location()[0],
                                        ast.get_location()[1])

    def _draw_ship(self):
        """
        Drawing the ship on the screen according the location and headind
        """
        x_location, y_location = self.__ship.get_location()
        ship_heading = self.__ship.get_heading()
        self.__screen.draw_ship(x_location, y_location, ship_heading)

    def _update_turn(self):
        """
        Updates the turns counter
        """
        self.__current_turn += 1

    def _is_game_over(self):
        """
        Checks if the game is over
        :return: If the game is over returns True and the relevant message,
        else returns False
        """
        if self.__life == 0:
            return True, self.MESSAGE_FOR_LOST
        if self.__asteroids_amount == 0:
            return True, self.MESSAGE_FOR_WIN
        if self.__screen.should_end():
            return True, self.MESSAGE_FOR_EXIT
        return False, False

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!

        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # TODO: Your code goes here
        self._update_turn()
        self._draw_ship()
        self._move_ship()
        self._is_move_pressed()
        self._draw_asteroid()
        self._move_asteroid()
        self._ship_intersection()
        self._is_space()
        self._move_remove_torpedos()
        self._torpedo_intersection()
        if self._is_game_over()[0]:
            self.__screen.show_message("Message", self._is_game_over()[1])
            self.__screen.end_game()
            sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
