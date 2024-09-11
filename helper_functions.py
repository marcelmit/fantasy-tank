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

def mouse_input():
    global cooldown
    current_time = pygame.time.get_ticks() / 1000
    mouse_input = pygame.mouse.get_pressed()

    if mouse_input[0] and current_time > cooldown:
        cooldown = current_time + 0.3
        return True
    return False

def keyboard_input(game):
    global cooldown
    current_time = pygame.time.get_ticks() / 1000
    pressed_key = pygame.key.get_pressed()

    # Options
    if pressed_key[K_ESCAPE] and cooldown < current_time and not game.paused:
        if game.state == "battle":
            game.state = "battle_options"
            cooldown = current_time + 0.3
        elif game.state == "battle_options":
            game.state = "battle"
            cooldown = current_time + 0.3
        elif game.state == "menu":
            game.state = "options"
            cooldown = current_time + 0.3
        elif game.state == "options":
            game.state = "menu"
            cooldown = current_time + 0.3

    # Pause
    if pressed_key[K_p] and cooldown < current_time and game.state == "battle":
        cooldown = current_time + 0.3
        game.paused = not game.paused

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