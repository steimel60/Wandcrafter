from items.wand import Wand
import pygame as pg
from config.game_settings import TILESIZE
from .animation import Animation

class PlayerEntitiy:
    def __init__(
            self,
            name : str = None,
            wand : Wand = None,
            coord : list = [0,0]
            ) -> None:
        self.name = name
        self.wand = wand
        self.x, self.y = coord
        self.height = TILESIZE
        self.width = TILESIZE
        self.rect = pg.Rect(self.x, self.y, self.height, self.width) # hit box
        self.anim_dict = self.initialize_anim_dict()
        self.current_anim = "idle_down"

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_UP | pg.K_w:
                        self.current_anim = "walk_up"
                    case pg.K_DOWN | pg.K_s:
                        self.current_anim = "walk_down"
                    case pg.K_LEFT | pg.K_a:
                        self.current_anim = "walk_left"
                    case pg.K_RIGHT | pg.K_d:
                        self.current_anim = "walk_right"
            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_UP | pg.K_w:
                        self.current_anim = "idle_up"
                    case pg.K_DOWN | pg.K_s:
                        self.current_anim = "idle_down"
                    case pg.K_LEFT | pg.K_a:
                        self.current_anim = "idle_left"
                    case pg.K_RIGHT | pg.K_d:
                        self.current_anim = "idle_right"
    
    def update(self):
        self.rect.x, self.rect.y = self.x, self.y
        self.anim_dict[self.current_anim].update()

    def draw(self, screen):
        screen.blit(self.anim_dict[self.current_anim].get_current_frame(), (self.x, self.y))

    def get_save_data(self):
        return {
            "name" : self.name,
            "wand" : self.wand,
            "coord" : [self.x, self.y]
        }

    def initialize_anim_dict(self):
        return {
            "walk_down" : Animation("walk_down", 15),
            "run_down" : Animation("walk_down", 5),
            "idle_down" : Animation("idle_down", 15),
            "walk_up" : Animation("walk_up", 15),
            "run_up" : Animation("walk_up", 5),
            "idle_up" : Animation("idle_up", 15),
            "walk_left" : Animation("walk_left", 15),
            "run_left" : Animation("walk_left", 5),
            "idle_left" : Animation("idle_left", 15),
            "walk_right" : Animation("walk_right", 15),
            "run_right" : Animation("walk_right", 5),
            "idle_right" : Animation("idle_right", 15)
            }