import os

import pygame

BASE_IMAGE_PATH = "assets/images/"
BASE_SOUND_PATH = "assets/sounds/"

def load_image(path):
    image = pygame.image.load(os.path.join(BASE_IMAGE_PATH + path + ".png")).convert_alpha()
    return image

def load_sound(path):
    sound = pygame.mixer.Sound(os.path.join(BASE_SOUND_PATH + path + ".wav"))
    return sound

def load_sprite_sheet(path, frame, width, height, scale, colour):
    original_image = pygame.image.load(os.path.join(BASE_IMAGE_PATH + path + ".png")).convert_alpha()
    frame_image = pygame.Surface((width, height)).convert_alpha()
    frame_image.blit(original_image, (0, 0), ((frame * width), 0, width, height))
    scaled_image = pygame.transform.scale(frame_image, (width * scale, height * scale))
    scaled_image.set_colorkey(colour)
    return scaled_image