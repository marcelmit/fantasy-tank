import random

import pygame

from helper_functions import load_image, load_sound, load_music, mouse_input, set_resolution, calculate_score

class MenuManager:
    def __init__(self, game):
        self.game = game

        self.current_menu = None
        self.last_game_state = None
        
        self.menus = {
            "menu": MainMenu(self.game),
            "options": OptionsMenu(self.game, "options"),
            "battle_options": OptionsMenu(self.game, "battle_options"),
            "battle": Battle(self.game),
            "victory": GameOver(self.game, "victory"),
            "defeat": GameOver(self.game, "defeat")
        }

    def initialize_menu(self):
        if self.game.state == "menu":
            self.current_menu = MainMenu(self.game)
        elif self.game.state == "options":
            self.current_menu = OptionsMenu(self.game, "options")
        elif self.game.state == "battle_options":
            self.current_menu = OptionsMenu(self.game, "battle_options")
        elif self.game.state == "battle":
            self.current_menu = Battle(self.game)
        elif self.game.state == "victory":
            self.current_menu = GameOver(self.game, "victory")
        elif self.game.state == "defeat":
            self.current_menu = GameOver(self.game, "defeat")
    
    def play_music(self):
        if not pygame.mixer.music.get_busy():
            if self.game.state == "menu":
                load_music("menu")
                pygame.mixer.music.play(- 1)
            elif self.game.state == "battle":
                load_music("battle")
                pygame.mixer.music.play(- 1)
            elif self.game.state == "victory":
                load_music("victory")
                pygame.mixer.music.play(- 1)
            elif self.game.state == "defeat":
                load_music("defeat")
                pygame.mixer.music.play(- 1)

    def update(self):
        #self.play_music()

        if self.game.state != self.last_game_state:
            self.initialize_menu()
            self.last_game_state = self.game.state

        self.current_menu.update()

    def draw(self):
        self.current_menu.draw()

class Menu:
    def __init__(self, game):
        self.game = game

        self.backgrounds = []
        self.buttons = []
        self.sliders = []
        self.text = []

    def add_background(self, image, pos, size, text=None, text_pos=None, text_col="white", hp_bar=False):
        background = Background(image, pos, size, self.game, text, text_pos, text_col, hp_bar)
        self.backgrounds.append(background)

    def add_button(self, image, pos, size, text=None):
        button = Button(image, pos, size, self.game, text)
        self.buttons.append(button)

    def add_slider(self, image, pos, size, value_range, slider_type):
        slider = Slider(image, pos, size, value_range, slider_type, self.game)
        self.sliders.append(slider)

    def add_text(self, text, pos, text_col="white"):
        text = Text(text, pos, self.game, text_col)
        self.text.append(text)

    def update(self):
        for button in self.buttons:
            if button.mouse_interaction():
                self.handle_mouse_click(button)

    def draw(self):
        for background in self.backgrounds:
            background.draw()
        for button in self.buttons:
            button.draw()
        for slider in self.sliders:
            slider.draw()
            slider.update()
        for text in self.text:
            text.draw()

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.add_background("ui/main_menu_background", (960, 540), (1920, 1080))
        self.add_background("ui/box_square", (960, 540), (400, 400))

        self.add_button("ui/button_square", (960, 430), (240, 100), text="Play")
        self.add_button("ui/button_square", (960, 545), (240, 100), text="Options")
        self.add_button("ui/button_square", (960, 660), (240, 100), text="Exit")

        self.add_background("ui/box_blue_square", (360, 300), (360, 275), text="Move", text_pos=(360, 300))
        self.add_background("ui/w", (360, 250), (50, 50))
        self.add_background("ui/up", (360, 200), (50, 50))
        self.add_background("ui/s", (360, 350), (50, 50))
        self.add_background("ui/down", (360, 400), (50, 50))
        self.add_background("ui/a", (265, 300), (50, 50))
        self.add_background("ui/left", (215, 300), (50, 50))
        self.add_background("ui/d", (455, 300), (50, 50))
        self.add_background("ui/right", (505, 300), (50, 50))

        self.add_background("ui/box_blue_square", (360, 600), (400, 175), text="Shoot", text_pos=(360, 550))
        self.add_background("ui/space_left", (200, 605), (50, 50))
        self.add_background("ui/space_middle", (250, 605), (50, 50))
        self.add_background("ui/space_middle", (300, 605), (50, 50), text="Cannon", text_pos=(270, 660))
        self.add_background("ui/space_right", (350, 605), (50, 50))
        self.add_background("ui/ctrl_left", (455, 605), (50, 50), text="Rocket", text_pos=(470, 660))
        self.add_background("ui/ctrl_right", (505, 605), (50, 50))

        self.add_background("ui/box_blue_square", (360, 825), (360, 125))
        self.add_background("ui/escape", (280, 800), (50, 50), text="Options", text_pos=(280, 850))
        self.add_background("ui/p", (460, 800), (50, 50), text="Pause", text_pos=(460, 850))

    def handle_mouse_click(self, button):
        if button.original_text == "Play":
            self.game.new_game()
        elif button.original_text == "Options":
            self.game.state = "options"
        elif button.original_text == "Exit":
            self.game.running = False

