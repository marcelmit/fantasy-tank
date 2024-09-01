import math
import random

import pygame

from helper_functions import load_image, load_sprite_sheet
from ui_elements import UI

class Wizard(pygame.sprite.Sprite):
    def __init__(self, game, screen_size, player_position):
        super().__init__()
        self.game = game
        self.screen_size = screen_size
        self.player_position = player_position

        self.image = load_sprite_sheet("enemies/wizard_idle", frame=0, width=40, height=60, scale=3, resolution=UI.resolution, colour=(0, 0, 0))
        self.rect = self.image.get_rect(centerx = self.screen_size[0] // 2)

        # Wizard stats
        self.max_health = 1000
        self.health = 100

        # Fire ball
        self.fire_ball_group = pygame.sprite.Group()
        self.fire_ball_interval = 255

        # Fire wall
        self.fire_wall_group = pygame.sprite.Group()
        self.fire_wall_interval = 1
        self.fire_wall_last_shot_time = 0
        self.fire_wall_count = 0
        self.max_fire_wall_count = 3

        # Sprite animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.animation_steps = 8

    def combat_logic(self):
        current_time = pygame.time.get_ticks() / 1000

        # Fire ball
        if current_time >= self.fire_ball_interval:
            fire_ball = FireBall((self.rect.centerx - 30 * UI.resolution, self.rect.centery - 35 * UI.resolution), self.player_position.rect.center)
            self.fire_ball_group.add(fire_ball)
            self.fire_ball_interval = current_time + 2

        # Fire wall
        if current_time >= self.fire_wall_interval and self.fire_wall_count < self.max_fire_wall_count and current_time >= self.fire_wall_last_shot_time + 2:
            self.cooldown = 500
            fire_wall = FireWall()
            self.fire_wall_group.add(fire_wall)
            self.fire_wall_count += 1
            self.fire_wall_last_shot_time = current_time
        elif self.fire_wall_count >= self.max_fire_wall_count and current_time >= self.fire_wall_last_shot_time:
            self.fire_wall_count = 0
            self.fire_wall_interval = current_time + 15
            self.cooldown = current_time + 4

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            pygame.mixer.music.unload()
            self.kill()
            self.game.game_state = "victory"

    def animate_sprite(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame += 1

            if self.animation_frame >= self.animation_steps:
                self.animation_frame = 0

            self.image = load_sprite_sheet("enemies/wizard_idle", frame=self.animation_frame, width=40, height=60, scale=3, resolution=UI.resolution, colour=(0, 0, 0))

    def update(self):
        self.combat_logic()
        self.animate_sprite()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class FireBall(pygame.sprite.Sprite):
    def __init__(self, enemy_position, player_position):
        super().__init__()
        self.fire_ball_velocity = 7 * UI.resolution

        # Calculate the players position
        direction_vector = pygame.math.Vector2(player_position) - pygame.math.Vector2(enemy_position)
        self.direction = direction_vector.normalize()

        # Rotate the image based on the shooting direction.
        angle = math.degrees(math.atan2(- self.direction.y, self.direction.x)) + 90
        self.original_image = load_image("enemies/fire_ball")
        self.rescaled_image = pygame.transform.scale(self.original_image, (64 * UI.resolution, 64 * UI.resolution))
        self.image = pygame.transform.rotate(self.rescaled_image, angle)
        self.rect = self.image.get_rect(center = enemy_position)

    def update(self):
        self.rect.center += self.direction * self.fire_ball_velocity
        if (self.rect.x < - 100 or self.rect.x > UI.screen_size[0] + 100 or
            self.rect.y < - 100 or self.rect.y > UI.screen_size[1] + 100):
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class FireWall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.group = pygame.sprite.Group()
        self.wall_elements = []

        self.wall_element_width = 79 * UI.resolution
        self.fire_wall_velocity = 6 * UI.resolution

        # Create random gaps towards the center of the wall.
        empty_gaps_list = list(range(5, 20))
        empty_gaps = random.sample(empty_gaps_list, k=4)

        for i in range(25):
            if i in empty_gaps:
                continue
            else:
                wall_element = pygame.sprite.Sprite()
                wall_element.image = load_image("enemies/fire_wall")
                wall_element.rect = wall_element.image.get_rect(topleft = (0 + i * self.wall_element_width, 0))

                self.wall_elements.append((wall_element.image, wall_element.rect))
                self.group.add(wall_element)

    def update(self):
        for _, wall_element_rect in self.wall_elements:
            wall_element_rect.y += self.fire_wall_velocity

        if wall_element_rect.y < - 100 or wall_element_rect.y > UI.screen_size[1] + 100:
            self.kill()
        
    def draw(self, surface):
        for wall_element_image, wall_element_rect in self.wall_elements:
            surface.blit(wall_element_image, wall_element_rect)