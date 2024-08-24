import sys

import pygame

from events import EventHandler
from player import PlayerTank
from enemies import Wizard

class Game:
    def __init__(self):
        pygame.display.set_caption("Fantasy Tank")
        self.screen = pygame.display.set_mode((1800, 800))
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock()

        self.event_handler = EventHandler()

        self.player = PlayerTank(self.screen_size)

        self.enemy_wizard = Wizard(self.screen_size, self.player)
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

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.player.draw(self.screen)
        self.player.projectile_group.draw(self.screen)

        self.enemy_wizard.draw(self.screen)
        self.enemy_wizard.fire_ball_group.draw(self.screen)

    def update(self):
        self.player.update()
        self.player.projectile_group.update()

        self.enemy_wizard.update()
        self.enemy_wizard.fire_ball_group.update()

    def run(self):
        self.running = True

        while self.running:
            self.event_handler.update()

            if self.event_handler.quit():
                self.running = False

            self.collisions()
            self.draw()
            self.update()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()