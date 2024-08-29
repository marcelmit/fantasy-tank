import pygame
from pygame.locals import *

class EventHandler:
    def __init__(self):
        self.events = []

    def update(self):
        self.events = pygame.event.get()
    
    def quit(self):
        pressed_key = pygame.key.get_pressed()

        for event in self.events:
            if event.type == pygame.QUIT or pressed_key[K_ESCAPE]:
                return True
        return False