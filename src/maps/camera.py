import pygame as pg
from config.game_settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Moves things with camera.
        
        eg: Keeping a mini-map in the top right corner of the screen.
        """
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """Move rects with camera."""
        return rect.move(self.camera.topleft)

    def update(self, target):
        """Move camera to keep player center screen."""
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        ## limit scrolling to map size
        x = min(0,x) # left
        x = max(-(self.width - SCREEN_WIDTH), x) # right
        y = min(0,y) # top
        y = max(-(self.height - SCREEN_HEIGHT), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)