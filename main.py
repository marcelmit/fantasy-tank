import sys

import pygame

from events import EventHandler

class Game:
    def __init__(self):
        pygame.display.set_caption("Fantasy Tank")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def run(self):
        self.running = True

        while self.running:
            EventHandler.update(self)

            if EventHandler.quit(self):
                self.running = False

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()