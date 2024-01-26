import pygame as pg
from config.game_settings import FPS

class FadeOut:
    def __init__(self, screen, game_state, color = (0,0,0,0), fade_time = 0.5) -> None:
        self.gs = game_state
        self.gs.sprite_groups["all_sprites"].append(self)
        self.img = pg.Surface(screen.get_size(), pg.SRCALPHA)
        self.fade_time = fade_time
        self.color = color
        self.timer = 0

    def update(self):
        self.timer += 1 / FPS
        self.color = (self.color[0], self.color[1], self.color[2], min(255 * (self.timer / self.fade_time), 255))
        if self.is_done():
            self.gs.sprite_groups["all_sprites"].remove(self)

    def draw(self, screen):
        self.img.fill(self.color)
        screen.blit(self.img, (0,0))

    def is_done(self):
        return self.timer > self.fade_time