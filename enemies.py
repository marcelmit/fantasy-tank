import math
import random

import pygame

from helper_functions import load_image, load_sprite_sheet

class Wizard(pygame.sprite.Sprite):
    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.player = player

        self.image = load_sprite_sheet("enemies/wizard_idle", frame=0, width=40, height=60, scale=3, resolution=self.game.resolution, colour=(0, 0, 0))
        self.rect = self.image.get_rect(centerx = self.game.screen_size[0] // 2)

        self.global_cooldown = 0

        # Wizard stats
        self.max_health = 1000
        self.health = 1000

        # Fire ball
        self.fire_ball_group = pygame.sprite.Group()
        self.fire_ball_interval = 2
        self.fire_ball_last_used = 0

        # Fire wall
        self.fire_wall_group = pygame.sprite.Group()
        self.fire_wall_interval = 12
        self.fire_wall_last_used = 0
        self.fire_wall_count = 0
        self.max_fire_wall_count = 3

        # Fire rain
        self.fire_rain_group = pygame.sprite.Group()
        self.fire_rain_interval = 22
        self.fire_rain_last_used = 0
        self.fire_rain_clear = float("inf")
        self.fire_rain_last_clear = float("inf")
        self.fire_rain_collision_tiles = float("inf")

        # Fire beam
        self.fire_beam_group = pygame.sprite.Group()
        self.fire_patch_group = pygame.sprite.Group()
        self.fire_beam_interval = 35
        self.fire_beam_last_used = 0
        self.fire_beam_duration = 10

        # Sprite animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.animation_steps = 8

    def combat_logic(self):
        # Fire ball
        if self.game.time >= self.global_cooldown and self.game.time > self.fire_ball_interval + self.fire_ball_last_used:
            fire_ball = FireBall(self.game, self, self.player)
            self.fire_ball_group.add(fire_ball)
            self.fire_ball_last_used = self.game.time

        # Fire wall
        if self.game.time >= self.fire_wall_interval + self.fire_wall_last_used and self.fire_wall_count < self.max_fire_wall_count:
            self.global_cooldown = float("inf")
            self.fire_wall_interval = 0
            fire_wall = FireWall(self.game, self)
            self.fire_wall_group.add(fire_wall)
            self.fire_wall_count += 1
            self.fire_wall_last_used = self.game.time + 2
        elif self.fire_wall_count >= self.max_fire_wall_count and self.game.time >= self.fire_wall_last_used:
            self.fire_wall_count = 0
            self.fire_wall_interval = 10
            self.fire_wall_last_used = self.game.time
            self.global_cooldown = self.game.time + 1

        # Fire rain
        fire_rain_spawner = FireRainSpawner(self.game, 79, self.fire_rain_group)
        if self.game.time >= self.global_cooldown and self.game.time >= self.fire_rain_interval + self.fire_rain_last_used:
            # Fire wall cooldown if needed to not overlap.
            if self.fire_wall_last_used - 5 <= self.game.time:
                self.fire_wall_last_used += 5
            self.global_cooldown = float("inf")
            fire_rain_spawner.fire_rain_tiles(has_collision=False)
            self.fire_rain_clear = self.game.time + 2 if self.health < 500 else self.game.time + 3
        elif self.game.time >= self.fire_rain_clear:
            self.fire_rain_group.empty()
            self.fire_rain_clear = float("inf")
            self.fire_rain_collision_tiles = 0
        elif self.game.time >= self.fire_rain_collision_tiles:
            self.fire_rain_collision_tiles = float("inf")
            fire_rain_spawner.fire_rain_tiles(has_collision=True)
            self.fire_rain_last_clear = self.game.time + 1.5
        elif self.game.time >= self.fire_rain_last_clear:
            self.fire_rain_group.empty()
            self.fire_rain_last_clear = float("inf")
            self.fire_rain_last_used = self.game.time
            self.global_cooldown = self.game.time + 1

        #Fire beam
        if self.game.time >= self.global_cooldown and self.game.time >= self.fire_beam_interval + self.fire_beam_last_used:
            # Fire wall cooldown if needed to not overlap.
            if self.fire_wall_last_used - 10 <= self.game.time:
                self.fire_wall_last_used += 10
            fire_beam = FireBeam(self.game, self, self.player, self.fire_patch_group)
            self.fire_beam_group.add(fire_beam)
            self.global_cooldown = float("inf")
            self.fire_beam_duration = self.game.time + 10
        elif self.game.time >= self.fire_beam_duration:
            self.fire_beam_group.empty()
            self.fire_patch_group.empty()
            self.fire_beam_duration = float("inf")
            self.fire_beam_last_used = self.game.time
            self.global_cooldown = self.game.time + 1

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            pygame.mixer.music.unload()
            self.kill()
            self.game.state = "victory"

    def animate_sprite(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame += 1

            if self.animation_frame >= self.animation_steps:
                self.animation_frame = 0

            self.image = load_sprite_sheet("enemies/wizard_idle", frame=self.animation_frame, width=40, height=60, scale=3, resolution=self.game.resolution, colour=(0, 0, 0))

    def update(self):
        self.combat_logic()
        self.animate_sprite()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class FireBall(pygame.sprite.Sprite):
    def __init__(self, game, enemy, player):
        super().__init__()
        self.game = game
        self.enemy = enemy
        self.player = player

        self.velocity = 7 * self.game.resolution
        self.size = (100 * self.game.resolution, 120 * self.game.resolution) if self.enemy.health < 500 else (50 * self.game.resolution, 60 * self.game.resolution)

        # Calculate the players position
        self.enemy_pos = pygame.math.Vector2(self.enemy.rect.centerx - 30 * self.game.resolution, self.enemy.rect.centery - 35 * self.game.resolution)
        self.direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.enemy_pos)
        self.direction = self.direction.normalize()

        # Rotate the image based on the shooting direction.
        self.angle = math.degrees(math.atan2(- self.direction.y, self.direction.x)) + 90
        self.original_image = load_image("enemies/fire_ball")
        self.rescaled_image = pygame.transform.scale(self.original_image, self.size)
        self.image = pygame.transform.rotate(self.rescaled_image, self.angle)
        self.rect = self.image.get_rect(center = self.enemy_pos)

    def update(self):
        self.enemy_pos += self.direction * int(self.velocity)
        self.rect.center = self.enemy_pos

        if (self.rect.x < - 100 or self.rect.x > self.game.screen_size[0] + 100 or
            self.rect.y < - 100 or self.rect.y > self.game.screen_size[1] + 100):
            self.kill()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class FireWall(pygame.sprite.Sprite):
    def __init__(self, game, enemy):
        super().__init__()
        self.game = game
        self.enemy = enemy

        self.fire_wall_elements = []
        self.group = pygame.sprite.Group()

        self.size = (40 * self.game.resolution, 70 * self.game.resolution)
        self.velocity = 6.8 * self.game.resolution if self.enemy.health < 500 else 5 * self.game.resolution
        self.fire_wall_gap_width = 82 * self.game.resolution

        # Create random gaps towards the center of the wall.
        empty_gaps_list = list(range(5 , 20))
        empty_gaps = random.sample(empty_gaps_list, k=4)

        for i in range(25):
            if i in empty_gaps:
                continue
            else:
                fire_wall_element = pygame.sprite.Sprite()
                fire_wall_element.original_image = load_image("enemies/fire_wall")
                fire_wall_element.image = pygame.transform.scale(fire_wall_element.original_image, self.size)
                fire_wall_element.rect = fire_wall_element.image.get_rect(topleft = (0 + i * self.fire_wall_gap_width, 0))

                self.fire_wall_elements.append((fire_wall_element.image, fire_wall_element.rect))
                self.group.add(fire_wall_element)

    def update(self):
        for _, fire_wall_element_rect in self.fire_wall_elements:
            fire_wall_element_rect.y += self.velocity
            if fire_wall_element_rect.y > self.game.screen_size[1] + 100:
                self.kill()
        
    def draw(self):
        for fire_wall_element_image, fire_wall_element_rect in self.fire_wall_elements:
            self.game.screen.blit(fire_wall_element_image, fire_wall_element_rect)

class FireRain(pygame.sprite.Sprite):
    def __init__(self, game, pos, image, has_collision=False):
        super().__init__()
        self.game = game
        self.has_collision = has_collision

        self.original_image = load_image(image)
        self.image = self.original_image
        self.rect = self.original_image.get_rect(center = pos)

        self.size = 0
        self.rotation = 0
        self.rotation_speed = 2

    def update(self):
        if self.has_collision:
            self.size += 0.011
            width, height = (64 * self.game.resolution) * self.size, (64 * self.game.resolution) * self.size
            self.image = pygame.transform.scale(self.original_image, (width, height))
            self.rect = self.image.get_rect(center = self.rect.center)
        else:
            self.rotation = (self.rotation - self.rotation_speed) % 360
            self.scaled_image = pygame.transform.scale(self.original_image, (54 * self.game.resolution, 54 * self.game.resolution))
            self.image = pygame.transform.rotate(self.scaled_image, self.rotation)
            self.rect = self.image.get_rect(center = self.rect.center)

class FireRainSpawner:
    def __init__(self, game, count, fire_rain_group):
        self.game = game
        self.count = count
        self.fire_rain_group = fire_rain_group

    def fire_rain_tiles(self, has_collision=False):
        no_collision_image_path = ("enemies/fire_rain_1")
        collision_image_path = ("enemies/fire_rain_2")

        step = 200 * self.game.resolution
        x_pos, y_pos = 60 * self.game.resolution, 290 * self.game.resolution
        reset_x_pos = False

        for i in range(self.count):
            position = (x_pos, y_pos)
            x_pos += step

            if x_pos >= 2000 * self.game.resolution:
                if reset_x_pos:
                    x_pos = 60 * self.game.resolution
                    reset_x_pos = False
                else:
                    x_pos = 160 * self.game.resolution
                    reset_x_pos = True
                y_pos += 100 * self.game.resolution

            if has_collision:
                fire_rain = FireRain(self.game, position, collision_image_path, has_collision=True)
                self.fire_rain_group.add(fire_rain)
            else:
                fire_rain = FireRain(self.game, position, no_collision_image_path)
                self.fire_rain_group.add(fire_rain)

class FireBeam(pygame.sprite.Sprite):
    def __init__(self, game, enemy, player, fire_patch_group):
        super().__init__()
        self.game = game
        self.enemy = enemy
        self.player = player
        self.fire_patch_group = fire_patch_group

        self.velocity = 6 * self.game.resolution if self.enemy.health < 500 else 4.5 * game.resolution

        self.fire_patch_spawner = FirePatchSpawner(self.game, self.fire_patch_group)
        self.enemy_pos = pygame.math.Vector2(self.enemy.rect.centerx - 30 * self.game.resolution, self.enemy.rect.centery - 35 * self.game.resolution)

        self.original_image = load_image("enemies/fire_beam")
        self.image = pygame.transform.scale(self.original_image, (120 * self.game.resolution, 120 * self.game.resolution))
        self.rect = self.image.get_rect(center = self.enemy_pos)

    def update(self):
        self.fire_patch_spawner.generate_fire_patch(self.rect.center)

        player_pos = pygame.math.Vector2(self.player.rect.center)
        direction = player_pos - self.enemy_pos
        direction = direction.normalize()

        self.enemy_pos += direction * int(self.velocity)
        self.rect.center = self.enemy_pos

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class FirePatch(pygame.sprite.Sprite):
    def __init__(self, game, fire_beam_pos):
        super().__init__()
        self.game = game
        self.fire_beam_pos = fire_beam_pos

        self.original_image = load_image("enemies/fire_patch")
        self.scaled_image = pygame.transform.scale(self.original_image, (120 * self.game.resolution, 120 * self.game.resolution))
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = fire_beam_pos)

        self.rotation = 0
        self.rotation_speed = 2

    def update(self):
        self.rotation = (self.rotation - self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.scaled_image, self.rotation)
        self.rect = self.image.get_rect(center = self.fire_beam_pos)

        if self.rect.top < 140 * self.game.resolution:
            self.kill()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class FirePatchSpawner:
    def __init__(self, game, fire_patch_group):
        self.game = game
        self.fire_patch_group = fire_patch_group

        self.last_fire_patch = 0
        self.fire_patch_cooldown = 0.6

    def generate_fire_patch(self, fire_beam_pos):
        current_time = pygame.time.get_ticks() / 1000

        if current_time - self.last_fire_patch > self.fire_patch_cooldown:
            fire_patch = FirePatch(self.game, fire_beam_pos)
            self.fire_patch_group.add(fire_patch)
            self.last_fire_patch = current_time