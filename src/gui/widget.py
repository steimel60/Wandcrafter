import pygame as pg
from config.game_settings import TILESIZE

class Widget:
    def __init__(self, image, alignment, padding = TILESIZE / 2):
        self.image = image
        self.alignment = alignment
        self.padding = padding

    def draw(self, screen: pg.Surface):
        position = self.get_draw_position()
        screen.blit(self.image, position)

    def get_draw_position(self):
        screen_w, screen_h = self.get_screen_size()
        v_align, h_align = self.alignment.split('_')
        x = self.get_horizontal_position(h_align, screen_w)
        y = self.get_vertical_position(v_align, screen_h)
        return (x, y)

    def get_horizontal_position(self, alignment, screen_width):
        if alignment == "center":
            return (screen_width / 2) - (self.image.get_width() / 2)

    def get_vertical_position(self, alignment, screen_height):
        if alignment == "bottom":
            return screen_height - self.image.get_height() - self.padding

    def get_screen_size(self):
        # Get screen info
        screen_info = pg.display.Info()
        # Retrieve screen width and height
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        return (screen_width, screen_height)

    def get_screen_center(self):
        # Get screen info
        screen_info = pg.display.Info()
        # Retrieve screen width and height
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        return (screen_width / 2, screen_height / 2)

    def get_screen_size_in_tiles(self):
        # Get screen info
        screen_info = pg.display.Info()
        # Retrieve screen width and height
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        return (screen_width // TILESIZE, screen_height // TILESIZE)
