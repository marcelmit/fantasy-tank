import pygame
from pygame.locals import *

from helper_functions import load_image

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super().__init__()
        self.screen_size = screen_size
        self.direction = "up"

        self.original_image = load_image("player/player_tank")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))

        # Player stats
        self.max_health = 200
        self.health = 100
        self.velocity = 10
        self.rocket_ammo = 5

        # Player invulnerability duration after taking damage.
        self.invulnerability_duration = 2
        self.last_hit_time = 0

        # Cooldown for the shoot method.
        self.projectile_group = pygame.sprite.Group()
        self.last_shot_time = 0
        self.shoot_delay = 500

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
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.screen_size[0]:
            self.rect.right = self.screen_size[0] - 10.5

        # Rotate sprite image based on movement direction and updates the direction state.
        if x_pos == 0 and y_pos < 0:
            self.direction = "up"
            self.image = self.original_image
        elif x_pos == 0 and y_pos > 0:
            self.direction = "down"
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif x_pos < 0 and y_pos == 0:
            self.direction = "left"
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif x_pos > 0 and y_pos == 0:
            self.direction = "right"
            self.image = pygame.transform.rotate(self.original_image, - 90)
        elif x_pos < 0 and y_pos < 0:
            self.direction = "up_left"
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif x_pos > 0 and y_pos < 0:
            self.direction = "up_right"
            self.image = pygame.transform.rotate(self.original_image, - 45)
        elif x_pos < 0 and y_pos > 0:
            self.direction = "down_left"
            self.image = pygame.transform.rotate(self.original_image, 135)
        elif x_pos > 0 and y_pos > 0:
            self.direction = "down_right"
            self.image = pygame.transform.rotate(self.original_image, - 135)

    def shoot(self):
        pressed_keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Create two cannon projectiles and offset them to fit the dual cannon barrel.
        if pressed_keys[K_SPACE] and current_time - self.last_shot_time > self.shoot_delay:
            if self.direction == "up":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - 8, self.rect.centery - 40, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + 8, self.rect.centery - 40, self.direction)
            elif self.direction == "down":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - 8, self.rect.centery + 40, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + 8, self.rect.centery + 40, self.direction)
            elif self.direction == "left":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - 42, self.rect.centery - 10, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx - 42, self.rect.centery + 6, self.direction)
            elif self.direction == "right":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx + 42, self.rect.centery - 10, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + 42, self.rect.centery + 6, self.direction)
            elif self.direction == "up_left":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - 23, self.rect.centery - 15, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx - 11, self.rect.centery - 25, self.direction)
            elif self.direction == "up_right":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx + 37, self.rect.centery - 26, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + 48, self.rect.centery - 14, self.direction)
            elif self.direction == "down_left":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - 11, self.rect.centery + 45, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx - 21, self.rect.centery + 33, self.direction)
            elif self.direction == "down_right":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx + 49, self.rect.centery + 35, self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + 39, self.rect.centery + 46, self.direction)

            self.projectile_group.add(left_cannon_projectile, right_cannon_projectile)
            self.last_shot_time = current_time

        # Create a rocket projectile and reduce rocket ammo count
        if self.rocket_ammo > 0 and pressed_keys[K_LCTRL] and current_time - self.last_shot_time > self.shoot_delay:
            self.rocket_ammo -= 1

            if self.direction == "up":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery - 7, self.direction, is_rocket=True)
            elif self.direction == "down":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery + 5, self.direction, is_rocket=True)
            elif self.direction == "left":
                rocket = PlayerProjectile(self.rect.centerx - 17, self.rect.centery + 8, self.direction, is_rocket=True)
            elif self.direction == "right":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery + 8, self.direction, is_rocket=True)
            elif self.direction == "up_left":
                rocket = PlayerProjectile(self.rect.centerx - 3, self.rect.centery + 6, self.direction, is_rocket=True)
            elif self.direction == "down_left":
                rocket = PlayerProjectile(self.rect.centerx - 2, self.rect.centery + 17, self.direction, is_rocket=True)
            elif self.direction == "up_right":
                rocket = PlayerProjectile(self.rect.centerx + 4, self.rect.centery + 10, self.direction, is_rocket=True)
            elif self.direction == "down_right":
                rocket = PlayerProjectile(self.rect.centerx + 6, self.rect.centery + 15, self.direction, is_rocket=True)

            self.projectile_group.add(rocket)
            self.last_shot_time = current_time

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.movement()
        self.shoot()

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, direction, is_rocket=False):
        super().__init__()
        self.direction = direction
        self.velocity = 5

        if is_rocket:
            self.original_image = load_image("player/player_tank_rocket")
            self.type = "rocket"
        else:
            self.original_image = load_image("player/player_tank_cannon")
            self.type = "cannon"

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
          
    def movement(self):
        x_pos, y_pos = 0, 0

        if self.direction == "up":
            y_pos -= self.velocity
        elif self.direction == "down":
            y_pos += self.velocity
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == "left":
            x_pos -= self.velocity
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == "right":
            x_pos += self.velocity
            self.image = pygame.transform.rotate(self.original_image, - 90)
        elif self.direction == "up_left":
            x_pos, y_pos = - self.velocity, - self.velocity
            self.image = pygame.transform.rotate(self.original_image, 45)
        elif self.direction == "up_right":
            x_pos, y_pos = + self.velocity, - self.velocity
            self.image = pygame.transform.rotate(self.original_image, - 45)
        elif self.direction == "down_left":
            x_pos, y_pos = - self.velocity, + self.velocity
            self.image = pygame.transform.rotate(self.original_image, 135)
        elif self.direction == "down_right":
            x_pos, y_pos = + self.velocity, + self.velocity
            self.image = pygame.transform.rotate(self.original_image, - 135)

        self.rect.move_ip(x_pos, y_pos)

        # Removes the projectile if it moves off-screen.
        if (self.rect.centerx < - 100 or self.rect.centerx > pygame.display.get_surface().get_width() + 100 or 
            self.rect.centery < - 100 or self.rect.centery > pygame.display.get_surface().get_height() + 100):
            self.kill()

    def update(self):
        self.movement()