class OptionsMenu(Menu):
    def __init__(self, game, state):
        super().__init__(game)
        self.add_background("ui/main_menu_background", (960, 540), (1920, 1080))

        self.add_background("ui/box_blue_square", (360, 300), (360, 275), text="Move", text_pos=(360, 300))
        self.add_background("ui/w", (360, 250), (50, 50))
        self.add_background("ui/up", (360, 200), (50, 50))
        self.add_background("ui/s", (360, 350), (50, 50))
        self.add_background("ui/down", (360, 400), (50, 50))
        self.add_background("ui/a", (265, 300), (50, 50))
        self.add_background("ui/left", (215, 300), (50, 50))
        self.add_background("ui/d", (455, 300), (50, 50))
        self.add_background("ui/right", (505, 300), (50, 50))

        self.add_background("ui/box_blue_square", (360, 600), (400, 175), text="Shoot", text_pos=(360, 550))
        self.add_background("ui/space_left", (200, 605), (50, 50))
        self.add_background("ui/space_middle", (250, 605), (50, 50))
        self.add_background("ui/space_middle", (300, 605), (50, 50), text="Cannon", text_pos=(270, 660))
        self.add_background("ui/space_right", (350, 605), (50, 50))
        self.add_background("ui/ctrl_left", (455, 605), (50, 50), text="Rocket", text_pos=(470, 660))
        self.add_background("ui/ctrl_right", (505, 605), (50, 50))

        self.add_background("ui/box_blue_square", (360, 825), (360, 125))
        self.add_background("ui/escape", (280, 800), (50, 50), text="Options", text_pos=(280, 850))
        self.add_background("ui/p", (460, 800), (50, 50), text="Pause", text_pos=(460, 850))

        self.add_background("ui/box_square", (960, 540), (500, 500))
        self.add_button("ui/main_menu", (1140, 722), (90, 90), text="")

        self.add_background("ui/audio", (800, 370), (50, 50))
        self.add_background("ui/slider_blank_frame", (1020, 370), (300, 50))
        self.add_slider("ui/slider_blank_button", (1020, 370), (50, 50), (890, 1150), "sound_volume")
        self.add_background("ui/music", (800, 470), (50, 50))
        self.add_background("ui/slider_blank_frame", (1020, 470), (300, 50))
        self.add_slider("ui/slider_blank_button", (1020, 470), (50, 50), (890, 1150), "music_volume")

        if state == "options":
            self.add_background("ui/box_square", (1500, 540), (300, 500))
            self.add_text("Resolution", (1500, 360))
            self.add_button("ui/button_square", (1500, 455), (240, 80), text="1920x1080")
            self.add_button("ui/button_square", (1500, 545), (240, 80), text="1600x900")
            self.add_button("ui/button_square", (1500, 635), (240, 80), text="1280x720")
            self.add_button("ui/button_square", (1500, 725), (240, 80), text="960x540")

    def handle_mouse_click(self, button):
        if button.original_text == "" and self.game.state == "battle_options":
            pygame.mixer.music.unload()
        if button.original_text == "":
            self.game.state = "menu"
        elif button.original_text == "1920x1080":
            set_resolution(self.game, "1920x1080")
            self.game.state = "menu"
        elif button.original_text == "1600x900":
            set_resolution(self.game, "1600x900")
            self.game.state = "menu"
        elif button.original_text == "1280x720":
            set_resolution(self.game, "1280x720")
            self.game.state = "menu"
        elif button.original_text == "960x540":
            set_resolution(self.game, "960x540")
            self.game.state = "menu"

