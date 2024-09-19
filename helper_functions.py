import os

import pygame
from pygame.locals import *

BASE_IMAGE_PATH = "assets/images/"
BASE_SOUND_PATH = "assets/sounds/effects/"
BASE_MUSIC_PATH = "assets/sounds/music/"

cooldown = 0

def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True  

def mouse_input(game):
    global cooldown
    mouse_input = pygame.mouse.get_pressed()

    if mouse_input[0] and game.time > cooldown:
        cooldown = game.time + 0.3
        return True
    return False

def keyboard_input(game):
    global cooldown
    pressed_key = pygame.key.get_pressed()

    # Options
    if pressed_key[K_ESCAPE] and cooldown < game.time and not game.paused:
        if game.state == "battle":
            game.state = "battle_options"
            cooldown = game.time + 0.3
        elif game.state == "battle_options":
            game.state = "battle"
            cooldown = game.time + 0.3
        elif game.state == "menu":
            game.state = "options"
            cooldown = game.time + 0.3
        elif game.state == "options":
            game.state = "menu"
            cooldown = game.time + 0.3

    # Pause
    if pressed_key[K_p] and cooldown < game.time and game.state == "battle":
        cooldown = game.time + 0.3
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