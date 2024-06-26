from random import randrange
#import os
import pygame as pg
from mongodb import *

import tkinter as tk
from tkinter import simpledialog

# from mongodb import update_player_score, get_player_data

pg.font.init()

MIN_SIZE = 5
MAX_SIZE = 25
WINDOW = 500

root = tk.Tk()
root.withdraw()

field_size = int(simpledialog.askinteger("Input", f"Set field size (between {MIN_SIZE}x{MIN_SIZE} and {MAX_SIZE}x{MAX_SIZE}):", minvalue=MIN_SIZE, maxvalue=MAX_SIZE))
user_name = simpledialog.askstring("Input", "Your name:")
snake_speed = int(simpledialog.askinteger("Input", "Set snake speed (1-10):", minvalue=1, maxvalue=10))

TILE_SIZE = WINDOW // field_size
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)


def get_random_position():
    global RANGE
    return [randrange(*RANGE), randrange(*RANGE)]


snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
score = 0
record_score = 0

color = (255, 255, 255)
font_size = 24
font = "Alias"


def show_score(font_color, font_style, size):
    global score, record_score, user_name

    player_data = get_player_data(user_name)
    if player_data:
        record_score = player_data.get('record', 0)
    else:
        record_score = 0

    score_font = pg.font.SysFont(font_style, size)
    score_surface = score_font.render(
        user_name + "'s Score : " + str(score) + " / Best score: " + str(record_score),
        True, font_color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)


def lost_score(font_color, font_style, size):
    global user_name, score, record_score, snake, food, segments, length, snake_dir




    if record_score < score:
        record_score = score
        update_player_score(user_name, score)

    lost_font = pg.font.SysFont(font_style, size)
    lost_surface = lost_font.render("You lost. Your score: " + str(score) + "\n" + "Best score: " + str(record_score),
                                    True, font_color)
    lost_rect = lost_surface.get_rect(center=(WINDOW // 2, WINDOW // 2))
    screen.blit(lost_surface, lost_rect)

    pg.display.flip()

    score = 0

    snake.center, food.center = get_random_position(), get_random_position()
    length, snake_dir = 1, (0, 0)
    segments = [snake.copy()]


def game(input_user_name):
    global score, segments, screen, record_score, length, \
        snake, snake_dir, snake_speed, food, font, \
        color, clock, dirs, WINDOW, MAX_SIZE, \
        MIN_SIZE, TILE_SIZE, RANGE, get_random_position

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w and dirs[pg.K_w]:
                    snake_dir = (0, -TILE_SIZE)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_s and dirs[pg.K_s]:
                    snake_dir = (0, TILE_SIZE)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
                if event.key == pg.K_a and dirs[pg.K_a]:
                    snake_dir = (-TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
                if event.key == pg.K_d and dirs[pg.K_d]:
                    snake_dir = (TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
        screen.fill('black')
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            score += 1
        self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
            lost_score(color, font, font_size)
            pg.time.wait(2000)

        pg.draw.rect(screen, 'red', food)
        [pg.draw.rect(screen, 'green', segment) for segment in segments]

        show_score(color, font, font_size)
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
        pg.display.flip()
        clock.tick(snake_speed)


#initialize()
game(user_name)

