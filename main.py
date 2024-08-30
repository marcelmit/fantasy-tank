import sys

import pygame

from events import EventHandler
from player import PlayerTank
from enemies import Wizard
from ui_elements import UI, MenuManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Fantasy Tank")
        self.screen = pygame.display.set_mode((1920, 1080)) # 1920, 1080 > 1600, 900 > 1280, 720 > 960, 540
        self.resolution = 1
        self.screen = pygame.display.set_mode((960, 540))
        self.resolution = 0.5
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.game_state = "menu"
        UI.init(self)

        self.event_handler = EventHandler()
        self.menu_manager = MenuManager(self)

        self.player = PlayerTank(self, self.screen_size)

        self.enemy_wizard = Wizard(self, self.screen_size, self.player)
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy_wizard)

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

    def update(self):
        self.menu_manager.update()

        if self.game_state == "battle":
            self.player.update()
            self.player.projectile_group.update()

            self.enemy_wizard.update()
            self.enemy_wizard.fire_ball_group.update()

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.menu_manager.draw()

        if self.game_state == "battle":
            self.menu_manager.draw()
            self.player.draw(self.screen)
            self.player.projectile_group.draw(self.screen)

            self.enemy_wizard.draw(self.screen)
            self.enemy_wizard.fire_ball_group.draw(self.screen)

    def run(self):
        self.running = True

        while self.running:
            self.event_handler.update()

            if self.event_handler.quit():
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