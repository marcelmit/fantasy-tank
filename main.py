import sys

import pygame

from helper_functions import close_game, keyboard_input, add_data
from player import PlayerTank
from enemies import Wizard
from ui_elements import MenuManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Fantasy Tank")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((960, 540))
        self.screen_size = self.screen.get_size()
        self.resolution = 0.5
        self.font = pygame.font.SysFont("cambria", int(40 * self.resolution))
        self.sound_volume = 0.5
        self.music_volume = 0.5

        self.paused = False
        self.state = "defeat"
        self.data_dict = {}

        # Timer
        self.time = 0
        self.mouse_clicked_time = 0
        self.key_pressed_time = 0
        self.new_game_time = 0
        self.score_time = 0
        self.pause_start_time = 0
        self.pause_end_time = 0
        self.pause_duration = 0

        self.player = PlayerTank(self)
        self.enemy_wizard = Wizard(self, self.player)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy_wizard)
        self.menu_manager = MenuManager(self)

    def collisions(self):
        # Player projectiles
        for projectile in self.player.projectile_group:
            if pygame.sprite.spritecollideany(projectile, self.enemy_group):
                if projectile.type == "cannon":
                    add_data(self, "cannon_hit")
                    self.enemy_wizard.decrease_health(5)
                elif projectile.type == "rocket":
                    add_data(self, "rocket_hit")
                    self.enemy_wizard.decrease_health(50)
                projectile.kill()

        # Fire ball
        if pygame.sprite.spritecollide(self.player, self.enemy_wizard.fire_ball_group, True):
            if self.time - self.player.last_hit_time > self.player.invulnerability_duration:
                self.player.decrease_health(15)
                self.player.last_hit_time = self.time
                add_data(self, "fire_ball")

        # Fire wall
        for fire_wall in self.enemy_wizard.fire_wall_group:
            if pygame.sprite.spritecollideany(self.player, fire_wall.group):
                if self.time - self.player.last_hit_time > self.player.invulnerability_duration:
                    self.player.decrease_health(10)
                    self.player.last_hit_time = self.time
                    add_data(self, "fire_wall")

        # Fire rain
        for fire_rain in self.enemy_wizard.fire_rain_group:
            if fire_rain.has_collision and pygame.sprite.spritecollide(self.player, self.enemy_wizard.fire_rain_group, True):
                self.player.decrease_health(5)
                add_data(self, "fire_rain")

        # Fire beam
        if pygame.sprite.spritecollideany(self.player, self.enemy_wizard.fire_beam_group):
            if self.time - self.player.last_hit_time > self.player.invulnerability_duration:
                self.player.decrease_health(10)
                self.player.last_hit_time = self.time
                add_data(self, "fire_beam")

        # Fire patch
        if pygame.sprite.spritecollide(self.player, self.enemy_wizard.fire_patch_group, True):
            self.player.decrease_health(5)
            add_data(self, "fire_patch")

    def update(self):
        keyboard_input(self)
        current_time = pygame.time.get_ticks() / 1000
        self.time = current_time - self.new_game_time - self.pause_duration

        if not self.paused:
            self.menu_manager.update()
            if self.state == "battle" and not self.paused:
                self.collisions()
                self.score_time += self.clock.get_time() / 1000
                self.player.update()
                self.player.projectile_group.update()
                self.enemy_wizard.update()
                self.enemy_wizard.fire_ball_group.update()
                self.enemy_wizard.fire_wall_group.update()
                self.enemy_wizard.fire_rain_group.update()
                self.enemy_wizard.fire_beam_group.update()
                self.enemy_wizard.fire_patch_group.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.menu_manager.draw()

        if self.state == "battle":
            self.player.draw()
            self.player.projectile_group.draw(self.screen)
            self.enemy_wizard.draw()
            self.enemy_wizard.fire_ball_group.draw(self.screen)
            for fire_wall in self.enemy_wizard.fire_wall_group:
                fire_wall.draw()
            self.enemy_wizard.fire_rain_group.draw(self.screen)
            self.enemy_wizard.fire_beam_group.draw(self.screen)
            self.enemy_wizard.fire_patch_group.draw(self.screen)

    def new_game(self):
        pygame.mixer.music.unload()
        self.new_game_time = pygame.time.get_ticks() / 1000
        self.time = 0
        self.score_time = 0
        self.pause_duration = 0
        self.data_dict = {}
        
        self.player.projectile_group.empty()
        self.enemy_wizard.fire_ball_group.empty()
        self.enemy_wizard.fire_wall_group.empty()
        self.enemy_wizard.fire_rain_group.empty()
        self.enemy_wizard.fire_beam_group.empty()
        self.enemy_wizard.fire_patch_group.empty()
        
        self.player = PlayerTank(self)
        self.enemy_wizard = Wizard(self, self.player)
        self.enemy_group.add(self.enemy_wizard)

        self.state = "battle"

    def run(self):
        self.running = True

        while self.running:
            if close_game():
                self.running = False

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()