import math

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
        self.fire_ball_interval = 2

        # Sprite animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.animation_steps = 8

    def combat_logic(self):
        current_time = pygame.time.get_ticks() / 1000

        # Fire ball
        if current_time >= self.fire_ball_interval:
            fire_ball = FireBall(self.rect.center, self.player_position.rect.center)
            self.fire_ball_group.add(fire_ball)
            self.fire_ball_interval = current_time + 2

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
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x)) + 90
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