import pygame
import random
import time
import sys


class Drawable:
    """Class represents an object that can be drawn on a Pygame window."""
    def __init__(self, coordinate_list, color_list):
        """
        Constructor for the Drawable class.
        :param coordinate_list: The coordinates of the square spots on the board the object occupies.
        :param color_list: The colors of all the square spots on the board the object occupies.
        """
        self.coordinate_list = coordinate_list
        self.color_list = color_list

    def get_color_list(self):
        return self.color_list

    def draw(self, surface_object):
        """
        Draws self on the screen without updating the screen (to prevent the game from lagging.)
        :param surface_object: The window to draw itself on.
        :type surface_object: pygame.Surface
        """
        for i in range(len(self.coordinate_list)):
            color = self.color_list[i]
            coordinate = self.coordinate_list[i]
            pixel_width = 25
            pygame.draw.rect(surface_object, color, (pixel_width * coordinate[0], pixel_width * coordinate[1], pixel_width, pixel_width))

    def get_coordinate_list(self):
        return self.coordinate_list


class Snake(Drawable):
    """Class that controls the Snake's behavior."""
    def __init__(self, coordinates, body_color, head_color):
        """Constructor for the Snake class.
        :param body_color: The color of the snake's body
        :type body_color: Tuple[int, int, int]
        :param head_color: The color of the snake's head
        :type head_color: Tuple[int, int, int]
        """
        super().__init__(coordinates, [body_color, head_color])
        self.body_color = body_color
        self.head_color = head_color

    def move(self, direction):
        """
        Moves the snake in the given direction.
        :param direction: The direction to move the snake in: left, right, up, or down
        :type direction: str
        """
        if direction == 'up':
            next_element = self.coordinate_list[-1]
            del self.coordinate_list[0]  # Remove the tail of the snake
            next_element = [next_element[0], next_element[1] - 1]  # Where the snake's head will be given its direction
            self.coordinate_list.append(next_element)
        elif direction == 'down':
            next_element = self.coordinate_list[-1]
            del self.coordinate_list[0]
            next_element = [next_element[0], next_element[1] + 1]
            self.coordinate_list.append(next_element)
        elif direction == 'left':
            next_element = self.coordinate_list[-1]
            del self.coordinate_list[0]
            next_element = [next_element[0] - 1, next_element[1]]
            self.coordinate_list.append(next_element)
        else:
            next_element = self.coordinate_list[-1]
            del self.coordinate_list[0]
            next_element = [next_element[0] + 1, next_element[1]]
            self.coordinate_list.append(next_element)

    def collides_with_coordinates(self, coordinates):
        """Returns whether the snake's body occupies the given coordinates.
        :param coordinates: The coordinates which the snake may occupy.
        :type coordinates: tuple
        """
        return self.get_coordinate_list().count(coordinates) > 0

    def grow(self, food_coordinate, direction):
        """
        Increases the length of the snake by one when it eats, in the given direction.
        :param food_coordinate: The coordinates where the food was located.
        :type food_coordinate: list
        :param direction: The direction the snake is moving in.
        :type direction: str
        """
        if direction == 'left':
            self.coordinate_list.append([food_coordinate[0] - 1, food_coordinate[1]])  # Add a new coordinate to the
            # list of coordinates the snake occupies
        elif direction == 'right':
            self.coordinate_list.append([food_coordinate[0] + 1, food_coordinate[1]])
        elif direction == 'up':
            self.coordinate_list.append([food_coordinate[0], food_coordinate[1] - 1])
        else:
            self.coordinate_list.append([food_coordinate[0], food_coordinate[1] + 1])
        self.color_list[-1] = self.body_color
        self.color_list.append(self.head_color)

    def is_dead(self, board_width, board_height):
        """
        Determines whether the snake has collided with a boundary or itself, in which case it's dead.
        :param board_width: The width of the game board
        :type board_width: int
        :param board_height: The height of the game board
        :type board_height: int
        :return: Whether the snake is dead
        :rtype: bool
        """
        coord_set = set()  # Stores all the coordinates that the snake occupies
        for x in self.coordinate_list:
            # Check if the snake is self-intersecting or hit a boundary
            if tuple(x) in coord_set or x[0] < 0 or x[0] > board_width - 1 or x[1] < 0 or x[1] > \
                    board_height - 1:
                return True
            coord_set.add(tuple(x))
        return False


class Food(Drawable):
    """Class representing food for the snake to eat."""
    def __init__(self, coordinates, color):
        """Constructor for the Food class.
        :param coordinates: The coordinates of the food on the game board
        :type coordinates: list
        :param color: The color of the food
        :type color: tuple
        """
        super().__init__(coordinates, [color])

    def reposition(self, x, y):
        """Places the food at another place on the game board, once eaten.
        :param x: The x-coordinate of the food
        :type x: int
        :param y: The y-coordinate of the food
        :type y: int
        """
        self.coordinate_list = [[x, y]]


