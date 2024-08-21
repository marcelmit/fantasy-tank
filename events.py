import pygame

class EventHandler:
    def __init__(self):
        self.events = []

    def update(self):
        self.events = pygame.event.get()

    def mouse_click(self):
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False
    
    def quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False