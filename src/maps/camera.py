import pygame as pg

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move (self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(screenWidth / 2)
        y = -target.rect.y + int(screenHeight / 2)

        ## limit scrolling to map size
        x = min(0,x) # left
        x = max(-(self.width - screenWidth), x) # right
        y = min(0,y) # top
        y = max(-(self.height - screenHeight), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)