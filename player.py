import pygame
from pygame.locals import *

from helper_functions import load_image, load_sound
from ui_elements import UI

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, game, screen_size):
        super().__init__()
        self.game = game
        self.screen_size = screen_size
        self.direction = "up"

        self.original_image = load_image("player/player_tank")
        self.scaled_image = pygame.transform.scale(self.original_image, (62 * UI.resolution, 76 * UI.resolution))
        self.image = self.scaled_image
        self.rect = self.scaled_image.get_rect(center = (self.screen_size[0] // 2, self.screen_size[1] // 2))

        # Player stats
        self.max_health = 200
        self.health = 150
        self.velocity = 10 * UI.resolution
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
        if self.rect.top <= 215 * UI.resolution:
            self.rect.top = 215 * UI.resolution
        elif self.rect.bottom >= self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.screen_size[0]:
            self.rect.right = self.screen_size[0] - 10.5 * UI.resolution

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
        current_time = pygame.time.get_ticks()

        cannon_sound = load_sound("cannon")
        rocket_sound = load_sound("rocket")
        pygame.mixer.Sound.set_volume(cannon_sound, UI.sound_volume)
        pygame.mixer.Sound.set_volume(rocket_sound, UI.sound_volume)

        # Create two cannon projectiles and offset them to fit the dual cannon barrel.
        if pressed_keys[K_SPACE] and current_time - self.last_shot_time > self.shoot_delay:
            cannon_sound.play()

            if self.direction == "up":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - (8 * UI.resolution), self.rect.centery - (40 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + (8 * UI.resolution), self.rect.centery - (40 * UI.resolution), self.direction)
            elif self.direction == "down":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - (8 * UI.resolution), self.rect.centery + (40 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + (8 * UI.resolution), self.rect.centery + (40 * UI.resolution), self.direction)
            elif self.direction == "left":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - (42 * UI.resolution), self.rect.centery - (10 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx - (42 * UI.resolution), self.rect.centery + (6 * UI.resolution), self.direction)
            elif self.direction == "right":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx + (42 * UI.resolution), self.rect.centery - (10 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + (42 * UI.resolution), self.rect.centery + (6 * UI.resolution), self.direction)
            elif self.direction == "up_left":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - (23 * UI.resolution), self.rect.centery - (15 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx - (11 * UI.resolution), self.rect.centery - (25 * UI.resolution), self.direction)
            elif self.direction == "up_right":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx + (37 * UI.resolution), self.rect.centery - (26 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + (48 * UI.resolution), self.rect.centery - (14 * UI.resolution), self.direction)
            elif self.direction == "down_left":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx - (11 * UI.resolution), self.rect.centery + (45 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx - (21 * UI.resolution), self.rect.centery + (33 * UI.resolution), self.direction)
            elif self.direction == "down_right":
                left_cannon_projectile = PlayerProjectile(self.rect.centerx + (49 * UI.resolution), self.rect.centery + (35 * UI.resolution), self.direction)
                right_cannon_projectile = PlayerProjectile(self.rect.centerx + (39 * UI.resolution), self.rect.centery + (46 * UI.resolution), self.direction)

            self.projectile_group.add(left_cannon_projectile, right_cannon_projectile)
            self.last_shot_time = current_time

        # Create a rocket projectile and reduce rocket ammo count
        if self.rocket_ammo > 0 and pressed_keys[K_LCTRL] and current_time - self.last_shot_time > self.shoot_delay:
            rocket_sound.play()
            self.rocket_ammo -= 1

            if self.direction == "up":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery - (7 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "down":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery + (5 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "left":
                rocket = PlayerProjectile(self.rect.centerx - (17 * UI.resolution), self.rect.centery + (8 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "right":
                rocket = PlayerProjectile(self.rect.centerx, self.rect.centery + (8 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "up_left":
                rocket = PlayerProjectile(self.rect.centerx - (3 * UI.resolution), self.rect.centery + (6 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "down_left":
                rocket = PlayerProjectile(self.rect.centerx - (2 * UI.resolution), self.rect.centery + (17 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "up_right":
                rocket = PlayerProjectile(self.rect.centerx + (4 * UI.resolution), self.rect.centery + (10 * UI.resolution), self.direction, is_rocket=True)
            elif self.direction == "down_right":
                rocket = PlayerProjectile(self.rect.centerx + (6 * UI.resolution), self.rect.centery + (15 * UI.resolution), self.direction, is_rocket=True)

            self.projectile_group.add(rocket)
            self.last_shot_time = current_time

    def decrease_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            pygame.mixer.music.unload()
            self.kill()
            self.game.game_state = "defeat"
        
    def update(self):
        self.movement()
        self.shoot()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, direction, is_rocket=False):
        super().__init__()
        self.direction = direction
        self.velocity = 5 * UI.resolution

        if is_rocket:
            self.original_image = load_image("player/player_tank_rocket")
            self.scaled_image = pygame.transform.scale(self.original_image, (13 * UI.resolution, 45 * UI.resolution))
            self.type = "rocket"
        else:
            self.original_image = load_image("player/player_tank_cannon")
            self.scaled_image = pygame.transform.scale(self.original_image, (8 * UI.resolution, 18 * UI.resolution))
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
        if (self.rect.x < - 100 or self.rect.x > UI.screen_size[0] + 100 or 
            self.rect.y < - 100 or self.rect.y > UI.screen_size[1] + 100):
            self.kill()

    def update(self):
        self.movement()