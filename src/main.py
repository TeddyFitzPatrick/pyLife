import copy
import random

import pygame
import sys
import button
from pygame.locals import *

## CONSTANTS ##
# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (20, 100, 250)
# Game
clock = pygame.time.Clock()
# Font
DEFAULT_FONT = pygame.font.Font(pygame.font.get_default_font(), 60)
# Screen
WINDOW_SIZE = (1200, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('pyLife')

## GAME VARIABLES ##
TICK_SPEED = 500
SIZE = 10
BLOCK_SIZE = int(800 / SIZE)
tiles = [[0 for _ in range(SIZE)] for _ in range(SIZE)]


def change_selection(selected_button: button, other_buttons: list[button]):
    for other_button in other_buttons:
        other_button.change_text_color(WHITE)
    selected_button.change_text_color(LIGHT_BLUE)


def adjust_cords(x, y):
    global tiles
    # Above check
    x = x % SIZE if x >= SIZE else x
    y = y % SIZE if y >= SIZE else y
    # Below check
    x = x + SIZE if x < 0 else x
    y = y + SIZE if y < 0 else y
    return tiles[x][y]


def get_num_neighbors(x, y):
    global tiles
    num_neighbors = 0
    # Top
    if adjust_cords(x - 1, y - 1):
        num_neighbors += 1
    if adjust_cords(x, y - 1):
        num_neighbors += 1
    if adjust_cords(x + 1, y - 1):
        num_neighbors += 1
    # Sides
    if adjust_cords(x - 1, y):
        num_neighbors += 1
    if adjust_cords(x + 1, y):
        num_neighbors += 1
    # Below
    if adjust_cords(x - 1, y + 1):
        num_neighbors += 1
    if adjust_cords(x, y + 1):
        num_neighbors += 1
    if adjust_cords(x + 1, y + 1):
        num_neighbors += 1
    return num_neighbors


def resize_grid(new_size: int):
    global tiles
    global SIZE
    global BLOCK_SIZE
    SIZE = new_size
    BLOCK_SIZE = int(800 / SIZE)
    tiles = [[0 for _ in range(SIZE)] for _ in range(SIZE)]


def main():
    global TICK_SPEED
    global tiles
    global SIZE
    global BLOCK_SIZE
    generating = False
    generation = 0
    TILE_COLOR = WHITE
    last_gen_time = 0
    # NORMAL + 10 GRID SIZE SETTINGS
    resize_grid(10)
    TICK_SPEED = 500
    # Buttons
    start = button.Button('START', 850, 50, 60)
    # Grid size
    grid_size = button.Button('Grid Size: ', 850, 150, 40)
    size_ten = button.Button('10', 850, 200, 30)
    size_twenty = button.Button('20', 900, 200, 30)
    size_forty = button.Button('40', 950, 200, 30)
    size_eighty = button.Button('80', 1000, 200, 30)
    size_max = button.Button('MAX', 1050, 200, 30)
    size_buttons = [size_ten, size_twenty, size_forty, size_eighty, size_max]
    # Generation Speed
    generation_speed = button.Button('Gen Speed: ', 850, 300, 40)
    slow = button.Button('SLOW', 850, 350, 30)
    normal = button.Button('NORMAL', 850, 390, 30)
    fast = button.Button('FAST', 850, 430, 30)
    speed = button.Button('SPEED', 850, 470, 30)
    speed_buttons = [slow, normal, fast, speed]
    # Configs
    gen_counter = button.Button('0', 850, 125, 60)
    randomize = button.Button('Randomize', 850, 550, 48)
    reset = button.Button('RESET', 850, 700, 60)
    # Color selection
    WHITE_SELECT = pygame.rect.Rect(850, 625, 40, 40)
    BLUE_SELECT = pygame.rect.Rect(900, 625, 40, 40)
    RED_SELECT = pygame.rect.Rect(950, 625, 40, 40)
    # Add all the initial button options
    menu_buttons = [start, grid_size, randomize, generation_speed]
    menu_buttons.extend(size_buttons)
    menu_buttons.extend(speed_buttons)
    # Select initial configs
    change_selection(size_ten, size_buttons)
    change_selection(normal, speed_buttons)

    while True:
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, WHITE_SELECT)
        pygame.draw.rect(screen, LIGHT_BLUE, BLUE_SELECT)
        pygame.draw.rect(screen, RED, RED_SELECT)
        # Draw a grid
        for x in range(0, 800, BLOCK_SIZE):
            for y in range(0, WINDOW_SIZE[0], BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)
        # Event Handler
        for event in pygame.event.get():
            # Quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if WHITE_SELECT.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                TILE_COLOR = WHITE
            elif BLUE_SELECT.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                TILE_COLOR = LIGHT_BLUE
            elif RED_SELECT.collidepoint(pygame.mouse.get_pos()) and event.type == MOUSEBUTTONDOWN:
                TILE_COLOR = RED
            # Button event handler
            if not generating and event.type == MOUSEBUTTONDOWN:
                # Start the simulation
                if start.hovering():
                    generating = True
                    start.update_text('GENERATION ', 48)
                elif randomize.hovering():
                    tiles = [[random.randint(0, 1) for _ in range(len(tiles))] for _ in range(len(tiles))]
                # GRID SIZING
                elif size_ten.hovering():
                    change_selection(size_ten, size_buttons)
                    resize_grid(10)
                elif size_twenty.hovering():
                    change_selection(size_twenty, size_buttons)
                    resize_grid(20)
                elif size_forty.hovering():
                    change_selection(size_forty, size_buttons)
                    resize_grid(40)
                elif size_eighty.hovering():
                    change_selection(size_eighty, size_buttons)
                    resize_grid(80)
                elif size_max.hovering():
                    change_selection(size_max, size_buttons)
                    resize_grid(160)
                # TICK SPEED
                elif slow.hovering():
                    change_selection(slow, speed_buttons)
                    TICK_SPEED = 1000
                elif normal.hovering():
                    change_selection(normal, speed_buttons)
                    TICK_SPEED = 500
                elif fast.hovering():
                    change_selection(fast, speed_buttons)
                    TICK_SPEED = 100
                elif speed.hovering():
                    change_selection(speed, speed_buttons)
                    TICK_SPEED = 10
                # Initial tile selection
                elif not generating and pygame.mouse.get_pos()[0] <= 800:
                    x, y = pygame.mouse.get_pos()
                    x, y = int(x / BLOCK_SIZE), int(y / BLOCK_SIZE)
                    tiles[y][x] = 1 if tiles[y][x] == 0 else 0
            if event.type == MOUSEBUTTONDOWN and reset.hovering():
                # Reset the game
                tiles = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
                main()
                return
        # MENU
        if not generating:
            for option in menu_buttons:
                option.blit(screen)
        else:
            # Generation counter
            start.blit(screen)
            gen_counter.update_text(str(generation), 60)
            gen_counter.blit(screen)
        # Reset button
        reset.blit(screen)
        # Create the next generation and render
        if generating and pygame.time.get_ticks() - last_gen_time >= TICK_SPEED:
            last_gen_time = pygame.time.get_ticks()
            next_tiles = copy.deepcopy(tiles)
            for x in range(len(tiles)):
                for y in range(len(tiles)):
                    neighbors = get_num_neighbors(x, y)
                    # Any live cell with fewer than two live neighbors dies, as if by underpopulation.
                    # Any live cell with two or three live neighbors lives on to the next generation.
                    # Any live cell with more than three live neighbors dies, as if by overpopulation.
                    # ^ Maybe a little too verbose Conway? ^
                    if tiles[x][y] == 1 and (neighbors < 2 or neighbors > 3):
                        next_tiles[x][y] = 0
                    # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
                    elif neighbors == 3:
                        next_tiles[x][y] = 1
            # Replace the last generation's tile scheme with the next generation
            tiles = next_tiles
            # Generation increment
            generation += 1
        # Render the white tiles
        for x in range(len(tiles)):
            for y in range(len(tiles)):
                if tiles[y][x] == 1:
                    pygame.draw.rect(screen, TILE_COLOR,
                                     pygame.rect.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        # Update screen
        pygame.display.flip()
        # 60 FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
