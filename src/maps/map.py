import pygame as pg
import pytmx
from config.directories import MAP_DIR

class TiledMap:
    def __init__(self, map_name):
        self.name = map_name
        tm = pytmx.load_pygame(MAP_DIR / map_name / f"{map_name}.tmx", pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height =tm.height * tm.tileheight
        self.tmxdata = tm
        self.image = self.make_map()

    def render(self, surface):
        """Create the image for the map"""
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        """Creates a PyGame surface that can be Blit to the screen"""
        temp_surface = pg.Surface((self.width, self.height))
        self.render (temp_surface)
        return temp_surface
    
    def draw(self, screen):
        screen.blit(self.image, (0,0))