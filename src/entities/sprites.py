import pygame as pg
from pygame.sprite import _Group

class SpriteObject(pg.sprite.Sprite):
    def __init__(self, *groups: _Group) -> None:
        super().__init__(*groups)