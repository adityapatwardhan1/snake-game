import pygame
import random
import time
import sys

pygame.init()


class Drawable:
    def __init__(self, coordinates, color):
        self.coordinates = coordinates
        self.color = color

    def get_color(self):
        return self.color

    def draw(self, surface_object):
        for x in self.coordinates:
            pygame.draw.rect(surface_object, self.color, (25 * x[0], 25 * x[1], 25, 25))

    def get_coordinates(self):
        return self.coordinates


class Snake(Drawable):
    def __init__(self, coordinates, body_color, head_color):
        super().__init__(coordinates, body_color)
        self.head_color = head_color

    def move(self, direction):
        if direction == 'up':
            next_element = self.coordinates[-1]
            del self.coordinates[0]
            next_element = [next_element[0], next_element[1] - 1]
            self.coordinates.append(next_element)
            return self.coordinates
        elif direction == 'down':
            next_element = self.coordinates[-1]
            del self.coordinates[0]
            next_element = [next_element[0], next_element[1] + 1]
            self.coordinates.append(next_element)
            return self.coordinates
        elif direction == 'left':
            next_element = self.coordinates[-1]
            del self.coordinates[0]
            next_element = [next_element[0] - 1, next_element[1]]
            self.coordinates.append(next_element)
            return self.coordinates
        else:
            next_element = self.coordinates[-1]
            del self.coordinates[0]
            next_element = [next_element[0] + 1, next_element[1]]
            self.coordinates.append(next_element)
            return self.coordinates

    def draw(self, surface_object):
        for x in self.coordinates[:-1]:
            pygame.draw.rect(surface_object, self.color, (25 * x[0], 25 * x[1], 25, 25))
        pygame.draw.rect(surface_object, self.head_color, (25 * self.coordinates[-1][0], 25 * self.coordinates[-1][1], 25, 25))

    def check_food_collision(self, food_object):
        current_coordinates = self.get_coordinates()
        if current_coordinates.count(food_object.get_coordinates()[0]) > 0:
            return True
        return False

    def grow(self, food_object, direction):
        if direction == 'left':
            self.coordinates.append([food_object.get_coordinates()[0][0] - 1, food_object.get_coordinates()[0][1]])

        elif direction == 'right':
            self.coordinates.append([food_object.get_coordinates()[0][0] + 1, food_object.get_coordinates()[0][1]])

        elif direction == 'up':
            self.coordinates.append([food_object.get_coordinates()[0][0], food_object.get_coordinates()[0][1] - 1])

        else:
            self.coordinates.append([food_object.get_coordinates()[0][0], food_object.get_coordinates()[0][1] + 1])

        return self.coordinates

    def check_for_death(self, grid_object):
        coord_set = set()
        for x in self.coordinates:
            if tuple(x) in coord_set or x[0] < 0 or x[0] > grid_object.get_size()[0] - 1 or x[1] < 0 or x[1] > \
                    grid_object.get_size()[1] - 1:
                return True
            coord_set.add(tuple(x))
        return False


class Food(Drawable):
    def __init__(self, coordinates, color):
        super().__init__(coordinates, color)

    def reposition(self, x, y):
        self.coordinates = [[x, y]]


def end_game_if_snake_died(snake_object, grid_object):
    isDead = snake_object.check_for_death(grid_object)
    if isDead:
        time.sleep(2)
        sys.exit()


def give_food_place(grid_object, snake_object):
    grid_array = []
    for x in range(2, grid_object.get_size()[0] - 2):
        for y in range(2, grid_object.get_size()[1] - 2):
            grid_array.append([x, y])
    grid_array = [x for x in grid_array if x not in snake_object.get_coordinates()]
    return random.choice(grid_array)


class Game:
    def __init__(self):
        self.run = True
        self.direc = 'right'

    def get_player_direction(self):
        while self.run:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direc = 'up'
            elif keys[pygame.K_DOWN]:
                self.direc = 'down'
            elif keys[pygame.K_LEFT]:
                self.direc = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direc = 'right'
            return self.direc


def draw_drawable(drawable_object, surface_object):
    drawable_object.draw(surface_object)
    # for x in drawable_object.get_coordinates():
    #     pygame.draw.rect(surface_object, drawable_object.get_color(), (25 * x[0], 25 * x[1], 25, 25))
    pygame.display.update()


class Grid:
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height
        self.color = background_color

    def get_size(self):
        return [self.width, self.height]

    def get_color(self):
        return self.color


def get_dimensional_input():
    dimensions = []
    print('What size do you want the game to be? Width,height')
    response = str(input())
    response_list = response.split(',')
    for i in response_list:
        dimensions.append(int(i))
    return dimensions


def get_dimensions(grid_object):
    size = grid_object.get_size()
    dimensions = (25 * size[0], 25 * size[1])
    return dimensions


if __name__ == '__main__':

    snake_game = Game()
    game_size = get_dimensional_input()
    game_grid = Grid(game_size[0], game_size[1], (0, 255, 0))
    game_snake = Snake([[3, 5], [4, 5]], (0, 0, 255), (255, 255, 0))
    game_food = Food([[7, 5]], (255, 0, 0))
    snake_direction = 'right'
    win = pygame.display.set_mode(get_dimensions(game_grid))
    win.fill(game_grid.get_color())
    pygame.display.set_caption('Snake')
    pygame.display.update()
    time.sleep(2)
    while True:
        draw_drawable(game_food, win)
        draw_drawable(game_snake, win)
        snake_direction = snake_game.get_player_direction()
        snake_collided = game_snake.check_food_collision(game_food)
        if snake_collided:
            game_snake.grow(game_food, snake_direction)
            game_food.reposition(give_food_place(game_grid, game_snake)[0],
                                 give_food_place(game_grid, game_snake)[1])
        game_snake.move(snake_direction)
        end_game_if_snake_died(game_snake, game_grid)
        time.sleep(0.11)
        win.fill(game_grid.get_color())