class Battle(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.add_background("ui/battle_background", (960, 650), (1920, 870))
        self.add_background("ui/sky_background", (960, 100), (1920, 230))
        self.cloud_generator = CloudGenerator(self.game)
        self.pause_text = Text("PAUSED", (960, 540), self.game, text_col="red", size=(250, 200))

    def update_stats(self):
        self.stat_elements = [
            Background("ui/hp_bar", (40, 60), (max(0, 500 * self.game.player.health / self.game.player.max_health), 50), self.game, hp_bar=True),
            Background("ui/slider_blank_frame", (290, 60), (500, 70), self.game, text=f"{self.game.player.health} / {self.game.player.max_health}", text_pos=(280, 60), text_col="black"),
            Background("player/player_tank", (40, 60), (65, 65), self.game),
            Background("ui/hp_bar", (1400, 60), (max(0, 500 * self.game.enemy_wizard.health / self.game.enemy_wizard.max_health), 50), self.game, hp_bar=True),
            Background("ui/slider_blank_frame", (1630, 60), (500, 70), self.game, text=f"{self.game.enemy_wizard.health} / {self.game.enemy_wizard.max_health}", text_pos=(1630, 60), text_col="black"),
            Background("enemies/wizard", (1395, 60), (140, 120), self.game,),
            Background("player/rocket", (40, 150), (50, 75), self.game,),
            Text(f"{self.game.player.rocket_ammo} / {self.game.player.max_rocket_ammo}", (130, 150), self.game, text_col="black")
        ]

    def update(self):
        self.cloud_generator.update()
        self.update_stats()

    def draw(self):
        for element in self.backgrounds:
            element.draw()
        self.cloud_generator.draw()
        for element in self.stat_elements:
            element.draw()
        if self.game.paused:
            self.pause_text.draw()

class GameOver(Menu):
    def __init__(self, game, state):
        super().__init__(game)
        minutes, seconds = divmod(self.game.score_timer, 60)

        self.add_background("ui/main_menu_background", (960, 540), (1920, 1080))
        self.add_background("ui/box_square", (960, 540), (1000, 800))
        if state == "victory":
            self.add_background("ui/box_blue_square", (960, 150), (200, 100), text="Victory", text_pos=(960, 150))
        elif state == "defeat":
            self.add_background("ui/box_blue_square", (960, 150), (200, 100), text="Defeat", text_pos=(960, 150))

        self.add_text("Hits taken", (630, 280))
        self.add_text("Hits done", (960, 280))
        self.add_text("Hits missed", (1290, 280))
        self.add_text(f"Time: {int(minutes)}:{int(seconds):02}", (950, 700))
        self.add_text(f"Score: {calculate_score(self.game.score_timer, self.game.data_dict)}", (1250, 700))

        self.add_background("enemies/fire_ball", (590, 410), (150, 150), text=f"{self.game.data_dict["fire_ball"] if "fire_ball" in self.game.data_dict else 0}", text_pos=(690, 410))
        self.add_background("enemies/fire_wall", (590, 550), (100, 100), text=f"{self.game.data_dict["fire_wall"] if "fire_wall" in self.game.data_dict else 0}", text_pos=(690, 550))
        self.add_background("enemies/fire_rain_2", (590, 690), (100, 100), text=f"{self.game.data_dict["fire_rain"] if "fire_rain" in self.game.data_dict else 0}", text_pos=(690, 690))
        self.add_background("enemies/fire_rain_2", (590, 820), (100, 100), text=f"{self.game.data_dict["fire_rain"] if "fire_rain" in self.game.data_dict else 0}", text_pos=(690, 820))

        self.add_background("player/cannon", (920, 400), (50, 60), text=f"{self.game.data_dict["cannon_hit"] if "cannon_hit" in self.game.data_dict else 0}", text_pos=(1020, 400))
        self.add_background("player/rocket", (920, 520), (50, 80), text=f"{self.game.data_dict["rocket_hit"] if "rocket_hit" in self.game.data_dict else 0}", text_pos=(1020, 520))

        self.add_background("player/cannon", (1230, 400), (50, 60), text=f"{self.game.data_dict["cannon_miss"] if "cannon_miss" in self.game.data_dict else 0}", text_pos=(1330, 400))
        self.add_background("player/rocket", (1230, 520), (50, 80), text=f"{self.game.data_dict["rocket_miss"] if "rocket_miss" in self.game.data_dict else 0}", text_pos=(1330, 520))

        self.add_button("ui/main_menu", (1350, 850), (90, 90), text="")
        self.add_button("ui/button_square", (960, 850), (180, 80), text="Retry")

    def handle_mouse_click(self, button):
        if button.original_text == "":
            pygame.mixer.music.unload()
            self.game.state = "menu"
        if button.original_text == "Retry":
            self.game.new_game()

class Text:
    def __init__(self, text, pos, game, text_col="white", size=False):
        self.game = game

        self.original_text = self.game.font.render(text, True, text_col)
        self.text = self.original_text
        if size:
            self.text = pygame.transform.scale(self.original_text, (size[0] * self.game.resolution, size[1] * self.game.resolution))
        self.rect = self.text.get_rect(center = (pos[0] * self.game.resolution, pos[1] * self.game.resolution))
        
    def draw(self):
        self.game.screen.blit(self.text, self.rect)

class Background:
    def __init__(self, image, pos, size, game, text=None, text_pos=None, text_col="white", hp_bar=False):
        self.game = game

        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * self.game.resolution, size[1] * self.game.resolution))
        self.rect = self.image.get_rect(center = (pos[0] * self.game.resolution, pos[1] * self.game.resolution))
        if hp_bar:
            self.rect.left = pos[0] * self.game.resolution

        self.text = text
        if text and text_pos:
            self.text = self.game.font.render(text, True, text_col)
            self.text_rect = self.text.get_rect(center = (text_pos[0] * self.game.resolution, text_pos[1] * self.game.resolution))

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        if self.text and self.text_rect:
            self.game.screen.blit(self.text, self.text_rect)

