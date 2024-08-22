import pygame
from pygame.locals import *

from helper_functions import load_image

class PlayerTank:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.original_image = load_image("player/player_tank")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))

        # Player stats
        self.velocity = 10

    def move(self):
        pressed_key = pygame.key.get_pressed()
        x_pos, y_pos = 0, 0

        # Changes x and y positions based on which key is pressed.
        if pressed_key[K_LEFT] or pressed_key[K_a]:
            x_pos -= self.velocity
        if pressed_key[K_RIGHT] or pressed_key[K_d]:
            x_pos += self.velocity
        if pressed_key[K_UP] or pressed_key[K_w]:
            y_pos -= self.velocity
        if pressed_key[K_DOWN] or pressed_key[K_s]:
            y_pos += self.velocity

        self.rect.move_ip(x_pos, y_pos)

        # Stops the player from moving off-screen.
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.screen_size[0]:
            self.rect.right = self.screen_size[0] - 10.5
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]

        # Rotate sprite image based on movement direction
        if x_pos == 0 and y_pos < 0:
            self.image = self.original_image
        elif x_pos == 0 and y_pos > 0:
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif x_pos < 0 and y_pos == 0:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif x_pos > 0 and y_pos == 0:
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif x_pos < 0 and y_pos < 0:
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif x_pos < 0 and y_pos > 0:
            self.image = pygame.transform.rotate(self.original_image, 135)
        elif x_pos > 0 and y_pos < 0:
            self.image = pygame.transform.rotate(self.original_image, -45)
        elif x_pos > 0 and y_pos > 0:
            self.image = pygame.transform.rotate(self.original_image, -135)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.move()