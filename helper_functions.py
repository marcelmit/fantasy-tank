import os

import pygame
from pygame.locals import *

BASE_IMAGE_PATH = "assets/images/"
BASE_SOUND_PATH = "assets/sounds/effects/"
BASE_MUSIC_PATH = "assets/sounds/music/"

def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True  

def mouse_input(game):
    mouse_input = pygame.mouse.get_pressed()
    current_time = pygame.time.get_ticks() / 1000

    if mouse_input[0] and current_time > game.mouse_clicked_time:
        game.mouse_clicked_time = current_time + 0.3
        return True
    return False

def keyboard_input(game):
    pressed_key = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks() / 1000

    # Options
    if pressed_key[K_ESCAPE] and current_time > game.key_pressed_time + 0.3:
        if game.state == "battle" and not game.paused:
            game.pause_start_time = pygame.time.get_ticks() / 1000
            game.state = "battle_options"
        elif game.state == "battle_options":
            game.pause_end_time = pygame.time.get_ticks() / 1000
            game.pause_duration += (game.pause_end_time - game.pause_start_time)
            game.state = "battle"
        elif game.state == "menu":
            game.state = "options"
        elif game.state == "options":
            game.state = "menu"
        game.key_pressed_time = pygame.time.get_ticks() / 1000

    # Pause
    if pressed_key[K_p] and current_time > game.key_pressed_time + 0.3 and game.state == "battle":
        if not game.paused:
            game.pause_start_time = pygame.time.get_ticks() / 1000
        else:
            game.pause_end_time = pygame.time.get_ticks() / 1000
            game.pause_duration += (game.pause_end_time - game.pause_start_time)
        game.key_pressed_time = pygame.time.get_ticks() / 1000
        game.paused = not game.paused

def set_resolution(game, resolution):
        resolutions = {
            "1920x1080": 1.0,
            "1600x900": 0.84,
            "1280x720": 0.67,
            "960x540": 0.5
        }

        game.resolution = resolutions[resolution]
        width, height = map(int, resolution.split("x"))
        game.screen = pygame.display.set_mode((width, height))
        game.screen_size = game.screen.get_size()
        game.font = pygame.font.SysFont("cambria", int(40 * game.resolution))

def add_data(self, data):
        if data in self.data_dict:
            self.data_dict[data] += 1
        else:
            self.data_dict[data] = 1

def calculate_score(score_timer, data):
    score_timer = int(score_timer * 0.5)
    score = 0

    for k, v in data.items():
        if k == "fire_ball":
            score -= v * 5
        elif k == "fire_wall":
            score -= v * 10
        elif k == "fire_rain":
            score -= v * 3
        elif k == "cannon_hit":
            score += v * 10
        elif k == "rocket_hit":
            score += v * 20
        elif k == "cannon_miss":
            score -= v * 1
        elif k == "rocket_miss":
            score -= v * 10
    return int(score - score_timer)

def load_image(path):
    image = pygame.image.load(os.path.join(BASE_IMAGE_PATH + path + ".png")).convert_alpha()
    return image

def load_sound(path):
    sound = pygame.mixer.Sound(os.path.join(BASE_SOUND_PATH + path + ".wav"))
    return sound

def load_music(path):
    music = pygame.mixer.music.load(os.path.join(BASE_MUSIC_PATH + path + ".wav"))
    return music

def load_sprite_sheet(path, frame, width, height, scale, resolution, colour):
    original_image = pygame.image.load(os.path.join(BASE_IMAGE_PATH + path + ".png")).convert_alpha()
    frame_image = pygame.Surface((width, height)).convert_alpha()
    frame_image.blit(original_image, (0, 0), ((frame * width), 0, width, height))
    scaled_image = pygame.transform.scale(frame_image, (width * scale * resolution, height * scale * resolution))
    scaled_image.set_colorkey(colour)
    return scaled_image