class Button:
    def __init__(self, image, pos, size, game, text=None):
        self.game = game

        self.click_sound = load_sound("click_sound")
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * self.game.resolution, size[1] * self.game.resolution))
        self.rect = self.image.get_rect(center = (pos[0] * self.game.resolution, pos[1] * self.game.resolution))

        self.original_text = text
        if text:
            self.text = self.game.font.render(self.original_text, True, "white")
            self.text_rect = self.text.get_rect(center = (pos[0] * self.game.resolution, pos[1] * self.game.resolution))

    def mouse_interaction(self):
        mouse_pos = pygame.mouse.get_pos()

        # Mouse clicked
        if self.rect.collidepoint(mouse_pos) and mouse_input(self.game):
            pygame.mixer.Sound.set_volume(self.click_sound, self.game.sound_volume)
            self.click_sound.play()
            return True
        
        # Mouse hovered
        if self.original_text:
            if self.rect.collidepoint(mouse_pos):
                self.text = self.game.font.render(self.original_text, True, "green")
            else:
                self.text = self.game.font.render(self.original_text, True, "white")

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        if self.original_text:
            self.game.screen.blit(self.text, self.text_rect)

class Slider:
    def __init__(self, image, pos, size, value_range, slider_type, game):
        self.slider_type = slider_type
        self.game = game

        self.click_sound = load_sound("click_sound")
        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * self.game.resolution, size[1] * self.game.resolution))
        self.rect = self.image.get_rect(center = (pos[0] * self.game.resolution, pos[1] * self.game.resolution))

        # Initial slider position
        if slider_type == "sound_volume":
            initial_value = self.game.sound_volume
        elif slider_type == "music_volume":
            initial_value = self.game.music_volume

        self.value_range = value_range[0] * self.game.resolution, value_range[1] * self.game.resolution
        self.rect.centerx = self.value_range[0] + (initial_value * (self.value_range[1] - self.value_range[0]))

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
                    self.game.sound_volume = (self.rect.centerx - self.value_range[0]) / (self.value_range[1] - self.value_range[0])
                    pygame.mixer.Sound.set_volume(self.click_sound, self.game.sound_volume)
                    self.click_sound.play()
                elif self.slider_type == "music_volume":
                    self.game.music_volume = (self.rect.centerx - self.value_range[0]) / (self.value_range[1] - self.value_range[0])
                    pygame.mixer.music.set_volume(self.game.music_volume)

            elif self.rect.collidepoint(mouse_position):
                self.dragging = True
        else:
            self.dragging = False

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class Cloud:
    def __init__(self, game, pos):
        self.game = game

        size = (random.randint(50, 100), random.randint(25, 50))
        rnd = random.randint(1, 8)
        image = f"ui/cloud_{rnd}"

        self.original_image = load_image(image)
        self.image = pygame.transform.scale(self.original_image, (size[0] * self.game.resolution, size[1] * self.game.resolution))
        self.rect = self.image.get_rect(center = (pos[0], pos[1] * self.game.resolution))

    def update(self):
        self.rect.x += 1

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

class CloudGenerator:
    def __init__(self, game):
        self.game = game

        self.clouds = []

        self.generate_initial_clouds(10)
        self.last_cloud = 0
        self.cloud_cooldown = 3

    def generate_cloud(self):
        current_time = pygame.time.get_ticks() / 1000
        pos = (- 50, random.randint(10, 190))

        if current_time - self.last_cloud > self.cloud_cooldown:
            self.clouds.append(Cloud(self.game, pos))
            self.last_cloud = current_time

    def generate_initial_clouds(self, count):
        step = self.game.screen_size[0] // count

        for i in range(count):
            x_pos = step * i + random.randint(- 50, 50)
            pos = (x_pos, random.randint(10, 190))
            self.clouds.append(Cloud(self.game, pos))

    def update(self):
        self.generate_cloud()

        for cloud in self.clouds:
            cloud.update()
            if cloud.rect.left > self.game.screen_size[0]:
                self.clouds.remove(cloud)

    def draw(self):
        for cloud in self.clouds:
            cloud.draw()