import random

import pygame

from helper_functions import load_image, load_sound, load_music

class UI:
    @staticmethod
    def init(game):
        UI.screen = game.screen
        UI.screen_size = game.screen.get_size()
        UI.resolution = game.resolution
        UI.font = pygame.font.SysFont("cambria", int(40 * UI.resolution))
        UI.click_sound = load_sound("click_sound")
        UI.game_volume = 0.5

class MenuManager:
    def __init__(self, game):
        self.game = game
        self.menus = {
            "menu": MainMenu(),
            "options": OptionsMenu(),
            "battle": Battle(),
            "victory": GameOver("victory"),
            "defeat": GameOver("defeat")
        }
    
    def play_music(self):
        if pygame.mixer.music.get_busy() == False:
            if self.game.game_state == "menu":
                load_music("menu")
                pygame.mixer.music.play(- 1)
            if self.game.game_state == "battle":
                load_music("battle")
                pygame.mixer.music.play(- 1)
            if self.game.game_state == "victory":
                load_music("victory")
                pygame.mixer.music.play(- 1)
            if self.game.game_state == "defeat":
                load_music("defeat")
                pygame.mixer.music.play(- 1)

    def update(self):
        #self.play_music()
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
        self.sliders = []

    def add_background(self, background):
        self.backgrounds.append(background)

    def add_button(self, button):
        self.buttons.append(button)

    def add_slider(self, slider):
        self.sliders.append(slider)
        
    def update(self, game):
        for button in self.buttons:
            if button.mouse_interaction():
                self.handle_mouse_click(game, button)

    def draw(self):
        for background in self.backgrounds:
            background.draw()
        for button in self.buttons:
            button.draw()
        for slider in self.sliders:
            slider.draw()
            slider.update()

class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_background(Background("ui/main_menu_background", (960, 540), (1920, 1080)))
        self.add_background(Background("ui/box_square", (960, 540), (400, 400)))

        self.add_button(Button("ui/button_square", (960, 430), (240, 100), text="Play"))
        self.add_button(Button("ui/button_square", (960, 545), (240, 100), text="Options"))
        self.add_button(Button("ui/button_square", (960, 660), (240, 100), text="Exit"))

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

    def handle_mouse_click(self, game, button):
        if button.original_text == "Play":
            game.new_game()
        elif button.original_text == "Options":
            game.game_state = "options"
        elif button.original_text == "Exit":
            game.running = False

class OptionsMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_background(Background("ui/main_menu_background", (960, 540), (1920, 1080)))
        self.add_background(Background("ui/box_square", (960, 540), (500, 500)))

        self.add_background(Background("ui/audio", (800, 370), (50, 50)))
        self.add_background(Background("ui/slider_blank_frame", (1020, 370), (300, 50)))
        self.add_slider(Slider("ui/slider_blank_button", (1020, 370), (50, 50), (890, 1150), "sound_volume"))
        self.add_background(Background("ui/music", (800, 470), (50, 50)))
        self.add_background(Background("ui/slider_blank_frame", (1020, 470), (300, 50)))
        self.add_slider(Slider("ui/slider_blank_button", (1020, 470), (50, 50), (890, 1150), "music_volume"))

        self.add_button(Button("ui/return_button", (1140, 722), (90, 90), text=""))

    def handle_mouse_click(self, game, button):
        if button.original_text == "":
            game.game_state = "menu"

class Battle(Menu):
    def __init__(self):
        super().__init__()
        self.cloud_generator = CloudGenerator()

        self.ui_elements = [
            Background("ui/battle_background", (960, 650), (1920, 870)),
            Background("ui/sky_background", (960, 100), (1920, 230))
        ]

    def update(self, game):
        self.cloud_generator.update()

    def draw(self):
        for element in self.ui_elements:
            element.draw()
        self.cloud_generator.draw()

class GameOver(Menu):
    def __init__(self, condition):
        super().__init__()
        self.add_background(Background("ui/box_square", (960, 540), (500, 500)))
        if condition == "victory":
            self.add_background(Background("ui/box_blue_square", (960, 300), (200, 100), text="Victory", text_pos=(960, 300)))
        elif condition == "defeat":
            self.add_background(Background("ui/box_blue_square", (960, 300), (200, 100), text="Defeat", text_pos=(960, 300)))

        self.add_button(Button("ui/main_menu", (800, 710), (90, 90), text=""))
        self.add_button(Button("ui/button_square", (1100, 720), (140, 60), text="Retry"))

    def handle_mouse_click(self, game, button):
        if button.original_text == "":
            pygame.mixer.music.unload()
            game.game_state = "menu"
        if button.original_text == "Retry":
            game.new_game()

