import os

import pygame

BASE_IMAGE_PATH = "assets/images/"

def load_image(path):
    image = pygame.image.load(os.path.join(BASE_IMAGE_PATH + path + ".png")).convert_alpha()
    return image