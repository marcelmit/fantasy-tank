import pygame
from pygame.locals import *

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.events = []

        self.pause_timer = 0

    def update(self):
        self.events = pygame.event.get()
        self.pause()
    
    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False
    
    def pause(self):
        current_time = pygame.time.get_ticks() / 1000
        pressed_key = pygame.key.get_pressed()

        if pressed_key[K_ESCAPE] and self.pause_timer < current_time and self.game.game_state == "battle":
            self.game.game_state = "battle_options"
            self.pause_timer = current_time + 0.3
        elif pressed_key[K_ESCAPE] and self.pause_timer < current_time and self.game.game_state == "battle_options":
            self.game.game_state = "battle"
            self.pause_timer = current_time + 0.3