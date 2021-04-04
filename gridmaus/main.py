'''The game backend.
All addresses, including movement addresses, are tuples.
'''

import math
from random import random, sample


MAX_DIMENSIONS = 5
MIN_DIMENSIONS = 2
MAX_SIZE = 10
MIN_SIZE = 3


class World():
    '''Handles in-game abstractions'''
    def __init__(self, dimensions, size):
        self.dimensions = dimensions
        self.size = size

        dimension_center = int(self.size / 2)
        self.dimension_range = range(dimensions)

        self.goal = self.generate_goal()
        self.player_location = tuple(dimension_center for x in self.dimension_range)

    def generate_goal(self):
        '''Sets the goal at the beginning of the game'''
        return tuple(rand_range(self.size) for x in self.dimension_range)

    def move_address(self, address, movement):
        '''Helper function for World.move_player'''
        return tuple(
                adjust_to_boundaries(address[x] + movement[x], self.size - 1)
                for x in movement
                )

    def move_player(self, movement):
        '''Probably the most important method of the game'''
        self.player_location = self.move_address(self.player_location, movement)


def adjust_to_boundaries(coordinate, boundary):
    '''Keeps the player from leaving the game area'''
    return boundary if coordinate > boundary else 0 if coordinate < 0 else coordinate

def change_world_template(_, value, index):
    '''Called by selector onreturn'''
    world_template[index] = value

def eat_food():
    '''Victory message'''
    with open('foods.txt', 'r') as foods_file:
        foods = [foods_file]
    food = sample(foods, 1)[0]
    food = food.rstrip('\n')
    return f'The mouse finds {food} and scarfs it down. Good job!'

def generate_numerical_selector(min_size, max_size, argument=None):
    '''Helper function for Game.showMenu()'''
    return [(str(x), x, argument) for x in range(min_size, max_size + 1)]

def get_distance(address1, address2):
    '''In Cartesian space using tuples'''
    distances = tuple(abs(address1[x] - address2[x]) for x in range(len(address1)))
    return math.hypot(*distances)

def get_velocity(goal, from_address, to_address):
    '''The player gets a readout of this.'''
    return get_distance(from_address, goal) - get_distance(to_address, goal)

def rand_range(maximum):
    '''Supposed to be faster than randrange'''
    return int(random() * maximum)

def run_game():
    '''The main game loop'''

    def edit_move_template(_, index, value):
        '''Called by show_move_menu()'''
        move_template[index] += value

    game_world = World(world_template['dimensions'], world_template['size'])
    move_template = [0 for x in game_world.dimension_range]
    velocity = 0
    while game_world.player_location != game_world.goal:
        position1 = game_world.player_location
        position2 = game_world.player_location
        velocity = get_velocity(game_world.goal, position1, position2)


world_template = {'dimensions': 2, 'size': 5}
