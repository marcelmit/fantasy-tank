import random

import pygame
from pygame.locals import *

from helper_functions import load_image, load_sound, add_data

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.original_image = load_image("player/player_tank")
        self.scaled_image = pygame.transform.scale(self.original_image, (62 * self.game.resolution, 76 * self.game.resolution))
        self.image = self.scaled_image
        self.rect = self.scaled_image.get_rect(center = (self.game.screen_size[0] // 2, self.game.screen_size[1] // 2))

        self.direction = "up"

        # Player stats
        self.max_health = 200
        self.health = 200
        self.velocity = 9 * self.game.resolution
        self.max_rocket_ammo = 20
        self.rocket_ammo = 5

        # Player invulnerability duration after taking damage.
        self.invulnerability_duration = 1
        self.last_hit_time = 0

        # Cooldown for the shoot method.
        self.projectile_group = pygame.sprite.Group()
        self.last_shot_time = 0
        self.shoot_delay = 0.5

        # Air drops
        self.air_drop_group = pygame.sprite.Group()
        self.crate_group = pygame.sprite.Group()
        self.air_drop_interval = 15
        self.last_air_drop = 0

    def movement(self):
        pressed_key = pygame.key.get_pressed()
        x_pos, y_pos = 0, 0

        # Changes x and y positions based on which key is pressed.
        if pressed_key[K_UP] or pressed_key[K_w]:
            y_pos -= self.velocity
        if pressed_key[K_DOWN] or pressed_key[K_s]:
            y_pos += self.velocity
        if pressed_key[K_LEFT] or pressed_key[K_a]:
            x_pos -= self.velocity
        if pressed_key[K_RIGHT] or pressed_key[K_d]:
            x_pos += self.velocity

        self.rect.move_ip(x_pos, y_pos)

        # Stops the player from moving off-screen.
        if self.rect.top <= 215 * self.game.resolution:
            self.rect.top = 215 * self.game.resolution
        elif self.rect.bottom >= self.game.screen_size[1]:
            self.rect.bottom = self.game.screen_size[1]
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.game.screen_size[0]:
            self.rect.right = self.game.screen_size[0] - 10.5 * self.game.resolution

        # Rotate sprite image based on movement direction and updates the direction state.
        if x_pos == 0 and y_pos < 0:
            self.direction = "up"
            self.image = self.scaled_image
        elif x_pos == 0 and y_pos > 0:
            self.direction = "down"
            self.image = pygame.transform.rotate(self.scaled_image, 180)
        elif x_pos < 0 and y_pos == 0:
            self.direction = "left"
            self.image = pygame.transform.rotate(self.scaled_image, 90)
        elif x_pos > 0 and y_pos == 0:
            self.direction = "right"
            self.image = pygame.transform.rotate(self.scaled_image, - 90)
        elif x_pos < 0 and y_pos < 0:
            self.direction = "up_left"
            self.image = pygame.transform.rotate(self.scaled_image, 45)
        elif x_pos > 0 and y_pos < 0:
            self.direction = "up_right"
            self.image = pygame.transform.rotate(self.scaled_image, - 45)
        elif x_pos < 0 and y_pos > 0:
            self.direction = "down_left"
            self.image = pygame.transform.rotate(self.scaled_image, 135)
        elif x_pos > 0 and y_pos > 0:
            self.direction = "down_right"
            self.image = pygame.transform.rotate(self.scaled_image, - 135)

    def shoot(self):
        pressed_keys = pygame.key.get_pressed()
        cannon_sound = load_sound("cannon")
        rocket_sound = load_sound("rocket")
        pygame.mixer.Sound.set_volume(cannon_sound, self.game.sound_volume)
        pygame.mixer.Sound.set_volume(rocket_sound, self.game.sound_volume)

        # Create two cannon projectiles and offset them to fit the dual cannon barrel.
        if pressed_keys[K_SPACE] and self.game.time - self.last_shot_time > self.shoot_delay:
            cannon_sound.play()

            if self.direction == "up":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (8 * self.game.resolution), self.rect.centery - (40 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (8 * self.game.resolution), self.rect.centery - (40 * self.game.resolution), self.direction)
            elif self.direction == "down":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (8 * self.game.resolution), self.rect.centery + (40 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (8 * self.game.resolution), self.rect.centery + (40 * self.game.resolution), self.direction)
            elif self.direction == "left":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (42 * self.game.resolution), self.rect.centery - (10 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (42 * self.game.resolution), self.rect.centery + (6 * self.game.resolution), self.direction)
            elif self.direction == "right":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (42 * self.game.resolution), self.rect.centery - (10 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (42 * self.game.resolution), self.rect.centery + (6 * self.game.resolution), self.direction)
            elif self.direction == "up_left":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (23 * self.game.resolution), self.rect.centery - (15 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (11 * self.game.resolution), self.rect.centery - (25 * self.game.resolution), self.direction)
            elif self.direction == "up_right":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (37 * self.game.resolution), self.rect.centery - (26 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (48 * self.game.resolution), self.rect.centery - (14 * self.game.resolution), self.direction)
            elif self.direction == "down_left":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (11 * self.game.resolution), self.rect.centery + (45 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx - (21 * self.game.resolution), self.rect.centery + (33 * self.game.resolution), self.direction)
            elif self.direction == "down_right":
                left_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (49 * self.game.resolution), self.rect.centery + (35 * self.game.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.game, self.rect.centerx + (39 * self.game.resolution), self.rect.centery + (46 * self.game.resolution), self.direction)

            self.projectile_group.add(left_cannon_projectile, right_cannon_projectile)
            self.last_shot_time = self.game.time

        # Create a rocket projectile and reduce rocket ammo count
        if self.rocket_ammo > 0 and pressed_keys[K_LCTRL] and self.game.time - self.last_shot_time > self.shoot_delay:
            rocket_sound.play()
            self.rocket_ammo -= 1

            if self.direction == "up":
                rocket = PlayerProjectile(self.game, self.rect.centerx, self.rect.centery - (7 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "down":
                rocket = PlayerProjectile(self.game, self.rect.centerx, self.rect.centery + (5 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "left":
                rocket = PlayerProjectile(self.game, self.rect.centerx - (17 * self.game.resolution), self.rect.centery + (8 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "right":
                rocket = PlayerProjectile(self.game, self.rect.centerx, self.rect.centery + (8 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "up_left":
                rocket = PlayerProjectile(self.game, self.rect.centerx - (3 * self.game.resolution), self.rect.centery + (6 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "down_left":
                rocket = PlayerProjectile(self.game, self.rect.centerx - (2 * self.game.resolution), self.rect.centery + (17 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "up_right":
                rocket = PlayerProjectile(self.game, self.rect.centerx + (4 * self.game.resolution), self.rect.centery + (10 * self.game.resolution), self.direction, is_rocket=True)
            elif self.direction == "down_right":
                rocket = PlayerProjectile(self.game, self.rect.centerx + (6 * self.game.resolution), self.rect.centery + (15 * self.game.resolution), self.direction, is_rocket=True)

            self.projectile_group.add(rocket)
            self.last_shot_time = self.game.time

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            pygame.mixer.music.unload()
            self.kill()
            self.game.state = "defeat"
        
    def update(self):
        self.movement()
        self.shoot()

        # Generate air drop
        if self.game.time >= self.air_drop_interval + self.last_air_drop:
            air_drop = AirDropSpawner(self.game, self.crate_group)
            self.air_drop_group.add(air_drop)
            self.last_air_drop = self.game.time

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, game, x_pos, y_pos, direction, is_rocket=False):
        super().__init__()
        self.game = game
        self.direction = direction
        
        self.velocity = 6 * self.game.resolution

        if is_rocket:
            self.original_image = load_image("player/rocket")
            self.scaled_image = pygame.transform.scale(self.original_image, (13 * self.game.resolution, 45 * self.game.resolution))
            self.type = "rocket"
        else:
            self.original_image = load_image("player/cannon")
            self.scaled_image = pygame.transform.scale(self.original_image, (8 * self.game.resolution, 18 * self.game.resolution))
            self.type = "cannon"

        self.image = self.scaled_image
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
          
    def movement(self):
        x_pos, y_pos = 0, 0

        if self.direction == "up":
            y_pos -= self.velocity
        elif self.direction == "down":
            y_pos += self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, 180)
        elif self.direction == "left":
            x_pos -= self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, 90)
        elif self.direction == "right":
            x_pos += self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, - 90)
        elif self.direction == "up_left":
            x_pos, y_pos = - self.velocity, - self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, 45)
        elif self.direction == "up_right":
            x_pos, y_pos = + self.velocity, - self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, - 45)
        elif self.direction == "down_left":
            x_pos, y_pos = - self.velocity, + self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, 135)
        elif self.direction == "down_right":
            x_pos, y_pos = + self.velocity, + self.velocity
            self.image = pygame.transform.rotate(self.scaled_image, - 135)

        self.rect.move_ip(x_pos, y_pos)

        # Removes the projectile if it moves off-screen.
        if (self.rect.x < - 100 or self.rect.x > self.game.screen_size[0] + 100 or 
            self.rect.y < - 100 or self.rect.y > self.game.screen_size[1] + 100):
            self.kill()
            if self.type == "cannon":
                add_data(self.game, "cannon_miss")
            elif self.type == "rocket":
                add_data(self.game, "rocket_miss")

    def update(self):
        self.movement()

class AirDropSpawner(pygame.sprite.Sprite):
    def __init__(self, game, crate_group):
        super().__init__()
        self.game = game
        self.crate_group = crate_group

        self.velocity = 6 * self.game.resolution
        self.size = (150 * self.game.resolution, 150 * self.game.resolution)

        # Randomise position
        x_pos_list = [- 100 * self.game.resolution, self.game.screen_size[0] + 100 * self.game.resolution]
        x_pos = random.choice(x_pos_list)
        y_pos = random.randrange(int(290 * self.game.resolution), int(self.game.screen_size[1] - self.size[0] // 2))
        self.pos = (x_pos, y_pos)
        # Randomise crate drop position
        self.crate_drop_pos = random.randint(100, self.game.screen_size[0] - 100)
        self.crate_dropped = False

        self.direction = "right" if x_pos < 0 else "left"
        self.angle = 0 if x_pos < 0 else 180

        self.original_image = load_image("player/plane")
        self.scaled_image = pygame.transform.scale(self.original_image, self.size)
        self.image = pygame.transform.rotate(self.scaled_image, self.angle)
        self.rect = self.image.get_rect(center = self.pos)

    def generate_air_drop_crate(self):
        if not self.crate_dropped:
            if (self.direction == "right" and self.rect.x >= self.crate_drop_pos or
                self.direction == "left" and self.rect.x <= self.crate_drop_pos):
                air_drop_crate = AirDropCrate(self.game, self.rect.center)
                self.crate_group.add(air_drop_crate)
                self.crate_dropped = True

    def update(self):
        self.generate_air_drop_crate()

        if self.direction == "right":
            self.rect.x += int(self.velocity)
        elif self.direction == "left":
            self.rect.x -= int(self.velocity)

        if self.rect.x < - 300 or self.rect.x > self.game.screen_size[0] + 100:
            self.kill()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class AirDropCrate(pygame.sprite.Sprite):
    def __init__(self, game, plane_pos):
        super().__init__()
        self.game = game

        self.size = (70 * self.game.resolution, 70 * self.game.resolution)

        random_crate_list = ["health", "ammo"]
        self.random_crate = random.choice(random_crate_list)

        if self.random_crate == "health":
            self.original_image = load_image("player/health_crate")
        elif self.random_crate == "ammo":
            self.original_image = load_image("player/ammo_crate")
        self.image = pygame.transform.scale(self.original_image, self.size)
        self.rect = self.image.get_rect(center = plane_pos)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)