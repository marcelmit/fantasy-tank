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

        self.enemy_wizard = Wizard(self.screen_size)

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.player.draw(self.screen)
        self.player.projectile_group.draw(self.screen)

        self.enemy_wizard.draw(self.screen)

    def update(self):
        self.player.update()
        self.player.projectile_group.update()

        self.enemy_wizard.update()

    def run(self):
        self.running = True

        while self.running:
            self.event_handler.update()

            if self.event_handler.quit():
                self.running = False

            self.draw()
            self.update()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()