class Background:
    def __init__(self, image, pos, size, text=None, text_pos=None):
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * UI.resolution, size[1] * UI.resolution))
        self.rect = self.image.get_rect(center = (pos[0] * UI.resolution, pos[1] * UI.resolution))

        self.text = text
        if text and text_pos:
            self.text = UI.font.render(text, True, "white")
            self.text_rect = self.text.get_rect(center = (text_pos[0] * UI.resolution, text_pos[1] * UI.resolution))

    def draw(self):
        UI.screen.blit(self.image, self.rect)
        if self.text and self.text_rect:
            UI.screen.blit(self.text, self.text_rect)

class Button:
    def __init__(self, image, pos, size, text=None):
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * UI.resolution, size[1] * UI.resolution))
        self.rect = self.image.get_rect(center = (pos[0] * UI.resolution, pos[1] * UI.resolution))

        self.original_text = text
        if text:
            self.text = UI.font.render(self.original_text, True, "white")
            self.text_rect = self.text.get_rect(center = (pos[0] * UI.resolution, pos[1] * UI.resolution))

    def mouse_interaction(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_input = pygame.mouse.get_pressed()

        # Mouse clicked
        if self.rect.collidepoint(mouse_pos) and mouse_input[0]:
            UI.click_sound.play()
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

class Slider:
    def __init__(self, image, pos, size, value_range, slider_type):
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * UI.resolution, size[1] * UI.resolution))
        self.rect = self.image.get_rect(center = (pos[0] * UI.resolution, pos[1] * UI.resolution))

        self.value_range = value_range[0] * UI.resolution, value_range[1] * UI.resolution
        self.slider_type = slider_type

        self.dragging = False

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if mouse_click[0]:
            if self.dragging:
                pos = mouse_position[0]
                pos = max(self.value_range[0], min(pos, self.value_range[1]))
                self.rect.centerx = pos

                if self.slider_type == "sound_volume":
                    UI.game_volume = (self.rect.centerx - self.value_range[0]) / (self.value_range[1] - self.value_range[0])
                    pygame.mixer.Sound.set_volume(UI.click_sound, UI.game_volume)
                    UI.click_sound.play()
                elif self.slider_type == "music_volume":
                    music_volume = (self.rect.centerx - self.value_range[0]) / (self.value_range[1] - self.value_range[0])
                    pygame.mixer.music.set_volume(music_volume)

            elif self.rect.collidepoint(mouse_position):
                self.dragging = True
        else:
            self.dragging = False

    def draw(self):
        UI.screen.blit(self.image, self.rect)

class Cloud:
    def __init__(self, pos):
        size = (random.randint(50, 100), random.randint(25, 50))
        rnd = random.randint(1, 8)
        image = f"ui/cloud_{rnd}"

        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * UI.resolution, size[1] * UI.resolution))
        self.rect = self.image.get_rect(center = (pos[0], pos[1] * UI.resolution))

    def update(self):
        self.rect.x += 1

    def draw(self):
        UI.screen.blit(self.image, self.rect)

class CloudGenerator:
    def __init__(self):
        self.clouds = []

        self.generate_initial_clouds(10)
        self.last_cloud = 0
        self.cloud_cooldown = 3

    def generate_cloud(self):
        current_time = pygame.time.get_ticks() / 1000
        pos = (- 50, random.randint(10, 190))

        if current_time - self.last_cloud > self.cloud_cooldown:
            self.clouds.append(Cloud(pos))
            self.last_cloud = current_time

    def generate_initial_clouds(self, count):
        step = UI.screen_size[0] // count

        for i in range(count):
            x_pos = step * i + random.randint(- 50, 50)
            pos = (x_pos, random.randint(10, 190))
            self.clouds.append(Cloud(pos))

    def update(self):
        self.generate_cloud()

        for cloud in self.clouds:
            cloud.update()
            if cloud.rect.left > UI.screen_size[0]:
                self.clouds.remove(cloud)

    def draw(self):
        for cloud in self.clouds:
            cloud.draw()