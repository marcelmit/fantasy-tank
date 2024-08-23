from helper_functions import load_sprite_sheet

class Wizard:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.image = load_sprite_sheet("enemies/wizard_idle", frame=0, width=40, height=60, scale=3, colour=(0, 0, 0))
        self.rect = self.image.get_rect(centerx=self.screen_size[0] // 2, top=0)

        # Sprite animation
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.animation_steps = 8

    def animate_sprite(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame += 1

            if self.animation_frame >= self.animation_steps:
                self.animation_frame = 0

            self.image = load_sprite_sheet("enemies/wizard_idle", frame=self.animation_frame, width=40, height=60, scale=3, colour=(0, 0, 0))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.animate_sprite()