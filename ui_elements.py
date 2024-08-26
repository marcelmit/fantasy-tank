import pygame

from helper_functions import load_image

class UI:
    @staticmethod
    def init(game):
        UI.screen = game.screen
        UI.resolution = game.resolution
        UI.screen_width, UI.screen_height = game.screen_size
        UI.font = pygame.font.SysFont("cambria", int(40 * UI.resolution))

class MenuManager:
    def __init__(self, game):
        self.game = game
        self.menus = {
            "menu": MainMenu(),
            "options": OptionsMenu(),
            "defeat": Defeat()
        }

    def update(self):
        current_menu = self.menus.get(self.game.game_state)
        if current_menu:
            current_menu.update(self.game)

    def draw(self):
        current_menu = self.menus.get(self.game.game_state)
        if current_menu:
            current_menu.draw()

class Menu:
    def __init__(self):
        self.backgrounds = []
        self.buttons = []

    def add_background(self, background):
        self.backgrounds.append(background)

    def add_button(self, button):
        self.buttons.append(button)
        
    def update(self, game):
        for button in self.buttons:
            if button.mouse_interaction():
                self.handle_mouse_click(game, button)

    def draw(self):
        for background in self.backgrounds:
            background.draw()
        for button in self.buttons:
            button.draw()

class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_background(Background("ui/main_menu_background", (960, 540), (1920, 1080)))
        self.add_background(Background("ui/box_square", (960, 540), (400, 400)))
        self.add_background(Background("ui/box_blue_square", (360, 450), (360, 275), text="Move", text_pos=(360, 450)))
        self.add_background(Background("ui/w", (360, 400), (50, 50)))
        self.add_background(Background("ui/up", (360, 350), (50, 50)))
        self.add_background(Background("ui/s", (360, 500), (50, 50)))
        self.add_background(Background("ui/down", (360, 550), (50, 50)))
        self.add_background(Background("ui/a", (265, 450), (50, 50)))
        self.add_background(Background("ui/left", (215, 450), (50, 50)))
        self.add_background(Background("ui/d", (455, 450), (50, 50)))
        self.add_background(Background("ui/right", (505, 450), (50, 50)))
        self.add_background(Background("ui/box_blue_square", (360, 750), (400, 175), text="Shoot", text_pos=(360, 700)))
        self.add_background(Background("ui/space_left", (200, 760), (50, 50)))
        self.add_background(Background("ui/space_middle", (250, 760), (50, 50)))
        self.add_background(Background("ui/space_middle", (300, 760), (50, 50), text="Cannon", text_pos=(270, 810)))
        self.add_background(Background("ui/space_right", (350, 760), (50, 50)))
        self.add_background(Background("ui/ctrl_left", (455, 760), (50, 50), text="Rocket", text_pos=(470, 810)))
        self.add_background(Background("ui/ctrl_right", (505, 760), (50, 50)))

        self.add_button(Button("ui/button_square", (960, 430), (240, 100), text="Play"))
        self.add_button(Button("ui/button_square", (960, 545), (240, 100), text="Options"))
        self.add_button(Button("ui/button_square", (960, 660), (240, 100), text="Exit"))
        
    def handle_mouse_click(self, game, button):
        if button.original_text == "Play":
            game.game_state = "gameplay"
        elif button.original_text == "Options":
            game.game_state = "options"
        elif button.original_text == "Exit":
            game.running = False

class OptionsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_background(Background("ui/main_menu_background", (960, 540), (1920, 1080)))
        self.add_background(Background("ui/box_square", (960, 540), (500, 500)))

        self.add_button(Button("ui/return_button", (1140, 722), (90, 90), text=""))

    def handle_mouse_click(self, game, button):
        if button.original_text == "":
            game.game_state = "menu"

class Defeat(Menu):
    def __init__(self):
        super().__init__()
        self.add_background(Background("ui/box_square", (960, 540), (500, 500)))

        self.add_button(Button("ui/main_menu", (800, 710), (90, 90), text=""))
        self.add_button(Button("ui/button_square", (1100, 720), (140, 60), text="Retry"))

    def handle_mouse_click(self, game, button):
        if button.original_text == "":
            game.game_state = "menu"
        elif button.original_text == "Retry":
            game.game_state = "gameplay"

class Background:
    def __init__(self, image, pos, size, text=None, text_pos=None):
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * UI.resolution, size[1] * UI.resolution))
        self.rect = self.image.get_rect(center=(pos[0] * UI.resolution, pos[1] * UI.resolution))

        self.text = text
        if text and text_pos:
            self.text = UI.font.render(text, True, "white")
            self.text_rect = self.text.get_rect(center=(text_pos[0] * UI.resolution, text_pos[1] * UI.resolution))

    def draw(self):
        UI.screen.blit(self.image, self.rect)
        if self.text and self.text_rect:
            UI.screen.blit(self.text, self.text_rect)

class Button:
    def __init__(self, image, pos, size, text=None):
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * UI.resolution, size[1] * UI.resolution))
        self.rect = self.image.get_rect(center=(pos[0] * UI.resolution, pos[1] * UI.resolution))

        self.original_text = text
        if text:
            self.text = UI.font.render(self.original_text, True, "white")
            self.text_rect = self.text.get_rect(center=(pos[0] * UI.resolution, pos[1] * UI.resolution))

    def mouse_interaction(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_input = pygame.mouse.get_pressed()

        # Mouse clicked
        if self.rect.collidepoint(mouse_pos) and mouse_input[0]:
            return True
        
        # Mouse hovered
        if self.original_text:
            if self.rect.collidepoint(mouse_pos):
                self.text = UI.font.render(self.original_text, True, "green")
            else:
                self.text = UI.font.render(self.original_text, True, "white")

    def draw(self):
        UI.screen.blit(self.image, self.rect)
        if self.original_text:
            UI.screen.blit(self.text, self.text_rect)