from GameKitML.genmanager import Training
from GameKitML.neuralnetwork import NeuralNetwork as nn

import pygame
import random
import sys

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 15

# Window size
frame_size_x = 400
frame_size_y = 400

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()
fps = 60
current_frame = 0
num_rows = frame_size_x // 10
num_column = frame_size_y // 10


def create_grid(snake_body, food_pos):
    grid = []
    unwrapped_grid = []
    for column in range(num_column):
        grid.append([])
        for row in range(num_rows):
            for i, body in enumerate(snake_body):
                if [body[0] // 10, body[1] // 10] == [row, column]:
                    if i == 0:
                        grid[column].append(2)
                        unwrapped_grid.append(2)
                    else:
                        grid[column].append(1)
                        unwrapped_grid.append(1)
                    break
            else:
                if [food_pos[0] // 10, food_pos[1] // 10] == [row, column]:
                    grid[column].append(-1)
                    unwrapped_grid.append(-1)
                else:
                    grid[column].append(0)
                    unwrapped_grid.append(0)
    return grid, unwrapped_grid


class Snake:
    def __init__(self):
        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]

        self.food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.grid_data = create_grid(self.snake_body, self.food_pos)
        self.grid = self.grid_data[0]
        self.unwrapped_grid = self.grid_data[1]
        self.nn_inputs = []

        self.score = 0

        self.direction = 'RIGHT'
        self.direction_value = -1

        self.change_to = self.direction

        # Making sure the snake cannot move in the opposite direction instantaneously

    def update_nn_inputs(self):
        self.nn_inputs = self.grid_data[1]
        self.nn_inputs.insert(0, self.direction_value)

    def update_direction_value(self):
        if self.direction == 'RIGHT':
            self.direction_value = -1
        elif self.direction == 'LEFT':
            self.direction_value = 1
        elif self.direction == 'UP':
            self.direction_value = 2
        elif self.direction == 'DOWN':
            self.direction_value = -2

    def update_grid(self):
        self.grid_data = create_grid(self.snake_body, self.food_pos)
        self.grid = self.grid_data[0]
        self.unwrapped_grid = self.grid_data[1]

    def reset_snake(self):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]

        self.food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.update_grid()

        self.score = 0

        self.direction = 'RIGHT'
        self.change_to = self.direction

    def run_snake(self, input_list):
        global current_frame
        if input_list[0]:
            self.change_to = 'UP'
        elif input_list[1]:
            self.change_to = 'DOWN'
        elif input_list[2]:
            self.change_to = 'LEFT'
        elif input_list[3]:
            self.change_to = 'RIGHT'
        if current_frame % (fps / difficulty) == 0:

            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

                # Moving the snake
            if self.direction == 'UP':
                self.snake_pos[1] -= 10
            if self.direction == 'DOWN':
                self.snake_pos[1] += 10
            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

                # Snake body growing mechanism
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False
            else:
                self.snake_body.pop()

            # Spawning food on the screen
            if not self.food_spawn:
                self.food_pos = [random.randrange(1, (frame_size_x // 10)) * 10,
                                 random.randrange(1, (frame_size_y // 10)) * 10]
            self.food_spawn = True

            # GFX
            game_window.fill(black)
            for pos in self.snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

            # Snake food
            pygame.draw.rect(game_window, white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

            # Game Over conditions
            # Getting out of bounds
            if self.snake_pos[0] < 0 or self.snake_pos[0] > frame_size_x - 10:
                self.game_over()
            if self.snake_pos[1] < 0 or self.snake_pos[1] > frame_size_y - 10:
                self.game_over()
            # Touching the snake body
            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.game_over()
            self.update_nn_inputs()
            self.update_direction_value()
            self.update_grid()
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        current_frame += 1
        fps_controller.tick(fps)

    # Game Over
    def game_over(self):
        self.reset_snake()


snake1 = Snake()

train = Training(Snake, 1)
layers = [len(snake1.nn_inputs), 3, 3, 4]
mutation_rate = 0.2
mutation_change = 0.2
train.initialize_nn(layers, mutation_rate, mutation_change)
# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down

    player_inputs = [pygame.key.get_pressed()[pygame.K_UP], pygame.key.get_pressed()[pygame.K_DOWN],
                     pygame.key.get_pressed()[pygame.K_LEFT], pygame.key.get_pressed()[pygame.K_RIGHT]]
    train.run_agent(nn.Step, snake1.nn_inputs, snake1.run_snake)

