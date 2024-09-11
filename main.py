import sys

import pygame

from helper_functions import close_game, keyboard_input
from player import PlayerTank
from enemies import Wizard
from ui_elements import UI, MenuManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Fantasy Tank")
        self.screen = pygame.display.set_mode((960, 540))
        self.resolution = 0.5
        #self.screen = pygame.display.set_mode((1920, 1080))
        #self.resolution = 1
        self.screen_size = self.screen.get_size()
        self.sound_volume = 0.5
        self.music_volume = 0.5
        self.clock = pygame.time.Clock()
        self.state = "battle"
        self.paused = False
        UI.init(self)

        self.menu_manager = MenuManager(self)

        self.player = PlayerTank(self, self.screen_size)

        self.enemy_wizard = Wizard(self, self.screen_size, self.player)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy_wizard)

    def set_resolution(self, resolution):
        resolutions = {
            "1920x1080": 1.0,
            "1600x900": 0.84,
            "1280x720": 0.67,
            "960x540": 0.5
        }

        self.resolution = resolutions[resolution]
        width, height = map(int, resolution.split("x"))
        self.screen = pygame.display.set_mode((width, height))
        self.screen_size = self.screen.get_size()
        UI.init(self)

    def collisions(self):
        current_time = pygame.time.get_ticks() / 1000

        # Player projectiles collision
        for projectile in self.player.projectile_group:
            if pygame.sprite.spritecollideany(projectile, self.enemy_group):
                if projectile.type == "cannon":
                    self.enemy_wizard.decrease_health(5)
                elif projectile.type == "rocket":
                    self.enemy_wizard.decrease_health(50)
                projectile.kill()

        # Fire ball collision
        if pygame.sprite.spritecollide(self.player, self.enemy_wizard.fire_ball_group, True):
            if current_time - self.player.last_hit_time > self.player.invulnerability_duration:
                self.player.decrease_health(15)
                self.player.last_hit_time = current_time

        # Fire wall collision
        for fire_wall in self.enemy_wizard.fire_wall_group:
            if pygame.sprite.spritecollideany(self.player, fire_wall.group):
                if current_time - self.player.last_hit_time > self.player.invulnerability_duration:
                    self.player.decrease_health(10)
                    self.player.last_hit_time = current_time

        # Fire rain collision
        for fire_rain in self.enemy_wizard.fire_rain_group:
            if fire_rain.has_collision and pygame.sprite.spritecollide(self.player, self.enemy_wizard.fire_rain_group, True):
                self.player.decrease_health(5)

    def update(self):
        keyboard_input(self)

        if not self.paused:
            self.menu_manager.update()

            if self.state == "battle":
                self.player.update()
                self.player.projectile_group.update()

                self.enemy_wizard.update()
                self.enemy_wizard.fire_ball_group.update()
                self.enemy_wizard.fire_wall_group.update()
                self.enemy_wizard.fire_rain_group.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.menu_manager.draw()

        if self.state == "battle":
            self.player.draw(self.screen)
            self.player.projectile_group.draw(self.screen)

            self.enemy_wizard.draw(self.screen)
            self.enemy_wizard.fire_ball_group.draw(self.screen)
            for fire_wall in self.enemy_wizard.fire_wall_group:
                fire_wall.draw(self.screen)
            self.enemy_wizard.fire_rain_group.draw(self.screen)

    def new_game(self):
        pygame.mixer.music.unload()
        self.player.projectile_group.empty()
        self.enemy_wizard.fire_ball_group.empty()
        self.enemy_wizard.fire_wall_group.empty()
        self.enemy_wizard.fire_rain_group.empty()
        
        self.player = PlayerTank(self, self.screen_size)

        self.enemy_wizard = Wizard(self, self.screen_size, self.player)
        self.enemy_group.add(self.enemy_wizard)

        self.state = "battle"

    def run(self):
        self.running = True

        while self.running:
            if close_game():
                self.running = False

            self.collisions()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()