def get_new_food_coordinates(board_object, snake_object):
    """Generates a random place for the food on the game board that the snake doesn't occupy.
    :param board_object: The board on which the food will be positioned
    :param snake_object: The Snake in the game, so the food won't coincide with it
    """
    board_array = []
    # Can't place food at a boundary or else they will immediately die if travelling in the boundary's direction.
    for x in range(2, board_object.get_dimensions()[0] - 2):
        for y in range(2, board_object.get_dimensions()[1] - 2):
            board_array.append([x, y])
    board_array = [x for x in board_array if x not in snake_object.get_coordinate_list()]
    return random.choice(board_array)


def get_dimensions_from_user():
    """Determines the size of the game board by asking the user."""
    dimensions = []
    print('What size do you want the game to be? Width,height')
    response = str(input())
    response_list = response.split(',')
    for i in response_list:
        try:
            if int(i) < 0:
                raise Exception()
            dimensions.append(int(i))
        except:
            print('Invalid dimensions, please enter again')
            get_dimensions_from_user()
    return dimensions


def end_game_if_snake_died(snake_object, board_object):
    """Ends the game if the snake is dead.
    :param board_object: The board on which the food will be positioned
    :type board_object: Board
    :param snake_object: The Snake in the game, so the food won't coincide with it
    :type snake_object: Snake
    """
    is_dead = snake_object.is_dead(board_object.width, board_object.height)
    if is_dead:
        time.sleep(1)
        sys.exit()


class Game:
    """Class representing the state of all game objects."""
    def __init__(self):
        """Constructor for the Game class."""
        self.game_size = get_dimensions_from_user()
        self.board = Board(self.game_size[0], self.game_size[1])
        self.snake = Snake([[3, 5], [4, 5]], (0, 0, 255), (255, 255, 0))
        self.food = Food([[7, 5]], (255, 0, 0))
        self.direction = 'right'

    def get_player_direction(self):
        """Determines the direction of the snake."""
        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction = 'down'
            elif keys[pygame.K_LEFT]:
                self.direction = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction = 'right'
            return self.direction

    def run(self):
        """Handles the game loop/runtime."""
        win = pygame.display.set_mode(get_dimensions(self.board))
        self.board.draw(win)
        pygame.display.set_caption('Snake')
        pygame.display.update()
        
        game_loop_time_interval = 0.11 # Update window every 0.11 seconds
        
        # Game loop
        while True:
            self.food.draw(win)
            self.snake.draw(win)
            pygame.display.update()  # Update screen at once so the game is fast
            snake_direction = self.get_player_direction()
            snake_collided_with_food = self.snake.collides_with_coordinates(self.food.get_coordinate_list()[0])
            
            # Grow the snake if it ate
            if snake_collided_with_food:
                self.snake.grow(self.food.get_coordinate_list()[0], snake_direction)
                food_coordinates = get_new_food_coordinates(self.board, self.snake)
                self.food.reposition(food_coordinates[0],
                                     food_coordinates[1])
                                     
            self.snake.move(snake_direction)
            end_game_if_snake_died(self.snake, self.board) # Terminate game if snake died
            time.sleep(game_loop_time_interval) 
            self.board.draw(win)


class Board(Drawable):
    """Class representing the board on which the game is played."""
    def __init__(self, width, height):
        """Constructor for the Board class.
        :param width: The width of the game board
        :type width: int
        :param height: The height of the game board
        :type height: int
        """
        coordinate_list = []   # The coordinates of all spots/squares on the game board
        for i in range(height):
            for j in range(width):
                coordinate_list.append([j, i])
        color_list = []
        
        lighter_green = (0, 255, 0)
        darker_green = (0, 224, 0)
        
        # Create a checkerboard pattern to show the squares of the game board
        for i in range(height):
            for j in range(width):
                if (i + j) % 2 == 0:
                    color_list.append(lighter_green)
                else:
                    color_list.append(darker_green)
                    
        super().__init__(coordinate_list, color_list)
        self.width = width  # Width of the game board
        self.height = height  # Height of the game board

    def get_dimensions(self):
        return [self.width, self.height]


def get_dimensions(board_object):
    """Converts the coordinates of points on the game board to dimensions (in pixels) of an object on the board."""
    size = board_object.get_dimensions()
    square_side = 25
    dimensions = (square_side * size[0], square_side * size[1])
    return dimensions


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
